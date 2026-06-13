# 📄 Resume Parser Pro

> An intelligent, end-to-end resume parsing tool built with Python, Streamlit, and NLP — designed as a portfolio-quality internship project.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red?logo=streamlit)
![spaCy](https://img.shields.io/badge/spaCy-3.7%2B-09a3d5?logo=spacy)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🏷️ Intern Details

| Field | Value |
|-------|-------|
| **Intern ID** | `CITS4367` |
| **Project** | Resume Parser Pro |
| **Domain** | Python / NLP / Web Development |

---

## 📌 Project Overview

**Resume Parser Pro** is a full-stack AI-powered application that automatically extracts, analyses, and matches resume data from PDF files. Upload any PDF resume and instantly get:

- Structured candidate information (name, email, phone, social links)
- Detected skills with category breakdown
- Education, experience, and certification records
- A **job description match score** with matched/missing skill analysis

Built for real-world use and internship portfolios.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📤 PDF Upload | Drag-and-drop or browse to upload any PDF resume |
| 👤 Info Extraction | Extracts name, email, phone, LinkedIn, GitHub automatically |
| 🛠 Skill Detection | Matches 100+ tech skills across 7 categories |
| 🎓 Education Parsing | Identifies degree, institution, and year information |
| 💼 Experience Parsing | Extracts work history and internship records |
| 🏅 Certifications | Finds course completions and awards |
| 📊 Visual Dashboard | Interactive Plotly charts for skill breakdown |
| 🎯 Job Match Score | Calculates % match and highlights skill gaps |
| ⬇️ CSV Export | Download extracted data as a spreadsheet |

---

## 🛠 Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Python 3.10+** | Core language |
| **Streamlit** | Web UI framework |
| **pdfplumber** | Primary PDF text extraction |
| **PyPDF2** | Fallback PDF extraction |
| **spaCy (en_core_web_sm)** | Named Entity Recognition (name detection) |
| **Regex** | Pattern-based extraction (email, phone, URLs) |
| **Plotly** | Interactive charts and gauge visualisations |
| **Pandas** | Data structuring and CSV export |
| **scikit-learn** | (Available for future ML-based scoring) |

---

## 📂 Project Structure

```
resume-parser/
│
├── app.py                  # Main Streamlit application entry point
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── utils/
│   ├── __init__.py
│   ├── parser.py           # PDF text extraction (pdfplumber + PyPDF2)
│   ├── extractor.py        # NLP + Regex information extractor
│   ├── matcher.py          # Job description skill matcher
│   └── visualization.py    # Plotly chart builders
│
├── data/                   # (Optional) processed output storage
├── models/                 # (Optional) custom spaCy/ML models
├── screenshots/            # UI screenshots for documentation
└── sample_resumes/         # Test resumes for demonstration
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Git

### Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/resume-parser.git
cd resume-parser
```

### Step 2 — Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Download the spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

### Step 5 — Run the Application

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

---

## 🚀 Usage

1. **Upload a PDF** — Click the upload area and select a PDF resume.
2. **View Profile** — The *Profile* tab shows all extracted information.
3. **Explore Analysis** — The *Analysis* tab shows skill charts and a candidate summary.
4. **Match a Job** — Paste a job description in the *Job Match* tab and click **Calculate Match**.
5. **Export Data** — Go to the *Raw Data* tab and click **Download as CSV**.

---

## 📸 Screenshots

> Add screenshots to the `screenshots/` folder and update the links below.

| Profile Tab | Analysis Tab | Job Match Tab |
|-------------|--------------|---------------|
| ![Profile](screenshots/profile.png) | ![Analysis](screenshots/analysis.png) | ![Match](screenshots/match.png) |

---

## 🔮 Future Enhancements

- [ ] **Multi-resume comparison** — Upload and compare multiple candidates side-by-side
- [ ] **ATS Score** — Simulate Applicant Tracking System scoring
- [ ] **Custom skill lists** — User-defined skill taxonomy per industry
- [ ] **GPT-powered summary** — AI-generated candidate overview
- [ ] **Database storage** — PostgreSQL/MongoDB backend for resume history
- [ ] **REST API** — FastAPI wrapper for integration with HR platforms
- [ ] **Bulk parsing** — Process entire folders of resumes at once
- [ ] **Resume scoring model** — ML model trained on real hiring data

---

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss what you'd like to change.

```bash
# Fork → Clone → Branch → Commit → PR
git checkout -b feature/your-feature-name
git commit -m "feat: add your feature"
git push origin feature/your-feature-name
```

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [spaCy](https://spacy.io/) for the excellent NLP library
- [Streamlit](https://streamlit.io/) for the rapid web-app framework
- [pdfplumber](https://github.com/jsvine/pdfplumber) for robust PDF extraction
- [Plotly](https://plotly.com/) for beautiful interactive charts

---

<div align="center">
  Made with ❤️ as an internship portfolio project &nbsp;|&nbsp; Intern ID: <strong>CITS4367</strong>
</div>
