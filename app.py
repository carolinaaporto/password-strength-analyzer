import re

import streamlit as st


COMMON_PASSWORDS = {
    "123456",
    "123456789",
    "12345678",
    "12345",
    "password",
    "password1",
    "qwerty",
    "qwerty123",
    "abc123",
    "111111",
    "123123",
    "admin",
    "letmein",
    "welcome",
    "iloveyou",
}

SEQUENTIAL_PATTERNS = (
    "012",
    "123",
    "234",
    "345",
    "456",
    "567",
    "678",
    "789",
    "890",
    "abc",
    "bcd",
    "cde",
    "def",
    "efg",
    "fgh",
    "ghi",
    "hij",
    "ijk",
    "jkl",
    "klm",
    "lmn",
    "mno",
    "nop",
    "opq",
    "pqr",
    "qrs",
    "rst",
    "stu",
    "tuv",
    "uvw",
    "vwx",
    "wxy",
    "xyz",
    "qwerty",
    "asdf",
    "zxcv",
)


def analyze_password(password: str) -> dict:
    checks = {
        "At least 12 characters": len(password) >= 12,
        "Uppercase letters": any(char.isupper() for char in password),
        "Lowercase letters": any(char.islower() for char in password),
        "Numbers": any(char.isdigit() for char in password),
        "Symbols": any(not char.isalnum() and not char.isspace() for char in password),
    }

    lowered = password.lower()
    is_common = lowered in COMMON_PASSWORDS
    patterns = [pattern for pattern in SEQUENTIAL_PATTERNS if pattern in lowered]
    has_repeated_chars = re.search(r"(.)\1{2,}", password) is not None
    has_year = re.search(r"(?:19|20)\d{2}", password) is not None

    score = sum(checks.values()) * 10
    score += min(max(len(password) - 8, 0) * 2, 20)
    if is_common:
        score -= 50
    if patterns:
        score -= 15
    if has_repeated_chars:
        score -= 10
    if has_year:
        score -= 5
    score = max(0, min(score, 100))

    if score < 25:
        strength = "Very weak"
    elif score < 50:
        strength = "Weak"
    elif score < 70:
        strength = "Fair"
    elif score < 90:
        strength = "Strong"
    else:
        strength = "Very strong"

    findings = []
    if is_common:
        findings.append("This matches a commonly used password.")
    if patterns:
        findings.append("It contains a predictable sequence or keyboard pattern.")
    if has_repeated_chars:
        findings.append("It repeats the same character several times in a row.")
    if has_year:
        findings.append("It contains a year, which can be easy to guess.")

    tips = []
    if len(password) < 12:
        tips.append("Make it longer: aim for at least 12 characters, or use a longer passphrase.")
    if not checks["Uppercase letters"] or not checks["Lowercase letters"]:
        tips.append("Mix uppercase and lowercase letters.")
    if not checks["Numbers"]:
        tips.append("Add numbers that are not a predictable sequence or date.")
    if not checks["Symbols"]:
        tips.append("Add a symbol in a way that does not form an obvious pattern.")
    if is_common or patterns or has_repeated_chars or has_year:
        tips.append("Avoid common phrases, keyboard runs, repeated characters, and personal dates.")
    tips.append("Use a different password for every account; a password manager can create and store them.")

    return {
        "checks": checks,
        "score": score,
        "strength": strength,
        "findings": findings,
        "tips": tips,
    }


st.set_page_config(page_title="Password Strength Analyzer", layout="wide")

st.markdown(
    """
    <style>
    :root {
        color-scheme: dark;
        --surface: #111815;
        --surface-raised: #171f1b;
        --line: #2a3731;
        --text: #edf2ee;
        --muted: #9aa79f;
        --accent: #a8d7bd;
        --warning: #e5bb7b;
        --grid: rgba(204, 220, 208, .016);
        --trace: rgba(168, 215, 189, .055);
    }
    .stApp {
        background-color: #101512;
        background-image:
            linear-gradient(90deg, var(--grid) 1px, transparent 1px),
            linear-gradient(var(--grid) 1px, transparent 1px),
            repeating-linear-gradient(135deg, transparent 0 132px, var(--trace) 133px 135px, transparent 136px 268px),
            linear-gradient(120deg, rgba(76, 111, 86, .18), transparent 46%, rgba(151, 125, 82, .055)),
            linear-gradient(180deg, #17211b 0, #101512 34rem, #121714 100%);
        background-size: 72px 72px, 72px 72px, 100% 100%, 100% 620px, 100% 100%;
        background-attachment: fixed;
        color: var(--text);
    }
    .stApp::before {
        content: "01  // LOCAL CHECK\\A 02  const length = value.length;\\A 03  const upper = hasUpper(value);\\A 04  const symbol = hasSymbol(value);\\A 05  return score(length, variety);";
        position: fixed;
        top: 16rem;
        right: max(1rem, calc((100vw - 1080px) / 2));
        width: 24rem;
        height: 26rem;
        overflow: hidden;
        color: rgba(168, 215, 189, .25);
        font: 11px/2.3 ui-monospace, SFMono-Regular, Menlo, monospace;
        white-space: pre;
        pointer-events: none;
        user-select: none;
        transform: rotate(-3deg);
        z-index: 0;
    }
    .stApp > header, .stApp [data-testid="stAppViewContainer"] {
        position: relative;
        z-index: 1;
    }
    header[data-testid="stHeader"] { background: transparent; }
    .block-container { max-width: 1080px; padding-top: 2rem; padding-bottom: 2.5rem; }
    h1, h2, h3, p, label { color: var(--text); letter-spacing: 0; }
    h1 { font-size: 2.2rem; font-weight: 650; margin: 1.6rem 0 .45rem; }
    h3 { font-size: 1.05rem; font-weight: 620; }
    .topbar { display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
    .brand { display: flex; align-items: center; gap: .7rem; color: var(--text); font-size: .77rem; font-weight: 700; }
    .brand-symbol { display: grid; place-items: center; width: 1.8rem; height: 1.8rem; border: 1px solid #577565; border-radius: 6px; color: var(--accent); }
    .local-label { display: inline-flex; align-items: center; gap: .45rem; color: var(--muted); font-size: .72rem; }
    .status-dot { width: .42rem; height: .42rem; border-radius: 50%; background: var(--accent); }
    .header-rule { height: 1px; margin-top: 1rem; background: var(--line); }
    .intro { color: var(--muted); margin: 0 0 1.7rem; }
    .section-kicker { color: var(--accent); font-size: .68rem; font-weight: 700; margin-bottom: .5rem; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(23, 31, 27, .82); border: 1px solid var(--line); border-radius: 10px;
    }
    [data-testid="stVerticalBlockBorderWrapper"] > div { border: 0; }
    [data-testid="stTextInput"] input {
        background: #101613; border: 1px solid #34433b;
        border-radius: 6px; color: var(--text); min-height: 3.15rem;
    }
    [data-testid="stTextInput"] button {
        background: #26332c; border: 1px solid #34433b; color: var(--text);
    }
    [data-testid="stTextInput"] input:focus { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent); }
    [data-testid="stMetric"] {
        background: #121915; border: 1px solid var(--line);
        border-radius: 6px; padding: .7rem .85rem;
    }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    [data-testid="stProgressBar"] > div > div { background: var(--accent); }
    .result-heading { display: flex; justify-content: space-between; align-items: baseline; gap: 1rem; margin: .1rem 0 .6rem; }
    .result-strength { font-size: 1.35rem; font-weight: 650; color: var(--text); }
    .result-score { color: var(--muted); font-size: .85rem; }
    .section-title { font-size: .85rem; font-weight: 650; margin: 1.35rem 0 .45rem; }
    .check-row { display: flex; justify-content: space-between; gap: 1rem; padding: .52rem 0; border-bottom: 1px solid var(--line); font-size: .88rem; }
    .check-name { color: var(--muted); }
    .check-pass { color: var(--accent); }
    .check-fail { color: #829188; }
    .finding { color: var(--warning); font-size: .86rem; padding: .28rem 0; }
    .tip { color: var(--muted); font-size: .86rem; padding: .28rem 0; }
    .empty-state { color: var(--muted); font-size: .9rem; line-height: 1.65; padding: 1rem 0 .2rem; }
    .privacy { color: var(--muted); font-size: .78rem; margin-top: 1rem; }
    @media (max-width: 700px) {
        .block-container { padding-top: 1.25rem; }
        h1 { font-size: 1.85rem; }
        .brand { font-size: .68rem; }
        .stApp::before {
            content: "01 // CHECK\\A 02 length = input.length\\A 03 hasUpper(input)\\A 04 score = rate(input);";
            top: 24rem;
            right: .5rem;
            width: 11rem;
            height: 18rem;
            font-size: 8px;
            opacity: .45;
            transform: none;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="topbar"><div class="brand"><span class="brand-symbol">S</span>'
    '<span>STRENGTH / PASSWORD ANALYZER</span></div>'
    '<span class="local-label"><span class="status-dot"></span> LOCAL ANALYSIS</span></div>'
    '<div class="header-rule"></div>',
    unsafe_allow_html=True,
)
st.title("Password security")
st.markdown(
    '<p class="intro">Review strength and spot patterns that make a password easier to guess.</p>',
    unsafe_allow_html=True,
)

input_column, analysis_column = st.columns([0.9, 1.1], gap="large")

with input_column:
    with st.container(border=True):
        st.markdown('<div class="section-kicker">PASSWORD INPUT</div>', unsafe_allow_html=True)
        st.subheader("Check a password")
        st.caption("Enter a password to review its length, character mix, and predictability.")
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password",
        )
        st.markdown(
            '<div class="privacy">Analyzed locally by this app. No external API is used.</div>',
            unsafe_allow_html=True,
        )

with analysis_column:
    with st.container(border=True):
        if password:
            result = analyze_password(password)
            st.markdown('<div class="section-kicker">ASSESSMENT</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="result-heading"><span class="result-strength">{result["strength"]}</span>'
                f'<span class="result-score">{result["score"]} / 100</span></div>',
                unsafe_allow_html=True,
            )
            st.progress(result["score"])

            metric_columns = st.columns(2)
            metric_columns[0].metric("Length", f'{len(password)} characters')
            metric_columns[1].metric(
                "Checks passed",
                f'{sum(result["checks"].values())} / {len(result["checks"])}',
            )

            st.markdown('<div class="section-title">Password checklist</div>', unsafe_allow_html=True)
            for label, passed in result["checks"].items():
                state_class = "check-pass" if passed else "check-fail"
                state_text = "Pass" if passed else "Missing"
                st.markdown(
                    f'<div class="check-row"><span class="check-name">{label}</span>'
                    f'<span class="{state_class}">{state_text}</span></div>',
                    unsafe_allow_html=True,
                )

            if result["findings"]:
                st.markdown('<div class="section-title">Predictability</div>', unsafe_allow_html=True)
                for finding in result["findings"]:
                    st.markdown(f'<div class="finding">{finding}</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-title">Recommendations</div>', unsafe_allow_html=True)
            for tip in result["tips"]:
                st.markdown(f'<div class="tip">{tip}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="section-kicker">ASSESSMENT</div>', unsafe_allow_html=True)
            st.subheader("Analysis")
            st.markdown(
                '<div class="empty-state">Your strength score, password checklist, and recommendations '
                'will appear here when you enter a password.</div>',
                unsafe_allow_html=True,
            )

st.markdown(
    '<div class="privacy">Strength estimates are heuristic and do not check known data breaches. '
    'Use unique passwords and store them in a password manager.</div>',
    unsafe_allow_html=True,
)