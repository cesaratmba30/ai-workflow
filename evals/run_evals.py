#!/usr/bin/env python3
"""Eval runner for ai-workflow skills. Works with the claude and codex CLIs.

Usage:
  python evals/run_evals.py --agent claude --skill roast --trials 3
  python evals/run_evals.py --agent codex  --skill roast --trials 3
  python evals/run_evals.py --agent claude --all
  python evals/run_evals.py --agent claude --skill tdd --no-skill   # retirement test

Design (per Schmid): isolated temp workspace per case (no context bleed),
multiple trials (nondeterminism), deterministic checks from checks.py,
marker-based trigger detection, outcome-graded not path-graded.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))
from checks import run_checks  # noqa: E402

# Default models per tier; override with --model. Update alongside MODELS.md.
DEFAULT_MODEL = {
    "claude": "claude-sonnet-5",
    "codex": "gpt-5.6-terra",
}


def build_cmd(agent, model, prompt, workdir, with_skills):
    """Return (cmd_list, env) for one run. Skills are installed into the temp
    workdir (project scope) so each run is isolated; --no-skill omits them."""
    env = os.environ.copy()
    if agent == "claude":
        if with_skills:
            dest = Path(workdir) / ".claude" / "skills"
            dest.mkdir(parents=True, exist_ok=True)
            for d in (REPO / "skills").iterdir():
                shutil.copytree(d, dest / d.name, dirs_exist_ok=True)
        cmd = ["claude", "-p", prompt, "--output-format", "json",
               "--model", model, "--max-turns", "12"]
    elif agent == "codex":
        if with_skills:
            dest = Path(workdir) / ".codex" / "skills"
            dest.mkdir(parents=True, exist_ok=True)
            for d in (REPO / "skills").iterdir():
                shutil.copytree(d, dest / d.name, dirs_exist_ok=True)
        cmd = ["codex", "exec", "--model", model, "--json",
               "--skip-git-repo-check", prompt]
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


def run_case(agent, model, case, markers, with_skills, timeout):
    with tempfile.TemporaryDirectory(prefix="skill-eval-") as workdir:
        cmd, env = build_cmd(agent, model, case["prompt"], workdir, with_skills)
        try:
            r = subprocess.run(cmd, capture_output=True, text=True,
                               timeout=timeout, cwd=workdir, env=env)
            out = extract_output(agent, r.stdout)
        except subprocess.TimeoutExpired:
            return {"error": "timeout", "triggered": None, "checks": {}}
        except FileNotFoundError:
            return {"error": f"{agent} CLI not found on PATH", "triggered": None, "checks": {}}

    triggered = any(re.search(m, out, re.I | re.S) for m in markers) if markers else None
    result = {"error": None, "triggered": triggered,
              "checks": run_checks(case.get("expected_checks", []), out),
              "output_len": len(out)}
    return result


def score(case, res):
    """A case passes when trigger expectation matches and all checks pass."""
    if res["error"]:
        return False
    ok = True
    if res["triggered"] is not None:
        ok &= (res["triggered"] == case["should_trigger"])
    if case["should_trigger"]:
        ok &= all(res["checks"].values())
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", choices=["claude", "codex"], required=True)
    ap.add_argument("--skill")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--trials", type=int, default=3)
    ap.add_argument("--model")
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--no-skill", action="store_true",
                    help="run WITHOUT skills installed (retirement test)")
    args = ap.parse_args()

    model = args.model or DEFAULT_MODEL[args.agent]
    prompt_files = sorted((HERE / "prompts").glob("*.json")) if args.all else \
        [HERE / "prompts" / f"{args.skill}.json"]

    grand = defaultdict(int)
    for pf in prompt_files:
        if not pf.exists():
            print(f"!! no prompt set: {pf.name}"); continue
        spec = json.loads(pf.read_text())
        markers = spec.get("trigger_markers", [])
        print(f"\n=== {spec['skill']} ({args.agent}/{model}, "
              f"{args.trials} trials, skills={'off' if args.no_skill else 'on'}) ===")
        for case in spec["cases"]:
            passes = 0
            for _ in range(args.trials):
                res = run_case(args.agent, model, case, markers,
                               not args.no_skill, args.timeout)
                if res["error"]:
                    print(f"  {case['id']}: ERROR {res['error']}")
                passes += score(case, res)
            grand["cases"] += 1
            grand["passed"] += (passes == args.trials)
            print(f"  {case['id']}: {passes}/{args.trials} trials passed")
    if grand["cases"]:
        rate = 100.0 * grand["passed"] / grand["cases"]
        print(f"\nOverall: {grand['passed']}/{grand['cases']} cases fully passing "
              f"({rate:.1f}%)")
        sys.exit(0 if rate == 100.0 else 1)


if __name__ == "__main__":
    main()
