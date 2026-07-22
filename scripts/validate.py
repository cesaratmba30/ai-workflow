#!/usr/bin/env python3
"""Repo self-check: frontmatter, metadata, eval wiring, compose links, coverage."""
import json, re, sys
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "evals"))
from checks import CHECK_REGISTRY

V02 = ["code-review-pass","codebase-design","diagnosing-bugs","doc-audit","domain-modeling",
"grill","handoff","harness-audit","improve-codebase-architecture","prototype","resume",
"roast","simplify","storm-research","tdd","teach","to-issues","traceability","verify",
"writing-great-skills","triage","zoom-out","test-stabilizer","skill-portfolio-audit"]
ENGINES={"fast","balanced","deep","frontier"}
CONC={"parallel-fanout","parallel-ok","single","single-wait","interactive","orchestrator"}
fails=[]
skills={}
for d in sorted((REPO/"skills").iterdir()):
    p=d/"SKILL.md"; s=p.read_text()
    m=re.match(r"^---\n(.*?)\n---\n",s,re.S)
    if not m: fails.append(f"{d.name}: no frontmatter"); continue
    fm=m.group(1)
    def get(k,src=fm):
        mm=re.search(rf"(?m)^\s*{k}:\s*(.+)$",src); return mm.group(1).strip() if mm else None
    name=get("name"); desc=get("description")
    if name!=d.name: fails.append(f"{d.name}: name mismatch ({name})")
    if not desc or len(desc)<80: fails.append(f"{d.name}: description too short")
    if "Do NOT" not in desc: fails.append(f"{d.name}: no negative trigger in description")
    eng=get("engine"); conc=get("concurrency")
    if eng not in ENGINES: fails.append(f"{d.name}: bad engine {eng}")
    if conc not in CONC: fails.append(f"{d.name}: bad concurrency {conc}")
    for k in ("claude","openai","subagent"):
        if not get(k): fails.append(f"{d.name}: missing {k}")
    if "> **Engine:**" not in s: fails.append(f"{d.name}: no Engine body line")
    if "> **Concurrency:**" not in s: fails.append(f"{d.name}: no Concurrency body line")
    if len(s.splitlines())>500: fails.append(f"{d.name}: over 500 lines")
    comp=re.search(r"composes:\s*\[(.*?)\]",fm)
    skills[d.name]=[c.strip() for c in comp.group(1).split(",")] if comp else []
for n,comps in skills.items():
    for c in comps:
        if c and c not in skills: fails.append(f"{n}: composes unknown skill {c}")
for v in V02:
    if v not in skills: fails.append(f"LOST v0.2 skill: {v}")
# eval wiring
psets={p.stem for p in (REPO/"evals/prompts").glob("*.json")}
for n in skills:
    if n not in psets: fails.append(f"{n}: no prompt set")
for p in (REPO/"evals/prompts").glob("*.json"):
    spec=json.loads(p.read_text())
    if spec["skill"]!=p.stem: fails.append(f"{p.name}: skill field mismatch")
    negs=[c for c in spec["cases"] if not c["should_trigger"]]
    if len(negs)<2: fails.append(f"{p.name}: fewer than 2 negative cases")
    for c in spec["cases"]:
        for cid in c["expected_checks"]:
            if cid not in CHECK_REGISTRY: fails.append(f"{p.name}:{c['id']}: unknown check {cid}")
        if c["should_trigger"] and not c["expected_checks"] and not spec.get("trigger_markers"):
            fails.append(f"{p.name}:{c['id']}: positive case with no checks or markers")
json.loads((REPO/".claude-plugin/plugin.json").read_text())
print(f"skills: {len(skills)}  prompt sets: {len(psets)}  checks: {len(CHECK_REGISTRY)}")
if fails:
    print("FAIL:"); [print(" -",f) for f in fails]; sys.exit(1)
print("ALL CHECKS PASS")
