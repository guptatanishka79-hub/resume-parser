"""
utils/extractor.py
-------------------
NLP + Regex-based information extractor for resumes.

Extracts:
  - Full Name
  - Email Address
  - Phone Number
  - LinkedIn / GitHub URLs
  - Skills (matched against a curated tech skill list)
  - Education records
  - Work Experience records
  - Certifications
"""

import re
import spacy
from typing import Any

# ── spaCy model ────────────────────────────────────────────────────────────
# Load once at module level; fall back gracefully if model isn't installed.
try:
    NLP = spacy.load("en_core_web_sm")
except OSError:
    NLP = None
    print("[extractor] spaCy model not found. Name extraction will use regex only.")

# ── Curated skill keyword list ──────────────────────────────────────────────
SKILL_KEYWORDS = [
    # Programming languages
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "go",
    "rust", "kotlin", "swift", "ruby", "php", "r", "matlab", "scala",
    "perl", "bash", "shell", "powershell",
    # Web
    "html", "css", "react", "angular", "vue", "node.js", "django", "flask",
    "fastapi", "express", "spring", "laravel", "nextjs", "nuxtjs",
    "bootstrap", "tailwind",
    # Data / ML
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "tensorflow", "keras", "pytorch", "scikit-learn",
    "pandas", "numpy", "matplotlib", "seaborn", "plotly",
    "data analysis", "data science", "statistics",
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "sqlite", "redis", "cassandra",
    "oracle", "firebase",
    # Cloud & DevOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "jenkins",
    "ci/cd", "terraform", "ansible", "linux", "git", "github", "gitlab",
    # Tools & IDEs
    "jupyter", "vscode", "pycharm", "intellij", "postman", "jira", "confluence",
    "excel", "power bi", "tableau", "hadoop", "spark",
    # Concepts
    "agile", "scrum", "rest api", "graphql", "microservices", "oop",
    "data structures", "algorithms", "design patterns",
]

# ── Section header patterns ────────────────────────────────────────────────
EDU_HEADERS   = re.compile(
    r"(education|academic|qualification|degree|university|college|school)",
    re.IGNORECASE,
)
EXP_HEADERS   = re.compile(
    r"(experience|employment|work history|career|internship|job)",
    re.IGNORECASE,
)
CERT_HEADERS  = re.compile(
    r"(certification|certificate|credential|course|training|achievement|award)",
    re.IGNORECASE,
)


class ResumeExtractor:
    """
    Extracts structured information from raw resume text.

    Usage:
        extractor = ResumeExtractor(raw_text)
        data = extractor.extract_all()
    """

    def __init__(self, text: str):
        self.text  = text
        self.lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    # ── Master method ───────────────────────────────────────────────────────

    def extract_all(self) -> dict[str, Any]:
        return {
            "name":           self._extract_name(),
            "email":          self._extract_email(),
            "phone":          self._extract_phone(),
            "linkedin":       self._extract_linkedin(),
            "github":         self._extract_github(),
            "skills":         self._extract_skills(),
            "education":      self._extract_section(EDU_HEADERS),
            "experience":     self._extract_section(EXP_HEADERS),
            "certifications": self._extract_section(CERT_HEADERS),
        }

    # ── Individual extractors ───────────────────────────────────────────────

    def _extract_name(self) -> str:
        """
        Name detection strategy:
          1. spaCy PERSON entity on the first 300 chars.
          2. Fallback: first non-empty line that looks like a name.
        """
        if NLP:
            doc = NLP(self.text[:300])
            for ent in doc.ents:
                if ent.label_ == "PERSON" and len(ent.text.split()) >= 2:
                    return ent.text.strip()

        # Fallback: first line that is likely a name
        for line in self.lines[:6]:
            # A name should have 2-4 words, no digits, no special chars
            if re.match(r"^[A-Za-z][A-Za-z .'-]{3,50}$", line):
                words = line.split()
                if 2 <= len(words) <= 4:
                    return line
        return ""

    def _extract_email(self) -> str:
        """Extract first valid email address found in the text."""
        pattern = r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
        match   = re.search(pattern, self.text)
        return match.group(0) if match else ""

    def _extract_phone(self) -> str:
        """
        Extract phone number supporting formats:
          +91-9876543210, (123) 456-7890, 123.456.7890, 1234567890
        """
        pattern = (
            r"(\+?\d{1,3}[\s\-]?)?(\(?\d{3}\)?[\s\-\.]?)?"
            r"\d{3}[\s\-\.]?\d{4}"
        )
        match = re.search(pattern, self.text)
        if match:
            phone = re.sub(r"[^\d+\-() ]", "", match.group(0)).strip()
            if len(re.sub(r"\D", "", phone)) >= 7:
                return phone
        return ""

    def _extract_linkedin(self) -> str:
        """Extract LinkedIn profile URL or username."""
        pattern = r"(https?://)?(www\.)?linkedin\.com/in/[\w\-]+"
        match   = re.search(pattern, self.text, re.IGNORECASE)
        return match.group(0) if match else ""

    def _extract_github(self) -> str:
        """Extract GitHub profile URL or username."""
        pattern = r"(https?://)?(www\.)?github\.com/[\w\-]+"
        match   = re.search(pattern, self.text, re.IGNORECASE)
        return match.group(0) if match else ""

    def _extract_skills(self) -> list[str]:
        """
        Match skills against a curated keyword list.
        Case-insensitive whole-word matching.
        """
        text_lower = self.text.lower()
        found      = []
        for skill in SKILL_KEYWORDS:
            # Use word boundary for single-word skills
            if " " in skill:
                if skill in text_lower:
                    found.append(skill.title())
            else:
                pattern = rf"\b{re.escape(skill)}\b"
                if re.search(pattern, text_lower):
                    found.append(skill.upper() if len(skill) <= 4 else skill.title())
        return sorted(set(found))

    def _extract_section(self, header_pattern: re.Pattern) -> list[str]:
        """
        Generic section extractor.
        Finds the header line then collects non-empty lines until the
        next recognisable section header is encountered.
        """
        OTHER_HEADERS = re.compile(
            r"(skills|projects|publications|references|languages|"
            r"interests|hobbies|summary|objective|profile)",
            re.IGNORECASE,
        )

        collecting = False
        items: list[str] = []

        for line in self.lines:
            # Detect start of target section
            if header_pattern.search(line) and len(line) < 60:
                collecting = True
                continue

            if collecting:
                # Stop at another section header
                if (OTHER_HEADERS.search(line) or
                        EDU_HEADERS.search(line) or
                        EXP_HEADERS.search(line) or
                        CERT_HEADERS.search(line)) and len(line) < 60:
                    break

                # Skip very short / noisy lines
                if len(line) < 5:
                    continue

                # Collect meaningful lines
                if len(line) > 8:
                    items.append(line)

                if len(items) >= 10:   # Cap per-section
                    break

        return items
