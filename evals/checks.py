"""Deterministic check registry for ai-workflow skill evals.

Each check is a small function (output_text: str) -> bool, registered by id.
Prompt sets reference checks via "expected_checks". Add new checks here;
keep them regex/section-based and fast. LLM-as-judge (run_judge in
run_evals.py, enabled via --judge) grades a case's optional "judge_criteria"
list and is used selectively, only where a criterion is genuinely qualitative
and a regex would be either too strict or too easy to game.
"""
import re

def _has(pattern, flags=re.I | re.S):
    return lambda out: bool(re.search(pattern, out, flags))

CHECK_REGISTRY = {
    # --- generic ---
    "nonempty_output": lambda out: len(out.strip()) > 0,
    "no_apology_refusal": lambda out: not re.search(r"\b(I cannot|I can't help with that)\b", out),

    # --- roast family ---
    "verdict_line": _has(r"\bVerdict:\s*(GO|RESHAPE|KILL)\b", re.S),
    "single_verdict": lambda out: len(set(re.findall(r"\bVerdict:\s*(GO|RESHAPE|KILL)\b", out))) == 1,
    "cheapest_test": _has(r"cheapest.{0,40}(test|experiment)|de-risk"),
    "persona_sections": _has(r"(Skeptical Customer|Devil's Advocate|Competitor Analyst|The Economist|The Operator|The Builder)"),
    "attack_header": _has(r"##\s*Attack\s*—"),
    "strongest_objection": _has(r"strongest\s+(single\s+)?(objection|argument)"),

    # --- research family ---
    "findings_header": _has(r"##\s*Findings\s*—"),
    "sources_present": _has(r"https?://"),
    "open_questions": _has(r"Open questions:"),
    "briefing_structure": _has(r"Executive summary.*(Key findings).*(Disagreements|uncertainties).*(Implications).*(Source list)"),
    "conflicts_named": _has(r"(conflict|disagree|contradict)"),
    "citations_report": _has(r"Citations:\s*\d+\s*checked,\s*\d+\s*verified"),
    "no_silent_keep": lambda out: not re.search(r"kept (the )?failed citation", out, re.I),

    # --- session bookends ---
    "state_packet": _has(r"(board|git).*(git|board)", re.I | re.S),
    "git_evidence": _has(r"(git log|git status|commit|branch)"),
    "drift_line": _has(r"Drift:"),
    "push_status": _has(r"(push(ed)?|nothing to push|up.to.date|N commits? ready to push)"),
    "routing_dimensions": _has(r"Route:.*(Autonomy|autonomy).*(Plan-first|plan-first)"),
    "candidate_menu": lambda out: len(re.findall(r"Route:", out)) >= 2,
    "three_states": _has(r"(verified).{0,200}(test.pending|tracked debt)"),
    "no_silent_gap": _has(r"silent gap"),
    "land_or_park": _has(r"(land(ed)?|park(ed)?)"),
    "inflight_note_short": lambda out: not re.search(r"(?m)^In-flight note:.{400,}", out),

    # --- build loop ---
    "red_before_green": _has(r"(fail(ing)? test|RED).{0,600}(pass|GREEN)"),
    "tests_pass_line": _has(r"Tests:\s*\d+\s*pass"),
    "mutation_language": _has(r"(mutation|revert(ed)?.{0,60}(red|fail))"),
    "seam_interface": _has(r"(seam|public interface)"),
    "severity_groups": _has(r"(blocker).{0,400}(should-fix|should fix).{0,400}(nit)"),
    "is_it_true": _has(r"is it TRUE"),
    "file_line_refs": _has(r"\w+\.\w{1,4}:\d+"),
    "behaviour_preserving": _has(r"behaviou?r[- ]preserving"),
    "suite_rerun": _has(r"(suite|tests).{0,60}(re-?run|green|pass)"),
    "evidence_artifact": _has(r"(screenshot|output:|byte-match|pasted below|```)"),
    "honesty_spot_check": _has(r"(bad|empty) input"),

    # --- bugs ---
    "verbatim_capture": _has(r"(observed|expected).{0,200}(expected|observed)"),
    "repro_red": _has(r"(repro(duction)?).{0,300}(red|fail)"),
    "no_fix_yet": lambda out: not re.search(r"(applied|landed) (the )?fix", out, re.I),
    "falsifiable_claim": _has(r"(falsifiable|suspected cause)"),
    "probe_flip": _has(r"(probe|toggle).{0,120}(flip|appear|disappear)"),
    "cause_mechanism_order": _has(r"cause.{0,400}mechanism.{0,400}fix.{0,400}regression"),
    "regression_test_first": _has(r"regression test.{0,200}(red|fail).{0,400}(fix|green)"),
    "sibling_sweep": _has(r"sibling"),

    # --- architecture ---
    "ousterhout_vocab": _has(r"(shallow module|deep module|seam)"),
    "ranked_output": _has(r"(rank(ed)?|payoff)"),
    "blast_radius": _has(r"blast radius"),
    "read_only_survey": lambda out: not re.search(r"(I (have )?(refactored|edited|changed) )", out, re.I),

    # --- issues / traceability ---
    "vertical_slices": _has(r"(vertical|end-to-end|tracer)"),
    "dependency_graph": _has(r"(blocked[- ]by|depends on|dependency graph|mermaid)"),
    "traces_field": _has(r"Traces:\s*(FR|NFR|AC|US)-[A-Z]"),
    "id_grammar": _has(r"\b(FR|NFR|AC|US)-[A-Z][A-Z0-9]{1,5}-[0-9]{2,}[a-z]?\b"),
    "fail_loud": _has(r"FAIL"),
    "coverage_line": _has(r"\d+/\d+\s*ACs?\s*verified"),

    # --- glossary / docs / guards ---
    "canonical_term_format": _has(r"_Avoid:_"),
    "adr_shape": _has(r"(decision).{0,200}(context).{0,200}(trade-off|tradeoff)"),
    "replace_not_append": _has(r"(replace|rewrit)"),
    "findings_by_file": _has(r"(stale|redundant|dangling|bloat)"),
    "guard_table": _has(r"(FIRING|DEAD|MISSING)"),
    "red_team_language": _has(r"(bad case|red-team|feed it)"),

    # --- teach ---
    "retrieval_quiz": _has(r"(quiz|retrieval|recall)"),
    "learning_record": _has(r"LEARNING-"),
    "worked_example": _has(r"worked example"),

    # --- prototype / grill ---
    "one_question": _has(r"(design )?question"),
    "throwaway_contract": _has(r"(throwaway|disposable|delete)"),
    "single_question_interview": lambda out: out.count("?") >= 1,
    "playback_summary": _has(r"(what we('| a)re building|NOT building)"),

    # --- skill-eval ---
    "prompt_set_json": _has(r'"should_trigger"'),
    "negative_cases": _has(r"(negative|should not trigger|must not)"),
    "multi_trial": _has(r"(3|three|multiple)[^.]{0,40}trial"),
    "description_first": _has(r"description"),


    # --- adopted skills (v0.3 intake) ---
    "system_map": _has(r"(module|responsibilit|caller)"),
    "no_code_changes": lambda out: not re.search(r"(I (have )?(edited|changed|refactored) )", out, re.I),
    "flake_frequency": _has(r"(flak|frequen|\d+\s*/\s*\d+ runs)"),
    "no_sleep_retry": lambda out: not re.search(r"(added? a (sleep|retry)|time\.sleep\(\d)", out, re.I),
    "root_cause_named": _has(r"(shared .{0,20}state|race|order.depend|unmocked|clock|seed)"),
    "portfolio_statuses": _has(r"(KEEP|PIVOT|RETIRE|KILL|INSUFFICIENT EVIDENCE)"),
    "no_uninstall": lambda out: not re.search(r"I (deleted|uninstalled|removed) the skill", out, re.I),
    "triage_states": _has(r"(needs-triage|needs-info|ready-for-agent|ready-for-human|wontfix)"),
    "ai_disclosure": _has(r"generated by AI during triage"),

    # --- model routing (skills must not run judgment work on cheap models) ---
    "engine_declared": _has(r"Engine:"),
}


def run_checks(check_ids, output_text):
    """Return {check_id: bool}; unknown ids raise KeyError loudly."""
    return {cid: CHECK_REGISTRY[cid](output_text) for cid in check_ids}
