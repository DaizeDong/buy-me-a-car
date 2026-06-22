#!/usr/bin/env python3
"""Routing / trigger-conflict assertions for buy-me-a-car skills.

Pure standard library. Run directly:

    python eval/test_routing.py

or under pytest / unittest discovery:

    python -m unittest eval.test_routing

Two guarantees are enforced:

  1. No two skills declare an identical exact trigger phrase
     (case-insensitive, whitespace-trimmed). Overlapping triggers make the
     router ambiguous, so they are a hard error.

  2. Every phrase in the README "## Trigger routing" table routes to its
     expected skill, using the README's stated rule: when a query could
     activate multiple skills, the most narrow + specific (= longest) matching
     trigger wins.

The golden fixture eval/golden/routing.json is the single source of truth for
both the per-skill trigger lists and the README phrase->skill expectations.
"""

import json
import os
import re
import unittest
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
GOLDEN = os.path.join(HERE, "golden", "routing.json")


def load_golden():
    with open(GOLDEN, encoding="utf-8") as fh:
        return json.load(fh)


def norm(phrase):
    return phrase.strip().lower()


def tokens(phrase):
    # Split on non-alphanumeric (ASCII) runs; keep CJK chars as 1-char tokens
    # so Chinese trigger phrases still contribute overlap signal.
    out = []
    for chunk in re.split(r"[^0-9a-z一-鿿]+", norm(phrase)):
        if not chunk:
            continue
        if re.search(r"[一-鿿]", chunk):
            out.extend(list(chunk))
        else:
            out.append(chunk)
    return set(out)


def all_triggers(info):
    """Combined trigger vocabulary for a skill: SKILL.md + README block."""
    return list(info.get("triggers", [])) + list(info.get("readme_triggers", []))


def route(query, skills):
    """Resolve a free-text query to a single skill directory.

    Rule (from README): when a query could activate multiple skills, the most
    narrow + specific trigger wins. Resolution proceeds in two stages:

      1. Substring match: among all triggers that appear verbatim inside the
         (normalized) query, the longest one wins -- longer == more specific.
      2. Token-overlap fallback: README-table phrases are paraphrases of the
         canonical triggers ("help me buy a car" vs "buy me a car"), so when no
         trigger is a literal substring we score each skill by the best
         token-Jaccard between the query and any of its triggers, and the
         highest-scoring skill wins.

    Ties are broken deterministically by skill-dir name. Returns the skill
    directory, or None if nothing matches at all.
    """
    q = norm(query)
    qtok = tokens(query)

    # Stage 1: longest verbatim substring trigger.
    best_sub = None  # (length, skill_dir)
    for skill_dir, info in skills.items():
        for trig in all_triggers(info):
            t = norm(trig)
            if t and t in q:
                cand = (len(t), skill_dir)
                if best_sub is None or cand[0] > best_sub[0] or (
                    cand[0] == best_sub[0] and cand[1] < best_sub[1]
                ):
                    best_sub = cand
    if best_sub is not None:
        return best_sub[1]

    # Stage 2: best token-overlap (Jaccard) across triggers.
    best_tok = None  # (score, skill_dir)
    for skill_dir, info in skills.items():
        for trig in all_triggers(info):
            ttok = tokens(trig)
            if not ttok or not qtok:
                continue
            score = len(qtok & ttok) / len(qtok | ttok)
            if score <= 0:
                continue
            cand = (score, skill_dir)
            if best_tok is None or cand[0] > best_tok[0] or (
                cand[0] == best_tok[0] and cand[1] < best_tok[1]
            ):
                best_tok = cand
    return best_tok[1] if best_tok else None


class TestNoDuplicateTriggers(unittest.TestCase):
    def test_no_two_skills_share_exact_trigger(self):
        skills = load_golden()["skills"]
        owners = defaultdict(set)
        for skill_dir, info in skills.items():
            for trig in all_triggers(info):
                owners[norm(trig)].add(skill_dir)
        dups = {t: sorted(s) for t, s in owners.items() if len(s) > 1}
        self.assertEqual(
            dups,
            {},
            "Identical trigger phrase(s) claimed by multiple skills "
            "(ambiguous routing): "
            + json.dumps(dups, ensure_ascii=False),
        )


class TestSkillsMatchFilesystem(unittest.TestCase):
    def test_every_skill_dir_present_and_has_triggers(self):
        skills = load_golden()["skills"]
        skills_root = os.path.join(REPO, "skills")
        on_disk = {
            d
            for d in os.listdir(skills_root)
            if os.path.isfile(os.path.join(skills_root, d, "SKILL.md"))
        }
        self.assertEqual(
            set(skills),
            on_disk,
            "Golden skill set does not match skills/*/SKILL.md on disk.",
        )
        for skill_dir, info in skills.items():
            self.assertTrue(
                info["triggers"],
                "Skill %r has no parsed triggers." % skill_dir,
            )


class TestReadmeTriggerTable(unittest.TestCase):
    def test_each_phrase_routes_to_expected_skill(self):
        golden = load_golden()
        skills = golden["skills"]
        failures = []
        for row in golden["readme_trigger_table"]:
            phrase, expected = row["phrase"], row["expected"]
            self.assertIn(
                expected,
                skills,
                "Expected skill %r is not a known skill." % expected,
            )
            got = route(phrase, skills)
            if got != expected:
                failures.append(
                    "  %r -> %r (expected %r)" % (phrase, got, expected)
                )
        self.assertEqual(
            failures,
            [],
            "README trigger-table phrases routed to the wrong skill:\n"
            + "\n".join(failures),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
