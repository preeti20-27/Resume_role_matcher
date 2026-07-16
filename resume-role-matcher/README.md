# Resume Role Matcher

A tool that reads a PDF resume, extracts the candidate's name, email, and
skills, and scores how well they match a set of predefined job roles.

## What it does

Given a resume PDF, it:
1. Extracts raw text (PyMuPDF)
2. Cleans and tokenizes the text (regex + spaCy lemmatization)
3. Extracts the candidate's name and email
4. Checks which known skills appear in the resume
5. Scores the resume against each job role as a percentage match, based on
   how many of that role's required skills were found

## Example output

```
Name: John Doe
Email: johndoe@example.com
Skills Found: ['Java', 'NLP', 'Python', 'Machine Learning', 'C++']
Role Match Scores: {'Data Analyst': '25.0% match', 'Machine Learning Engineer': '75.0% match', 'Software Developer': '66.67% match'}
```

## How I built this

I built this using Claude to generate the core pipeline — PDF text
extraction, cleaning/tokenization, and the skill-matching logic. I accepted
most of the generated code as-is, since the functions were doing
straightforward, well-defined tasks (regex extraction, dictionary lookups)
where there wasn't much reason to rewrite from scratch. On top of that, I
adjusted the skill list and job role definitions to match what I actually
wanted the tool to screen for, and consolidated several rounds of iteration
(there were multiple versions written while I was testing different
approaches to cleaning/tokenizing) into the single pipeline in
`resume_matcher.py`.

## Known limitations

- **Name extraction is naive** — it assumes the first line of the resume
  text is the candidate's name, which breaks on resumes with a header,
  logo, or different layout above the name.
- **Skill matching is exact-substring, not semantic** — "ML" won't match
  "Machine Learning" unless both are explicitly listed as separate skills.
  A stronger version would use embeddings (see my
  [semantic search project](https://github.com/preeti20-27/-semantic-search-system)
  for that approach).
- **Job roles and skills are hardcoded** — for a real tool, these would
  come from a database or be user-configurable.

## Running it

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python resume_matcher.py
```

Drop your own resume PDF in the project folder and change the
`resume_path` in the `if __name__ == "__main__":` block to match.
