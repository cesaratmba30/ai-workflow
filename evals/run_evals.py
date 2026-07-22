#!/usr/bin/env python3
"""Eval runner for ai-workflow skills. Works with the claude and codex CLIs.

Usage:
  python evals/run_evals.py --agent claude --skill roast --trials 3
  python evals/run_evals.py --agent codex  --skill roast --trials 3
  python evals/run_evals.py --agent claude --all
  python evals/run_evals.py --agent claude --skill tdd --no-skill   # retirement test
  python evals/run_evals.py --agent claude --skill roast --judge    # + LLM-as-judge on
                                                                     # cases with judge_criteria

Design (per Schmid): isolated temp workspace per case (no context bleed),
multiple trials (nondeterminism), deterministic checks from checks.py,
marker-based trigger detection, outcome-graded not path-graded. A nonzero
CLI exit code is always a hard error, never scored as pass or fail.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))
from checks import run_checks  # noqa: E402

# Fallback models, used only when a skill's own frontmatter can't be read
# (e.g. a prompt set with no matching skills/<name>/ dir). Update alongside
# MODELS.md. Normal routing reads each skill's own claude:/openai: hint --
# see skill_engine_hint() -- so a "fast" tier skill runs on haiku, not this.
DEFAULT_MODEL = {
    "claude": "claude-sonnet-5",
    "codex": "gpt-5.6-terra",
}

# Env vars that must never leak from the caller's own shell/session into an
# eval subprocess -- they'd silently override the per-skill model/effort
# routing below with whatever tier the CALLER happened to be running at.
_STRIP_ENV = ("CLAUDE_EFFORT",)


def skill_engine_hint(skill_name, agent):
    """Read (model, effort) from skills/<name>/SKILL.md's own frontmatter --
    e.g. `claude: claude-haiku-4-5 (low)` -> ("claude-haiku-4-5", "low").
    Falls back to DEFAULT_MODEL / no effort override if the skill dir or the
    hint line can't be found."""
    skill_md = REPO / "skills" / skill_name / "SKILL.md"
    if not skill_md.exists():
        return DEFAULT_MODEL[agent], None
    fm = skill_md.read_text()
    key = "claude" if agent == "claude" else "openai"
    m = re.search(rf"(?m)^\s*{key}:\s*([\w.-]+)\s*\((\w+)\)", fm)
    if not m:
        return DEFAULT_MODEL[agent], None
    return m.group(1), m.group(2)


def build_cmd(agent, model, prompt, workdir, with_skills, effort=None):
    """Return (cmd_list, env) for one run. Skills are installed into the temp
    workdir (project scope) so each run is isolated; --no-skill omits them.
    `effort` is passed explicitly to the CLI -- never inherited from the
    caller's environment, which is stripped below."""
    env = os.environ.copy()
    for var in _STRIP_ENV:
        env.pop(var, None)
    if agent == "claude":
        if with_skills:
            dest = Path(workdir) / ".claude" / "skills"
            dest.mkdir(parents=True, exist_ok=True)
            for d in (REPO / "skills").iterdir():
                shutil.copytree(d, dest / d.name, dirs_exist_ok=True)
        cmd = ["claude", "-p", prompt, "--output-format", "json",
               "--model", model, "--max-turns", "12"]
        if effort:
            cmd += ["--effort", effort]
    elif agent == "codex":
        if with_skills:
            dest = Path(workdir) / ".codex" / "skills"
            dest.mkdir(parents=True, exist_ok=True)
            for d in (REPO / "skills").iterdir():
                shutil.copytree(d, dest / d.name, dirs_exist_ok=True)
        cmd = ["codex", "exec", "--model", model, "--json",
               "--skip-git-repo-check", prompt]
        # NOTE: codex's reasoning-effort flag is not verified in this
        # environment (no codex CLI installed) -- see AGENTS.md's tier
        # table for the intended low/medium/high/xhigh mapping. Left
        # unset rather than guessing a flag name that could break the call.
    else:
        raise ValueError(f"unknown agent: {agent}")
    return cmd, env


def extract_output(agent, raw):
    """Pull the final response text out of the CLI's JSON output; fall back to raw."""
    try:
        if agent == "claude":
            data = json.loads(raw.strip())
            return data.get("result") or data.get("response") or raw
        # codex --json emits JSONL events; take agent_message items
        msgs = []
        for line in raw.splitlines():
            line = line.strip()
            if not line.startswith("{"):
                continue
            evt = json.loads(line)
            item = evt.get("item") or evt
            if item.get("type") in ("agent_message", "assistant_message", "message"):
                msgs.append(item.get("text") or item.get("content") or "")
        return "\n".join(m for m in msgs if m) or raw
    except (json.JSONDecodeError, AttributeError):
        return raw


def build_judge_cmd(agent, model, output_text, criteria, effort=None):
    """A judge call is a plain one-shot prompt asking a model to grade another
    model's output against a rubric -- no skills installed, no repo context."""
    rubric = "\n".join(f"{i}. {c}" for i, c in enumerate(criteria, 1))
    judge_prompt = (
        "You are grading an AI agent's output against a rubric. For EACH "
        "numbered criterion below, judge whether the output satisfies it. "
        "Reply with exactly one line per criterion, in the form `N: PASS` or "
        "`N: FAIL`, and nothing else -- no explanation, no extra text.\n\n"
        f"Criteria:\n{rubric}\n\n"
        f"Agent output to grade:\n---\n{output_text}\n---"
    )
    if agent == "claude":
        cmd = ["claude", "-p", judge_prompt, "--output-format", "json", "--model", model]
        if effort:
            cmd += ["--effort", effort]
        return cmd
    return ["codex", "exec", "--model", model, "--json", "--skip-git-repo-check", judge_prompt]


def run_judge(agent, model, output_text, criteria, timeout, effort=None):
    """Returns {criterion_text: bool}. Fails closed (all False) on any judge
    error -- a broken judge call must never silently pass a case."""
    if not criteria:
        return {}
    cmd = build_judge_cmd(agent, model, output_text, criteria, effort)
    env = os.environ.copy()
    for var in _STRIP_ENV:
        env.pop(var, None)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env)
        if r.returncode != 0:
            return {c: False for c in criteria}
        verdict_text = extract_output(agent, r.stdout)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return {c: False for c in criteria}
    results = {}
    for i, c in enumerate(criteria, 1):
        m = re.search(rf"(?m)^\s*{i}[.:]\s*(PASS|FAIL)", verdict_text, re.I)
        results[c] = bool(m and m.group(1).upper() == "PASS")
    return results


def run_case(agent, model, case, markers, with_skills, timeout, judge, judge_model,
             effort=None, judge_effort=None):
    with tempfile.TemporaryDirectory(prefix="skill-eval-") as workdir:
        cmd, env = build_cmd(agent, model, case["prompt"], workdir, with_skills, effort)
        try:
            r = subprocess.run(cmd, capture_output=True, text=True,
                               timeout=timeout, cwd=workdir, env=env)
        except subprocess.TimeoutExpired:
            return {"error": "timeout", "triggered": None, "checks": {}, "judge": None}
        except FileNotFoundError:
            return {"error": f"{agent} CLI not found on PATH", "triggered": None,
                    "checks": {}, "judge": None}
        if r.returncode != 0:
            # A nonzero exit means the CLI itself failed (crash, auth error,
            # bad flags) -- never infer pass/fail from garbage/partial stdout.
            stderr_tail = (r.stderr or "").strip()[:300]
            return {"error": f"nonzero exit ({r.returncode}): {stderr_tail}",
                    "triggered": None, "checks": {}, "judge": None}
        out = extract_output(agent, r.stdout)

    triggered = any(re.search(m, out, re.I | re.S) for m in markers) if markers else None
    judge_results = None
    if judge and case.get("judge_criteria"):
        judge_results = run_judge(agent, judge_model, out, case["judge_criteria"], timeout, judge_effort)
    result = {"error": None, "triggered": triggered,
              "checks": run_checks(case.get("expected_checks", []), out),
              "judge": judge_results,
              "output_len": len(out)}
    return result


def score(case, res):
    """A case passes when trigger expectation matches, all deterministic
    checks pass, and (if judging ran) every judge criterion passes."""
    if res["error"]:
        return False
    ok = True
    if res["triggered"] is not None:
        ok &= (res["triggered"] == case["should_trigger"])
    if case["should_trigger"]:
        ok &= all(res["checks"].values())
        if res.get("judge"):
            ok &= all(res["judge"].values())
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", choices=["claude", "codex"], required=True)
    ap.add_argument("--skill")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--only", help="comma-separated skill names to run, e.g. "
                                    "for re-running just a broken subset")
    ap.add_argument("--trials", type=int, default=3)
    ap.add_argument("--model", help="override: run every skill on this one model "
                                     "instead of each skill's own declared tier")
    ap.add_argument("--effort", help="override: force this effort for every call "
                                      "(only meaningful together with --model)")
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--no-skill", action="store_true",
                    help="run WITHOUT skills installed (retirement test)")
    ap.add_argument("--judge", action="store_true",
                    help="also run LLM-as-judge on cases with judge_criteria "
                         "(extra CLI call per such case -- cost/latency, use selectively)")
    ap.add_argument("--judge-model",
                    help="model for judge calls (default: same tier as the skill under test)")
    args = ap.parse_args()

    if args.only:
        prompt_files = [HERE / "prompts" / f"{s.strip()}.json" for s in args.only.split(",")]
    elif args.all:
        prompt_files = sorted((HERE / "prompts").glob("*.json"))
    else:
        prompt_files = [HERE / "prompts" / f"{args.skill}.json"]

    grand = defaultdict(int)
    for pf in prompt_files:
        if not pf.exists():
            print(f"!! no prompt set: {pf.name}"); continue
        spec = json.loads(pf.read_text())
        markers = spec.get("trigger_markers", [])
        skill = spec["skill"]

        if args.model:
            # Explicit override: same model (and effort, if given) for every
            # call, bypassing each skill's own declared tier entirely.
            model, effort = args.model, args.effort
        else:
            model, effort = skill_engine_hint(skill, args.agent)
        judge_model = args.judge_model or model
        judge_effort = effort

        print(f"\n=== {skill} ({args.agent}/{model}"
              f"{'/' + effort if effort else ''}, "
              f"{args.trials} trials, skills={'off' if args.no_skill else 'on'}, "
              f"judge={'on' if args.judge else 'off'}) ===")
        for case in spec["cases"]:
            passes = 0
            errors = 0
            for _ in range(args.trials):
                res = run_case(args.agent, model, case, markers,
                               not args.no_skill, args.timeout, args.judge, judge_model,
                               effort, judge_effort)
                if res["error"]:
                    errors += 1
                    print(f"  {case['id']}: ERROR {res['error']}")
                passes += score(case, res)
            grand["cases"] += 1
            grand["passed"] += (passes == args.trials)
            grand["errors"] += errors
            print(f"  {case['id']}: {passes}/{args.trials} trials passed"
                  + (f" ({errors} errored)" if errors else ""))
    if grand["cases"]:
        rate = 100.0 * grand["passed"] / grand["cases"]
        err_note = f", {grand['errors']} trial error(s)" if grand["errors"] else ""
        print(f"\nOverall: {grand['passed']}/{grand['cases']} cases fully passing "
              f"({rate:.1f}%{err_note})")
        sys.exit(0 if rate == 100.0 and not grand["errors"] else 1)


if __name__ == "__main__":
    main()
