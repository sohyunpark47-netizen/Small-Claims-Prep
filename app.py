import streamlit as st
import streamlit.components.v1 as components
import anthropic
import markdown as md_lib
import os

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Small Claims Prep",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
  }

  .stApp {
    background-color: #FAFAF8;
    color: #1a1a1a;
  }

  h1, h2, h3 {
    font-family: 'DM Serif Display', serif;
    color: #1a1a1a;
  }

  .stage-header {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    color: #1a1a1a;
    margin-bottom: 0.25rem;
  }

  .stage-sub {
    font-size: 0.85rem;
    color: #666;
    margin-bottom: 1.5rem;
    letter-spacing: 0.03em;
    text-transform: uppercase;
  }

  .notice-box {
    background: #F0EDE8;
    border-left: 3px solid #1a1a1a;
    padding: 1rem 1.2rem;
    margin-bottom: 2rem;
    font-size: 0.9rem;
    line-height: 1.6;
    color: #333;
  }

  .progress-bar {
    display: flex;
    gap: 8px;
    margin-bottom: 2rem;
  }

  .progress-step {
    flex: 1;
    height: 3px;
    background: #E0DDD8;
    border-radius: 2px;
  }

  .progress-step.active {
    background: #1a1a1a;
  }

  .progress-step.done {
    background: #666;
  }

  .message-user {
    background: #1a1a1a;
    color: #FAFAF8;
    padding: 0.75rem 1rem;
    border-radius: 12px 12px 2px 12px;
    margin: 0.5rem 0;
    margin-left: 2rem;
    font-size: 0.95rem;
    line-height: 1.5;
  }

  .message-agent {
    background: #EEEAE4;
    color: #1a1a1a;
    padding: 0.75rem 1rem;
    border-radius: 12px 12px 12px 2px;
    margin: 0.5rem 0;
    margin-right: 2rem;
    font-size: 0.95rem;
    line-height: 1.6;
  }

  .input-area {
    margin-top: 1.5rem;
    padding-top: 1rem;
    border-top: 1px solid #E0DDD8;
  }

  .stButton > button {
    border-radius: 2px;
    border: 1px solid #1a1a1a;
    background: #1a1a1a;
    color: #FAFAF8;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    padding: 0.5rem 1.2rem;
    transition: all 0.15s;
  }

  .stButton > button:hover {
    background: #333;
    border-color: #333;
  }

  /* Text area — minimal, word-processor style */
  .stTextArea > div > div > textarea {
    border: 1px solid #D0CCC6;
    border-radius: 2px;
    background: white;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    color: #1a1a1a;
    caret-color: #1a1a1a;
  }

  .stTextArea > div > div > textarea:focus {
    border-color: #1a1a1a;
    box-shadow: none !important;
    outline: none !important;
  }

  /* Suppress all red/orange Streamlit focus rings */
  .stTextArea > div {
    box-shadow: none !important;
  }

  [data-baseweb="textarea"]:focus-within {
    border-color: #1a1a1a !important;
    box-shadow: none !important;
  }

  .stTextArea [data-baseweb="base-input"] {
    border-color: #D0CCC6 !important;
    box-shadow: none !important;
  }

  .stTextArea [data-baseweb="base-input"]:focus-within {
    border-color: #1a1a1a !important;
    box-shadow: none !important;
  }

  footer {display: none;}
  #MainMenu {visibility: hidden;}
  header {visibility: hidden;}

  .footer-note {
    text-align: center;
    color: #999;
    font-size: 0.78rem;
    margin-top: 3rem;
    padding-bottom: 2rem;
  }

  @media print {
    .stButton, .stTextArea, .progress-bar, .stage-header, .stage-sub, .footer-note { display: none; }
  }
</style>
""", unsafe_allow_html=True)

# ── Anthropic client ──────────────────────────────────────────────────────────
def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY", "")
    return anthropic.Anthropic(api_key=api_key)

MODEL = "claude-sonnet-4-6"

# ── Agent system prompts ──────────────────────────────────────────────────────
AGENT1_SYSTEM = """You are a careful, calm fact collector helping someone prepare to speak to a lawyer or legal adviser about a small claims matter in England or Wales.

Your job is to collect the user's story through conversation. Ask clarifying questions one or two at a time — never overwhelm them. Be warm, plain-spoken, and patient.

You must collect ALL of the following before declaring the facts complete:
1. What happened (the core dispute)
2. Key dates (when things happened, deadlines, any correspondence)
3. The amount of money involved
4. What evidence the user has (receipts, emails, photos, contracts, texts)
5. How the user paid (cash, card, credit card, bank transfer, PayPal etc.)

If the user mentions needing contact details for the other party (such as an address or full name), acknowledge that they will need these for any formal claim, but tell them not to enter those details here. Ask them to keep those details noted separately.

Once you have all five points, end your final message with a brief plain-English summary of the facts collected, then on the very last line write exactly:
FACTS COMPLETE

Do not ask any follow-up questions after writing FACTS COMPLETE. Do not ask the user to confirm or add anything. FACTS COMPLETE must be the final line.
Do not give legal opinions. Do not tell the user whether they have a good case."""

AGENT1_SYSTEM_DEFENDANT = """You are a careful, calm fact collector helping someone prepare to speak to a lawyer or legal adviser. The user has received a small claims court claim against them in England or Wales and needs help preparing their defence.

Your job is to collect the full picture through conversation. Ask clarifying questions one or two at a time — never overwhelm them. Be warm, plain-spoken, and patient.

You must collect ALL of the following before declaring the facts complete:
1. What the claimant is alleging happened
2. The user's account of events
3. Key dates (when things happened, any correspondence, service of the claim, response deadline)
4. The amount being claimed
5. What evidence the user has to support their position (receipts, emails, photos, contracts, texts)
6. Any prior attempts to resolve the dispute

If the user mentions needing contact details for the other party, acknowledge that they will need these for any formal response, but tell them not to enter those details here. Ask them to keep those details noted separately.

Once you have all points, end your final message with a brief plain-English summary of the facts collected, then on the very last line write exactly:
FACTS COMPLETE

Do not ask any follow-up questions after writing FACTS COMPLETE. Do not ask the user to confirm or add anything. FACTS COMPLETE must be the final line.
Do not give legal opinions. Do not tell the user whether they have a good defence."""

AGENT2_SYSTEM = """You are a legal information assistant helping someone prepare to speak to a lawyer or legal adviser about a small claims matter in England or Wales.

You will receive a structured summary of facts from an earlier stage. Your job is to:
1. Identify the most likely relevant legal basis in plain English — this may include Consumer Rights Act 2015, Consumer Contracts Regulations 2013, Supply of Goods and Services Act 1982, or other relevant UK law depending on the facts
2. If the user paid by credit card and the amount is between £100 and £30,000, flag the Section 75 option under the Consumer Credit Act 1974 clearly
3. Produce a short, plain-English legal summary (3-5 paragraphs)

Do NOT use markdown headers like ## or # in your response. Use plain text with clear paragraph breaks.
Frame everything as information to discuss with a legal adviser, not as legal advice. Do not tell the user they have a strong or weak case. Do not recommend a specific course of action."""

AGENT2_SYSTEM_DEFENDANT = """You are a legal information assistant helping someone prepare to speak to a lawyer or legal adviser about a small claims defence in England or Wales.

You will receive a structured summary of facts from an earlier stage. Your job is to:
1. Identify the most likely relevant legal defences or counter-arguments in plain English
2. Note any procedural points (limitation periods, proper service, pre-action protocol compliance, response deadline)
3. Produce a short, plain-English legal summary (3-5 paragraphs) covering what the claimant would need to prove and what the defendant might rely on

Do NOT use markdown headers like ## or # in your response. Use plain text with clear paragraph breaks.
Frame everything as information to discuss with a legal adviser, not as legal advice. Do not tell the user they have a strong or weak defence."""

AGENT3_SYSTEM = """You are helping someone prepare for a small claims hearing in England or Wales by stress-testing their case. You play the role of a probing district judge or the opposing party's representative.

You will receive the user's facts and a legal analysis. Your job is to ask the hard questions — the ones that expose weaknesses, gaps in evidence, inconsistencies, or assumptions.

CRITICAL RULES:
- Never ask for anyone's name, address, or any personal identifier. Refer to people by their role only: "the seller", "the contractor", "the cardholder", "you", "the other party".
- Ask one question at a time
- After each answer, briefly coach the user on how to strengthen their response or what to be careful about
- Be direct but not hostile — you are helping them prepare, not attacking them
- Run for AT LEAST five questions before you may end the cross-examination
- After at least five complete exchanges, you may end by writing exactly: CROSS EXAMINATION COMPLETE

Do not give legal advice. Focus on the facts and the user's ability to present them clearly."""

AGENT3_SYSTEM_DEFENDANT = """You are helping someone prepare their small claims defence in England or Wales by stress-testing their position. You play the role of a probing district judge or the claimant's representative.

You will receive the defendant's facts and a legal analysis. Your job is to ask the hard questions — the ones that expose weaknesses, gaps in evidence, inconsistencies, or assumptions in the defence.

CRITICAL RULES:
- Never ask for anyone's name, address, or any personal identifier. Refer to people by their role only: "the claimant", "you", "the other party".
- Ask one question at a time
- After each answer, briefly coach the user on how to strengthen their response or what to be careful about
- Be direct but not hostile — you are helping them prepare, not attacking them
- Run for AT LEAST five questions before you may end the cross-examination
- After at least five complete exchanges, you may end by writing exactly: CROSS EXAMINATION COMPLETE

Do not give legal advice. Focus on the facts and the user's ability to present them clearly."""

AGENT4_SYSTEM = """You are producing a preparation summary for someone about to speak to a lawyer, legal adviser, or support service about a small claims matter in England or Wales.

You will receive: the user's facts, a legal analysis, and notes from a cross-examination preparation session.

Produce a clean one-page preparation summary containing:
1. What happened — in three sentences maximum
2. Chronology — key dates and evidence in a simple table
3. Legal basis — in plain English, no jargon
4. Amount being claimed
5. Key questions and prepared answers — at least three, drawn from the cross-examination
6. Things to bring or action before your appointment — a checklist

Format with clear section headings. This is preparation material for a conversation with a legal adviser, not a court document. Write it so a stressed, non-legally-trained person can pick it up, read it in two minutes, and feel more prepared.

Do not include legal advice. Do not recommend a specific outcome."""

AGENT4_SYSTEM_DEFENDANT = """You are producing a preparation summary for someone about to speak to a lawyer, legal adviser, or support service about defending a small claims matter in England or Wales.

You will receive: the defendant's facts, a legal analysis, and notes from a cross-examination preparation session.

Produce a clean one-page preparation summary containing:
1. The claim against them — in two sentences maximum
2. Their account — in two sentences maximum
3. Chronology — key dates and evidence in a simple table
4. Legal basis — relevant defences and what the claimant must prove, in plain English
5. Amount being claimed
6. Key questions and prepared answers — at least three, drawn from the cross-examination
7. Things to bring or action before your appointment — a checklist including the response deadline

Format with clear section headings. This is preparation material for a conversation with a legal adviser, not a court document.

Do not include legal advice. Do not recommend a specific outcome."""

# ── Session state init ────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "stage": "welcome",
        "mode": None,
        "messages_1": [],
        "facts_summary": "",
        "legal_summary": "",
        "messages_3": [],
        "final_summary": "",
        "cross_count": 0,
        "input_key_1": 0,
        "input_key_3": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── Helpers ───────────────────────────────────────────────────────────────────
def call_claude(system_prompt, messages):
    client = get_client()
    resp = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        system=system_prompt,
        messages=messages
    )
    return resp.content[0].text

def progress_html(stage):
    order = {"welcome": -1, "agent1": 0, "agent2": 1, "agent3": 2, "agent4": 3}
    current = order.get(stage, -1)
    bars = ""
    for i in range(4):
        if i < current:
            cls = "done"
        elif i == current:
            cls = "active"
        else:
            cls = ""
        bars += f'<div class="progress-step {cls}"></div>'
    return f'<div class="progress-bar">{bars}</div>'

def render_messages(messages):
    for m in messages:
        if m["role"] == "user":
            st.markdown(f'<div class="message-user">{m["content"]}</div>', unsafe_allow_html=True)
        else:
            content = m["content"]
            content = content.replace("FACTS COMPLETE", "").replace("CROSS EXAMINATION COMPLETE", "").strip()
            if content:
                st.markdown(f'<div class="message-agent">{content}</div>', unsafe_allow_html=True)

def render_input(key_suffix, input_key, placeholder="Type here..."):
    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    user_input = st.text_area(
        "Your response",
        key=f"input_{key_suffix}_{input_key}",
        height=100,
        placeholder=placeholder,
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    return user_input

def render_footer():
    st.markdown(
        '<div class="footer-note">This tool covers the law of England and Wales only. '
        'It does not apply to Scotland, Northern Ireland, or any other jurisdiction. '
        '<a href="/Privacy_Policy" style="color:#999;">Privacy Policy</a></div>',
        unsafe_allow_html=True
    )

def render_print_pdf(summary_text):
    summary_html = md_lib.markdown(summary_text, extensions=["tables"])
    print_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');
  body {{
    font-family: 'DM Sans', sans-serif;
    font-size: 11pt;
    color: #1a1a1a;
    max-width: 680px;
    margin: 2rem auto;
    line-height: 1.6;
  }}
  h1, h2, h3, h4 {{
    font-family: 'DM Serif Display', serif;
    margin-top: 1.4rem;
    margin-bottom: 0.4rem;
  }}
  h1 {{ font-size: 1.5rem; }}
  h2 {{ font-size: 1.2rem; border-bottom: 1px solid #ccc; padding-bottom: 0.2rem; }}
  h3 {{ font-size: 1rem; }}
  ul, ol {{ padding-left: 1.4rem; }}
  li {{ margin-bottom: 0.3rem; }}
  table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: 10pt; }}
  th {{ text-align: left; border-bottom: 2px solid #1a1a1a; padding: 0.4rem 0.6rem; font-weight: 500; }}
  td {{ border-bottom: 1px solid #ddd; padding: 0.4rem 0.6rem; vertical-align: top; }}
  strong {{ font-weight: 500; }}
  .notice {{
    border-left: 3px solid #1a1a1a;
    padding: 0.6rem 0.8rem;
    background: #f5f3ef;
    font-size: 9pt;
    margin-top: 1.5rem;
    color: #444;
  }}
  .doc-footer {{
    font-size: 8pt;
    color: #999;
    text-align: center;
    margin-top: 2rem;
    border-top: 1px solid #eee;
    padding-top: 0.6rem;
  }}
  @media print {{
    body {{ margin: 1cm; max-width: 100%; }}
  }}
</style>
</head>
<body>
{summary_html}
<div class="notice">
  This summary is preparation material only. It is not legal advice and should not be used as a court document.
  Bring it to your appointment with a lawyer, legal adviser, or support service such as Citizens Advice.
</div>
<div class="doc-footer">
  Small Claims Prep — England and Wales only — smallclaims.streamlit.app
</div>
<script>
  window.onload = function() {{ window.print(); }}
</script>
</body>
</html>"""
    components.html(print_html, height=0, scrolling=False)
    st.info("Your browser's print dialog should have opened. Select 'Save as PDF' to save a copy.")

# ── WELCOME ───────────────────────────────────────────────────────────────────
if st.session_state.stage == "welcome":
    st.markdown('<h1 style="margin-bottom:0.25rem;">Small Claims Prep</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#666; margin-bottom:2rem;">Prepare for your conversation with a lawyer or legal adviser</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="notice-box">
    <strong>Before you start:</strong> do not enter full names, addresses, or other identifying personal details.
    Describe your situation in general terms. This tool is designed to help you prepare for a conversation
    with a lawyer or legal adviser — it does not provide legal advice.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Are you making a claim or defending one?**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("I'm making a claim", use_container_width=True):
            st.session_state.mode = "claimant"
            st.session_state.stage = "agent1"
            st.rerun()
    with col2:
        if st.button("I've received a claim", use_container_width=True):
            st.session_state.mode = "defendant"
            st.session_state.stage = "agent1"
            st.rerun()
    render_footer()

# ── AGENT 1: FACT COLLECTOR ───────────────────────────────────────────────────
elif st.session_state.stage == "agent1":
    st.markdown(progress_html("agent1"), unsafe_allow_html=True)
    st.markdown('<div class="stage-header">Building Your Case</div>', unsafe_allow_html=True)
    st.markdown('<div class="stage-sub">Stage 1 of 4 — Fact Collection</div>', unsafe_allow_html=True)

    system = AGENT1_SYSTEM if st.session_state.mode == "claimant" else AGENT1_SYSTEM_DEFENDANT

    if not st.session_state.messages_1:
        opening = "I'm here to help you prepare. Tell me what happened — in your own words, as much or as little as you like to start."
        st.session_state.messages_1 = [{"role": "assistant", "content": opening}]

    render_messages(st.session_state.messages_1)

    facts_done = any(
        "FACTS COMPLETE" in m["content"]
        for m in st.session_state.messages_1
        if m["role"] == "assistant"
    )

    if facts_done:
        if st.button("Continue to Legal Analysis →"):
            with st.spinner("Summarising your case..."):
                convo_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages_1])
                summary_prompt = f"Summarise the following fact-collection conversation into a structured summary covering: what happened, key dates, amount involved, evidence available, and payment method.\n\n{convo_text}"
                summary = call_claude("You produce structured factual summaries. Be concise and factual.", [{"role": "user", "content": summary_prompt}])
            st.session_state.facts_summary = summary
            st.session_state.messages_1 = []
            st.session_state.stage = "agent2"
            st.rerun()
    else:
        user_input = render_input("1", st.session_state.input_key_1, "Type here...")
        if st.button("Send", key="send_1") and user_input.strip():
            st.session_state.input_key_1 += 1
            st.session_state.messages_1.append({"role": "user", "content": user_input.strip()})
            api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages_1]
            with st.spinner("Thinking..."):
                response = call_claude(system, api_messages)
            st.session_state.messages_1.append({"role": "assistant", "content": response})
            st.rerun()

    render_footer()

# ── AGENT 2: LEGAL ANALYST ────────────────────────────────────────────────────
elif st.session_state.stage == "agent2":
    st.markdown(progress_html("agent2"), unsafe_allow_html=True)
    st.markdown('<div class="stage-header">Legal Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="stage-sub">Stage 2 of 4 — Identifying the Legal Basis</div>', unsafe_allow_html=True)

    if not st.session_state.legal_summary:
        with st.spinner("Analysing your situation..."):
            system = AGENT2_SYSTEM if st.session_state.mode == "claimant" else AGENT2_SYSTEM_DEFENDANT
            legal = call_claude(system, [{"role": "user", "content": st.session_state.facts_summary}])
            st.session_state.legal_summary = legal

    st.markdown(st.session_state.legal_summary)

    st.markdown("""
    <div class="notice-box" style="margin-top:1.5rem;">
    This is legal information, not legal advice. Discuss these points with a lawyer, legal adviser, or support service before taking action.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Facts"):
            st.session_state.stage = "agent1"
            st.session_state.legal_summary = ""
            st.rerun()
    with col2:
        if st.button("Continue to Preparation →"):
            st.session_state.stage = "agent3"
            st.rerun()

    render_footer()

# ── AGENT 3: CROSS EXAMINER ───────────────────────────────────────────────────
elif st.session_state.stage == "agent3":
    st.markdown(progress_html("agent3"), unsafe_allow_html=True)
    st.markdown('<div class="stage-header">Preparing You For Court</div>', unsafe_allow_html=True)
    st.markdown('<div class="stage-sub">Stage 3 of 4 — Cross-Examination Practice</div>', unsafe_allow_html=True)

    system = AGENT3_SYSTEM if st.session_state.mode == "claimant" else AGENT3_SYSTEM_DEFENDANT

    if not st.session_state.messages_3:
        context = f"FACTS:\n{st.session_state.facts_summary}\n\nLEGAL ANALYSIS:\n{st.session_state.legal_summary}"
        opening_prompt = f"Here are the facts and legal analysis. Begin the cross-examination.\n\n{context}"
        with st.spinner("Preparing questions..."):
            opening = call_claude(system, [{"role": "user", "content": opening_prompt}])
        st.session_state.messages_3 = [
            {"role": "user", "content": opening_prompt},
            {"role": "assistant", "content": opening}
        ]

    display_msgs = [m for m in st.session_state.messages_3 if not m["content"].startswith("Here are the facts")]
    render_messages(display_msgs)

    cross_done = any(
        "CROSS EXAMINATION COMPLETE" in m["content"]
        for m in st.session_state.messages_3
        if m["role"] == "assistant"
    )

    if cross_done:
        st.markdown('<div class="message-agent">Good work. You\'ve been through the key questions. Let\'s put together your summary.</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back to Legal Analysis"):
                st.session_state.stage = "agent2"
                st.rerun()
        with col2:
            if st.button("Generate My Summary →"):
                st.session_state.stage = "agent4"
                st.rerun()
    else:
        user_input = render_input("3", st.session_state.input_key_3, "Answer the question above...")
        if st.button("Send", key="send_3") and user_input.strip():
            st.session_state.input_key_3 += 1
            st.session_state.cross_count += 1
            st.session_state.messages_3.append({"role": "user", "content": user_input.strip()})
            api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages_3]
            with st.spinner("Thinking..."):
                response = call_claude(system, api_messages)
            st.session_state.messages_3.append({"role": "assistant", "content": response})
            st.rerun()

        if st.button("← Back to Legal Analysis", key="back_3"):
            st.session_state.stage = "agent2"
            st.rerun()

    render_footer()

# ── AGENT 4: SUMMARY WRITER ───────────────────────────────────────────────────
elif st.session_state.stage == "agent4":
    st.markdown(progress_html("agent4"), unsafe_allow_html=True)
    st.markdown('<div class="stage-header">Your Case Summary</div>', unsafe_allow_html=True)
    st.markdown('<div class="stage-sub">Stage 4 of 4 — Preparation Summary</div>', unsafe_allow_html=True)

    if not st.session_state.final_summary:
        cross_text = "\n".join([
            f"{m['role'].upper()}: {m['content']}"
            for m in st.session_state.messages_3
            if not m["content"].startswith("Here are the facts")
        ])
        full_context = f"FACTS:\n{st.session_state.facts_summary}\n\nLEGAL ANALYSIS:\n{st.session_state.legal_summary}\n\nCROSS-EXAMINATION NOTES:\n{cross_text}"

        with st.spinner("Writing your summary..."):
            system = AGENT4_SYSTEM if st.session_state.mode == "claimant" else AGENT4_SYSTEM_DEFENDANT
            summary = call_claude(system, [{"role": "user", "content": full_context}])
            st.session_state.final_summary = summary

    st.markdown(st.session_state.final_summary)

    st.markdown("""
    <div class="notice-box" style="margin-top:1.5rem;">
    This summary is preparation material only. It is not legal advice and should not be used as a court document.
    Bring it to your appointment with a lawyer, legal adviser, or support service such as Citizens Advice.
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Back to Preparation"):
            st.session_state.stage = "agent3"
            st.session_state.final_summary = ""
            st.rerun()
    with col2:
        show_print = st.button("🖨 Print / Save as PDF")
    with col3:
        if st.button("Start Again"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    if show_print:
        render_print_pdf(st.session_state.final_summary)

    render_footer()
