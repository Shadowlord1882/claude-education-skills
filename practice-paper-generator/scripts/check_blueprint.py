#!/usr/bin/env python3
"""Check a practice-paper blueprint for marks and topic coverage.

Usage:
    python check_blueprint.py blueprint.json [--floor 0.6]

Blueprint JSON:
{
  "duration_min": 60,
  "total_marks": 50,
  "questions": [
    {"id": "A1", "section": "A", "topic": "Blood", "marks": 1, "type": "mcq", "answer": "C"},
    ...
  ]
}

Reports marks by section and topic, and flags:
  - the total not matching total_marks
  - topics below `floor` x an equal share of the marks
  - multiple-choice answer letters that cluster on one option
  - a duration/marks ratio far from about one mark per 70 seconds
  - written parts (answer_type word/state/explain/extended/calc) whose planned
    `lines` fall short of the answer-space table in references/answer-space.md
Exit status is 1 if any problem is flagged, else 0.
"""
import argparse
import json
import sys
from collections import Counter, defaultdict


WRITTEN_TYPES = {"word", "state", "explain", "extended", "calc"}
PLANNED_ONLY_TYPES = {"graph", "drawing", "table"}


def required_lines(answer_type: str, marks: int) -> int:
    """Minimum ruled lines (or blank working lines) for a written answer."""
    if answer_type == "word":
        return 1
    if answer_type == "state":
        return max(1, marks)
    if answer_type == "explain":
        return max(2, 2 * marks)
    if answer_type == "extended":
        return max(10, 2 * marks)
    if answer_type == "calc":
        return max(4, 3 * marks)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("blueprint")
    parser.add_argument("--floor", type=float, default=0.6,
                        help="minimum share of an equal split a topic must get (default 0.6)")
    args = parser.parse_args()

    with open(args.blueprint, encoding="utf-8") as fh:
        bp = json.load(fh)

    questions = bp.get("questions", [])
    if not questions:
        print("No questions in blueprint.")
        return 1

    problems = []
    by_section = defaultdict(int)
    by_topic = defaultdict(int)
    mcq_answers = []

    for q in questions:
        marks = q.get("marks", 0)
        by_section[q.get("section", "?")] += marks
        by_topic[q.get("topic", "?")] += marks
        if q.get("type") == "mcq" and q.get("answer"):
            mcq_answers.append(str(q["answer"]).strip().upper())

    total = sum(by_section.values())
    declared = bp.get("total_marks")

    print("Marks by section")
    for sec in sorted(by_section):
        print(f"  {sec}: {by_section[sec]}")
    print(f"  Total: {total}" + (f" (declared {declared})" if declared is not None else ""))

    if declared is not None and total != declared:
        problems.append(f"Total marks {total} does not match declared {declared}.")

    duration = bp.get("duration_min")
    if duration and total:
        seconds_per_mark = duration * 60 / total
        print(f"\nTime per mark: {seconds_per_mark:.0f} s (target about 70 s)")
        if not 50 <= seconds_per_mark <= 95:
            problems.append(f"{seconds_per_mark:.0f} s per mark is outside the 50-95 s range; "
                            "the paper is likely too long or too short for the time.")

    print("\nMarks by topic")
    n_topics = len(by_topic)
    equal_share = total / n_topics if n_topics else 0
    floor = args.floor * equal_share
    for topic, marks in sorted(by_topic.items(), key=lambda kv: -kv[1]):
        pct = 100 * marks / total if total else 0
        flag = ""
        if marks < floor:
            flag = "  <-- below floor"
            problems.append(f"Topic '{topic}' has {marks} marks ({pct:.0f}%), "
                            f"below the floor of {floor:.1f} marks.")
        print(f"  {topic}: {marks} ({pct:.0f}%){flag}")

    if len(mcq_answers) >= 5:
        counts = Counter(mcq_answers)
        letter, most = counts.most_common(1)[0]
        print("\nMultiple-choice answer spread: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
        if most / len(mcq_answers) > 0.4:
            problems.append(f"Answer '{letter}' is correct for {most} of {len(mcq_answers)} "
                            "multiple-choice questions; spread the answers out.")

    # Answer-space check for parts that declare an answer_type.
    checked = 0
    for q in questions:
        atype = str(q.get("answer_type", "")).strip().lower()
        if not atype or atype == "mcq":
            continue
        qid = q.get("id", "?")
        marks = q.get("marks", 0)
        if atype in WRITTEN_TYPES:
            checked += 1
            need = required_lines(atype, marks)
            have = q.get("lines")
            if have is None:
                problems.append(f"{qid}: '{atype}' answer worth {marks} marks has no 'lines' planned "
                                f"(needs at least {need}).")
            elif have < need:
                problems.append(f"{qid}: only {have} lines planned for a {marks}-mark '{atype}' answer; "
                                f"needs at least {need}.")
        elif atype in PLANNED_ONLY_TYPES:
            checked += 1
        else:
            problems.append(f"{qid}: unknown answer_type '{atype}'.")
    if checked:
        print(f"\nAnswer space checked for {checked} parts.")
    else:
        print("\nNo answer_type fields given, so answer space was not checked.")

    print()
    if problems:
        print("Problems:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("Blueprint OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
