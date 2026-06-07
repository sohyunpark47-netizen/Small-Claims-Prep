# Small Claims Prep

A four-agent legal triage tool to help people prepare for conversations with lawyers and legal advisers about small claims matters in England and Wales.

**Not legal advice. Preparation tool only.**

---

## What it does

Guides users through four stages:

1. **Building Your Case** — Fact collection via conversation (Agent 1)
2. **Legal Analysis** — Identifies relevant UK law in plain English (Agent 2)
3. **Preparing You For Court** — Cross-examination practice (Agent 3)
4. **Your Case Summary** — Printable one-page prep summary (Agent 4)

Supports both claimant and defendant modes.

---

## Deploy to Streamlit Community Cloud

### 1. Push this repo to GitHub (public)

```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/YOUR_USERNAME/small-claims-prep.git
git push -u origin main
```

### 2. Add your API key as a secret

In Streamlit Community Cloud, go to your app settings → Secrets and add:

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

### 3. Deploy

- Go to share.streamlit.io
- Connect your GitHub account
- Select this repo
- Set main file path to `app.py`
- Deploy

---

## Run locally

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
streamlit run app.py
```

---

## Model

Uses `claude-sonnet-4-20250514` for all four agents.

---

## Liability note

This tool is designed for use upstream of legal advice, not as a replacement for it. All outputs are framed as preparation material. No Letter Before Action is generated.
