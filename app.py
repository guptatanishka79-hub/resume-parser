"""
Resume Parser - Main Application
Author: Intern Project
Description: An intelligent resume parsing tool built with Streamlit
             that extracts and analyzes resume data using NLP and Regex.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import tempfile
import os

# Local utility imports
from utils.parser import PDFParser
from utils.extractor import ResumeExtractor
from utils.matcher import JobMatcher
from utils.visualization import create_skill_chart, create_match_gauge

# ─────────────────────────────────────────────
#  Page Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Resume Parser Pro",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; }

    /* Cards */
    .info-card {
        background: linear-gradient(135deg, #1e2130, #252840);
        border: 1px solid #3a3f5c;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }
    .info-card h4 {
        color: #7c83fd;
        margin: 0 0 0.4rem 0;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .info-card p {
        color: #e2e8f0;
        margin: 0;
        font-size: 1rem;
        font-weight: 500;
    }

    /* Skill badges */
    .skill-badge {
        display: inline-block;
        background: #7c83fd22;
        border: 1px solid #7c83fd55;
        color: #a5b4fc;
        border-radius: 20px;
        padding: 3px 12px;
        margin: 3px;
        font-size: 0.82rem;
        font-weight: 500;
    }
    .skill-badge.match {
        background: #10b98122;
        border-color: #10b98155;
        color: #6ee7b7;
    }
    .skill-badge.missing {
        background: #ef444422;
        border-color: #ef444455;
        color: #fca5a5;
    }

    /* Section header */
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #7c83fd;
        border-bottom: 2px solid #7c83fd44;
        padding-bottom: 0.4rem;
        margin-bottom: 1rem;
    }

    /* Metric overrides */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1e2130, #252840);
        border: 1px solid #3a3f5c;
        border-radius: 10px;
        padding: 0.8rem 1rem;
    }

    /* Upload area */
    [data-testid="stFileUploader"] {
        background: #1e2130;
        border-radius: 12px;
        border: 2px dashed #3a3f5c;
    }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #13151f; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/resume.png", width=64)
    st.title("Resume Parser Pro")
    st.caption("Powered by NLP + Regex")
    st.divider()

    st.markdown("### 🔧 Settings")
    show_raw_text = st.checkbox("Show extracted raw text", value=False)
    st.divider()

    st.markdown("### ℹ️ About")
    st.info(
        "Upload any PDF resume to extract structured information, "
        "analyse candidate profile, and match against a job description."
    )
    st.markdown("---")
    st.caption("🎓 Internship Portfolio Project")
    st.caption("Tech: Python · Streamlit · spaCy · Regex")


# ─────────────────────────────────────────────
#  Header
# ─────────────────────────────────────────────
col_logo, col_title = st.columns([1, 9])
with col_logo:
    st.markdown("## 📄")
with col_title:
    st.markdown("## Resume Parser Pro")
    st.caption("Extract · Analyse · Match — all in one place")

st.divider()

# ─────────────────────────────────────────────
#  File Upload
# ─────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload a PDF Resume",
    type=["pdf"],
    help="Supports standard single-column and multi-column PDF resumes.",
)

if uploaded_file is None:
    st.markdown("""
    <div style='text-align:center; padding: 3rem 0; color: #4a5568;'>
        <div style='font-size: 3rem'>📂</div>
        <p>Upload a PDF resume above to get started.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────
#  Parse Resume
# ─────────────────────────────────────────────
with st.spinner("Parsing resume…"):
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        # Extract raw text
        parser   = PDFParser(tmp_path)
        raw_text = parser.extract_text()

        # Extract structured data
        extractor = ResumeExtractor(raw_text)
        data      = extractor.extract_all()

    except Exception as e:
        st.error(f"❌ Failed to parse resume: {e}")
        os.unlink(tmp_path)
        st.stop()
    finally:
        os.unlink(tmp_path)

st.success(f"✅ Resume parsed successfully — **{uploaded_file.name}**")

# ─────────────────────────────────────────────
#  Tabs
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "👤 Profile",
    "📊 Analysis",
    "🎯 Job Match",
    "📋 Raw Data",
])

# ══════════════════════════════════════════════
#  TAB 1 — Profile
# ══════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">Candidate Information</div>', unsafe_allow_html=True)

    # Top identity cards
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="info-card">
            <h4>👤 Full Name</h4>
            <p>{data.get('name', 'Not detected')}</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="info-card">
            <h4>📧 Email</h4>
            <p>{data.get('email', 'Not detected')}</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="info-card">
            <h4>📞 Phone</h4>
            <p>{data.get('phone', 'Not detected')}</p>
        </div>""", unsafe_allow_html=True)

    # Social links
    c4, c5 = st.columns(2)
    with c4:
        linkedin = data.get('linkedin', 'Not detected')
        st.markdown(f"""
        <div class="info-card">
            <h4>🔗 LinkedIn</h4>
            <p>{linkedin}</p>
        </div>""", unsafe_allow_html=True)
    with c5:
        github = data.get('github', 'Not detected')
        st.markdown(f"""
        <div class="info-card">
            <h4>🐙 GitHub</h4>
            <p>{github}</p>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # Skills
    st.markdown('<div class="section-header">🛠 Skills Detected</div>', unsafe_allow_html=True)
    skills = data.get('skills', [])
    if skills:
        badges = "".join(f'<span class="skill-badge">{s}</span>' for s in skills)
        st.markdown(badges, unsafe_allow_html=True)
    else:
        st.info("No skills detected.")

    st.divider()

    # Education & Experience
    ec1, ec2 = st.columns(2)

    with ec1:
        st.markdown('<div class="section-header">🎓 Education</div>', unsafe_allow_html=True)
        for edu in data.get('education', []):
            st.markdown(f"- {edu}")
        if not data.get('education'):
            st.info("No education details detected.")

    with ec2:
        st.markdown('<div class="section-header">💼 Work Experience</div>', unsafe_allow_html=True)
        for exp in data.get('experience', []):
            st.markdown(f"- {exp}")
        if not data.get('experience'):
            st.info("No work experience detected.")

    st.divider()

    # Certifications
    st.markdown('<div class="section-header">🏅 Certifications</div>', unsafe_allow_html=True)
    for cert in data.get('certifications', []):
        st.markdown(f"- {cert}")
    if not data.get('certifications'):
        st.info("No certifications detected.")


# ══════════════════════════════════════════════
#  TAB 2 — Analysis
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">Resume Statistics</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    skills_list = data.get('skills', [])
    m1.metric("Total Skills", len(skills_list))
    m2.metric("Education Records", len(data.get('education', [])))
    m3.metric("Experience Records", len(data.get('experience', [])))
    m4.metric("Certifications", len(data.get('certifications', [])))

    st.divider()

    if skills_list:
        st.markdown('<div class="section-header">Skill Category Breakdown</div>', unsafe_allow_html=True)
        fig = create_skill_chart(skills_list)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No skills available for chart.")

    st.divider()

    # Profile summary
    st.markdown('<div class="section-header">Candidate Summary</div>', unsafe_allow_html=True)
    summary_parts = []
    if data.get('name'):        summary_parts.append(f"**{data['name']}**")
    if data.get('education'):   summary_parts.append(f"holds a degree in **{data['education'][0]}**")
    if data.get('experience'):  summary_parts.append(f"has experience in **{data['experience'][0]}**")
    if skills_list:             summary_parts.append(f"and is proficient in **{len(skills_list)} skills**")

    summary = ", ".join(summary_parts) + "." if summary_parts else "Insufficient data for a summary."
    st.markdown(f"> {summary}")


# ══════════════════════════════════════════════
#  TAB 3 — Job Match
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Job Description Match</div>', unsafe_allow_html=True)
    st.caption("Paste a job description below to see how well this resume matches.")

    jd_text = st.text_area(
        "Job Description",
        height=200,
        placeholder="Paste the job description here…",
    )

    if st.button("🎯 Calculate Match", type="primary") and jd_text.strip():
        with st.spinner("Matching skills…"):
            matcher = JobMatcher(skills_list, jd_text)
            result  = matcher.match()

        score    = result['score']
        matched  = result['matched']
        missing  = result['missing']

        # Gauge
        fig_gauge = create_match_gauge(score)
        st.plotly_chart(fig_gauge, use_container_width=True)

        gc1, gc2 = st.columns(2)

        with gc1:
            st.markdown(f'<div class="section-header">✅ Matching Skills ({len(matched)})</div>', unsafe_allow_html=True)
            if matched:
                badges = "".join(f'<span class="skill-badge match">{s}</span>' for s in matched)
                st.markdown(badges, unsafe_allow_html=True)
            else:
                st.info("No matching skills found.")

        with gc2:
            st.markdown(f'<div class="section-header">❌ Missing Skills ({len(missing)})</div>', unsafe_allow_html=True)
            if missing:
                badges = "".join(f'<span class="skill-badge missing">{s}</span>' for s in missing)
                st.markdown(badges, unsafe_allow_html=True)
            else:
                st.success("All required skills are present!")

        if score >= 75:
            st.success(f"🎉 Strong match! This candidate covers {score:.1f}% of the job requirements.")
        elif score >= 50:
            st.warning(f"⚠️ Moderate match at {score:.1f}%. Some skill gaps exist.")
        else:
            st.error(f"❌ Low match at {score:.1f}%. Significant skill gaps detected.")

    elif jd_text == "":
        st.info("Enter a job description and click **Calculate Match** to begin.")


# ══════════════════════════════════════════════
#  TAB 4 — Raw Data
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">Extracted JSON Data</div>', unsafe_allow_html=True)
    st.json(data)

    if show_raw_text:
        st.divider()
        st.markdown('<div class="section-header">Raw Extracted Text</div>', unsafe_allow_html=True)
        st.text_area("PDF Text", value=raw_text, height=400)

    st.divider()
    # Download as CSV
    flat = {k: str(v) for k, v in data.items()}
    df   = pd.DataFrame([flat])
    csv  = df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download as CSV",
        data=csv,
        file_name="parsed_resume.csv",
        mime="text/csv",
    )
