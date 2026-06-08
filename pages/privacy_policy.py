import streamlit as st

st.set_page_config(
    page_title="Privacy Policy — Small Claims Prep",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');
  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
  .stApp { background-color: #FAFAF8; color: #1a1a1a; }
  h1, h2, h3 { font-family: 'DM Serif Display', serif; color: #1a1a1a; }
  footer {display: none;}
  #MainMenu {visibility: hidden;}
  header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("# Privacy Policy")
st.markdown("*Last updated: June 2026*")

st.markdown("""
## What this tool does

Small Claims Prep is a preparation tool designed to help people in England and Wales get ready for a conversation with a lawyer, legal adviser, or support service. It does not provide legal advice.

## What data we collect

This tool does not collect, store, or retain any personal data.

The information you type into the tool is sent to the Anthropic Claude API to generate responses. It is processed in real time and is not stored by this application after your session ends. When you close or refresh the page, your session data is permanently lost.

We do not use cookies, analytics, or tracking tools.

## What we ask you not to enter

Before you begin, the tool asks you not to enter full names, addresses, phone numbers, or other identifying personal details. This is both a privacy precaution and a practical one — the tool is designed to work with general descriptions of your situation, not personally identifying information.

## Third-party processing

Your inputs are processed by the Anthropic Claude API. Anthropic's privacy policy applies to that processing and can be found at [anthropic.com/privacy](https://www.anthropic.com/privacy).

This tool is hosted on Streamlit Community Cloud. Streamlit's privacy policy applies to hosting and can be found at [streamlit.io/privacy-policy](https://streamlit.io/privacy-policy).

## Your rights

Because this tool does not store personal data, there is no data held about you to access, correct, or delete.

If you have questions about this privacy policy, you can contact us at the email address listed on the GitHub repository for this project.

## Changes to this policy

This policy may be updated from time to time. The date at the top of this page reflects the most recent revision.
""")

st.markdown("---")
st.markdown(
    '<p style="text-align:center; color:#999; font-size:0.78rem;">This tool covers the law of England and Wales only. '
    'It does not apply to Scotland, Northern Ireland, or any other jurisdiction.</p>',
    unsafe_allow_html=True
)