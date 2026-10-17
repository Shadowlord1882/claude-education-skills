---
name: practice-paper-generator
description: Generate a ready-to-print practice test paper plus a separate mark scheme for any school subject, from a Grade, Subject, Topic and Sub-topics (typed, or read from photos of a textbook contents page or syllabus list). Use this whenever the user asks for a practice paper, mock test, revision test, unit test, question paper, exam-style questions or a test for a class or grade, in any subject (science, maths, English, history, geography, languages, computing and so on) and any board (IGCSE, Cambridge, CBSE, ICSE, IB, state boards), even if they only say "make a test on fractions for grade 6". The default paper is at most 1 hour (50 marks) unless the user sets another duration. Not for marking a student's completed paper or for lesson plans.
---

# Practice Paper Generator

Produce two separate documents: a **question paper** a student can sit, and a **mark scheme** a teacher or parent can mark from. A good paper is only useful if it stays inside the scope the user gave, spreads marks fairly across that scope, and has answers that are actually correct. Most of the steps below exist to protect those three things.

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| Grade | yes | Sets vocabulary, number difficulty and expected depth. |
| Subject | yes | |
| Topic(s) | yes | Chapter or unit names. |
| Sub-topics | no | If missing, cover every sub-topic of the named topics as the syllabus or textbook defines them. |
| Duration | no | **Default 60 minutes, never more than 60 unless the user asks for longer.** |
| Board / style | no | Use the board the user names or has used earlier in the conversation. If none, write Cambridge-style questions (command words such as State, Describe, Explain, Calculate, Suggest, Predict). |
| Difficulty | no | Default medium (see the mix below). |

If Grade, Subject or Topic is missing and cannot be read from the conversation or attached photos, ask one short question. Otherwise start; do not interview the user.

### Reading scope from photos

Users often photograph a textbook contents page and a handwritten list of chapters.

- Transcribe the scope into one line for yourself and state it back in your final reply, so a misreading is caught early.
- Handwritten numbering often disagrees with the printed book (for example a list numbered 1–9 against a book numbered 1–12). Treat the printed chapter titles as the truth, map the handwritten items onto them, and mention the mapping if there was any doubt. If a mapping is genuinely ambiguous, make the most likely reading and flag it in one line; do not stall.
- Tick marks, crossings or notes on a printed contents page are not scope unless the user says so.
- Chapters that are not listed are out of scope, even if they sit between listed chapters.
- Use the book only for scope and terminology. Write original questions; never copy exercises from it.

## Workflow

### 1. Build a blueprint before writing any question

Decide the structure first, because fixing balance after the questions are written is slow and error-prone.

**Marks from time.** Use roughly one mark per 70 seconds:

| Duration | Total marks |
| --- | --- |
| 30 min | 25 |
| 45 min | 40 |
| 60 min (default) | 50 |
| 90 min | 80 |
| 120 min | 100 |

**Default 60-minute science-style structure (50 marks).** Adapt per subject using `references/subject-adaptations.md`.

| Section | Type | Marks |
| --- | --- | --- |
| A | Multiple choice, 1 mark each | 10 |
| B | Short-answer theory | 14 |
| C | Calculations (only where the subject has quantitative content; otherwise more of D) | 8 |
| D | Data analysis and experiments | 18 |

Always include the data/experiment section where the subject allows it. Users ask for "data and experiments in addition to theory and calculations", and these questions test skills (variables, graphs, reliability, conclusions) that recall questions do not.

**Medium difficulty mix.** About 30% of marks recall and straightforward, 50% application, 20% analysis or multi-step reasoning. Within each section, order questions from easier to harder so a student builds momentum.

**Topic weighting.** Weight marks by how much teaching each topic carries (number of sub-topics is a good proxy), then apply a floor: no topic should get less than about 60% of an equal share, otherwise it becomes a token question and the paper does not really test it. A topic added or swapped late is the usual victim, so check it.

Write the blueprint as JSON and run the checker:

```json
{
  "duration_min": 60,
  "total_marks": 50,
  "questions": [
    {"id": "A1", "section": "A", "topic": "Blood", "marks": 1, "type": "mcq", "answer": "C"},
    {"id": "B2a", "section": "B", "topic": "Respiratory system", "marks": 3, "type": "short",
     "answer_type": "explain", "lines": 6},
    {"id": "D1c", "section": "D", "topic": "Solubility", "marks": 2, "type": "data",
     "answer_type": "graph"}
  ]
}
```

List written answers part by part and give each an `answer_type` and the `lines` of space you will leave, so the checker can flag cramped space.

```bash
python <skill-dir>/scripts/check_blueprint.py blueprint.json
```

It reports marks by section and by topic, flags topics under the floor, checks the total, warns if multiple-choice answers cluster on one letter, and flags written parts whose planned answer space is too small for their marks. Fix the blueprint until it passes; then write the questions.

### 2. Write the question paper

- **Scope discipline.** Every question must map to a listed topic or sub-topic. If you notice you are drawing on something outside it, replace the question.
- **Original, grade-appropriate.** Use vocabulary a student of that grade has met. Choose clean numbers so calculations finish in a line or two (whole numbers or one decimal place).
- **Self-contained.** Never write "see the diagram" unless the figure is actually included. Prefer tables, described set-ups and short scenarios, which render reliably. If a drawing is truly needed, ask the student to draw it rather than assume it exists.
- **Command words and marks.** Put marks in brackets at the end of each part, and match demand to marks: one mark is one fact, a "Describe" for 3 marks needs three distinct points.
- **Calculations.** For lower grades, list the equations at the top of the section. Ask for units and "show your working".
- **Data and experiment questions.** Give a realistic table of results and ask a progression: identify independent, dependent and control variables, plot or describe the trend, read or estimate a value from a graph, calculate from the data, spot an anomaly or comment on reliability, and draw a conclusion or suggest an improvement. Not every question needs all of these, but across the section each skill should appear at least once. Where the topic has practical work (chromatography, solubility, pulse rate, speed, etc.), base a question on the standard experiment.
- **Multiple choice.** One defensible answer, plausible distractors that reflect real misconceptions, answer letters spread out (no letter more than about 40%).
- **Answer space.** Leave enough room to write, sized from the marks and the kind of answer (roughly 2 ruled lines per mark for explanations, 1 per mark for short statements, 3 blank working lines per mark for calculations, and a printed grid or large block for graphs and drawings). Read `references/answer-space.md` for the full table and for how to make sure the lines really render, because tools can collapse a run of underscores into a single thin rule.
- **Header.** Title, name/class/date line, time, total marks, instructions, a marks-by-section table, and the chapters in scope (see `references/layout.md`).

The question paper must contain no answers, hints that give answers, or marking notes.

### 3. Write the mark scheme

One row per question part: expected answer, marking points with the marks each earns, and the total. Include accepted alternatives ("accept X", "ignore Y"), error-carried-forward for multi-step calculations, and for graph questions the expected shape, key points, and an acceptable reading range. Use method (M) and answer (A) marks for calculations. For multiple choice, a compact answer-key table is enough. Layout is in `references/layout.md`.

### 4. Verify before delivering

Do these as actual checks, not a glance:

1. **Recompute every calculation with code** (a short Python snippet), including values read from data tables. Mental arithmetic is where wrong answer keys come from.
2. **Data consistency.** Tables, graphs and "estimate at X" answers must agree. If a question asks for a value between two data points, make sure the mark-scheme value sits on a sensible curve.
3. **Marks add up**: each question's parts sum to its total, sections sum to the section total, the paper sums to the header total, and the mark scheme matches the question paper row for row.
4. **Scope.** Re-read the list of topics and make sure nothing sits outside it and each topic is represented.
5. **Separation.** Search the question paper for leaked answers.
6. **Answer space.** Read back or render the question paper and count the lines or blank space on a sample of questions (a 2-mark explain, a 4-mark explain, a calculation, any extended answer) against `references/answer-space.md`. If the document tool rendered fewer lines than you intended, fix it before delivering.
7. **Re-run `check_blueprint.py`** against the final paper's actual marks and lines if anything changed while writing.

### 5. Deliver as two separate documents

Make the question paper and the mark scheme as two separate documents, never one combined file, so the paper can be printed without the answers. Name them `<Grade> <Subject> Practice Test: Question Paper` and `... : Mark Scheme`. Use whatever document tooling the session offers (a doc artifact by default, Word or PDF when the user names that format), and follow that tool's own instructions for creating and filling it. Create the question paper first.

Final reply: the links, one line on duration and total marks, the marks by topic in one compact line, and any weakness worth knowing (for example a topic that ended up lightly weighted, or an ambiguous scope mapping). Do not recap the questions or paste the paper into the chat.

## Changing a paper after delivery

When the user changes scope, duration or difficulty, rebuild the blueprint and re-run the checker rather than patching questions one by one, because weights shift. Swapping one chapter for another is the classic case: a one-for-one swap leaves the new chapter with only the marks the old one had, which may be far too few. Then update both documents so they stay in sync (header, chapters line, marks table, mark scheme), and tell the user the new marks by topic.

## Reference files

- `references/subject-adaptations.md`: how the sections change for maths, languages, humanities, computing and others. Read it when the subject is not a science.
- `references/layout.md`: header, question formatting and mark scheme templates. Read it when writing the documents.
- `references/answer-space.md`: how many lines or how much blank space each kind of answer gets, and how to make sure it renders. Read it before writing the question paper.
- `scripts/check_blueprint.py`: blueprint checker described above.
