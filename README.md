# Password Strength Analyzer

A small Streamlit app that evaluates password length, character variety, common passwords, and predictable patterns. Analysis uses local heuristics; passwords are not sent to an external API.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

The score is an estimate, not a breach-database check. Use unique passwords and store them in a password manager.