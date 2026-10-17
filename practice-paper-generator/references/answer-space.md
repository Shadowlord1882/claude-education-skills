# Answer space

A paper that is printed and written on needs room to write. Cramped answer lines make students shrink their writing, skip parts, or run onto the back of the page, and they make the paper hard to mark. Size the space from the marks and the kind of answer, and keep to the rules below.

## How much space

Count a "line" as one ruled line of handwriting (about 8 mm of height). Grade 6–9 handwriting is large, so these figures are deliberately generous.

| Answer type | Space to leave |
| --- | --- |
| Multiple choice | None beyond the options |
| One word, name or number (1 mark) | One short line |
| State / name / give / list (n marks) | n lines |
| Describe / explain / suggest / compare (n marks) | 2 lines per mark, at least 2 |
| Extended answer (5 marks or more) | 2 lines per mark, at least 10 lines |
| Calculation (n marks) | Blank working space of 3 lines per mark, at least 4 lines, then a line `Answer: ____________ (unit)` |
| Completing a table | Cells tall and wide enough to write in; do not shrink them to fit the page |
| Plotting a graph | A printed grid, or an explicit "use graph paper" instruction plus a blank block of about a third of a page |
| Drawing or labelling | A blank box of at least a quarter of a page |
| Experiment design or plan | 10 or more lines |

A question that gives the student a sentence to complete ("The pencil line is drawn above the solvent because ____") needs only enough blank for that phrase.

## Placement rules

- Put the space directly after the part it belongs to, not in a block at the end of a multi-part question.
- Keep a question and its answer space on the same page where the tool allows it; if a question must break, break between parts, not inside the space.
- Scale to the expected answer: if the mark scheme needs three marking points of a sentence each, the space must hold three sentences. Check each written answer against its mark-scheme row.
- Do not try to save pages by trimming space. A 60-minute paper with proper answer space commonly runs 6–10 printed pages, and that is fine.

## Making the space actually appear

Document tools can silently collapse answer lines, which defeats the point. A run of underscore characters on its own line can turn into a single horizontal rule, so a 4-mark answer ends up with one thin line.

- **Doc editors (markdown-based):** produce each answer line as its own rule or ruled paragraph, separated by a blank line so they do not merge, and do this once per line you need. For blank working space and drawing boxes, use a bordered one-cell table of the right height, or enough empty ruled paragraphs.
- **Word (.docx):** use paragraphs with a bottom border or an underscore tab leader at a fixed line height, or a one-cell table with a set minimum row height for boxes.
- **PDF:** draw lines at fixed spacing and keep question and space together.
- **Graph grids:** generate a blank grid (for example with matplotlib or an SVG) when the tool can embed images; otherwise tell students to use graph paper and leave the block.

After building the question paper, read it back or render it and **count the lines for several questions** (a 2-mark explain, a 4-mark explain, a 3-mark calculation, any extended answer) against the table. If the tool rendered fewer lines than intended, fix the construction before delivering rather than noting it.

## Recording it in the blueprint

When writing the blueprint, give each written part an `answer_type` and the number of `lines` you will leave, and `check_blueprint.py` will flag parts that fall short of the table above:

```json
{"id": "B2a", "section": "B", "topic": "Respiratory system", "marks": 3, "type": "short",
 "answer_type": "explain", "lines": 6}
```

Valid `answer_type` values: `mcq`, `word`, `state`, `explain`, `extended`, `calc`, `graph`, `drawing`, `table`. For `graph`, `drawing` and `table` the check only confirms that space was planned (`lines` can be an approximate line-equivalent or omitted).
