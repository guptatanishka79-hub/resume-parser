"""
utils/parser.py
----------------
PDF text extraction module.
Uses pdfplumber (primary) with PyPDF2 as fallback for broad format support.
"""

import pdfplumber
import PyPDF2
import re
from pathlib import Path


class PDFParser:
    """
    Extracts raw text from PDF resumes.

    Tries pdfplumber first (better layout preservation),
    then falls back to PyPDF2 for encrypted or non-standard PDFs.
    """

    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # ── Public API ──────────────────────────────────────────────────────────

    def extract_text(self) -> str:
        """Return cleaned text from all pages of the PDF."""
        text = self._extract_with_pdfplumber()
        if not text or len(text.strip()) < 50:
            text = self._extract_with_pypdf2()
        return self._clean_text(text)

    def get_page_count(self) -> int:
        """Return the number of pages in the PDF."""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                return len(pdf.pages)
        except Exception:
            with open(self.pdf_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                return len(reader.pages)

    # ── Private helpers ─────────────────────────────────────────────────────

    def _extract_with_pdfplumber(self) -> str:
        """Primary extraction using pdfplumber."""
        pages_text = []
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        pages_text.append(text)
        except Exception as e:
            print(f"[pdfplumber] Extraction error: {e}")
        return "\n".join(pages_text)

    def _extract_with_pypdf2(self) -> str:
        """Fallback extraction using PyPDF2."""
        pages_text = []
        try:
            with open(self.pdf_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        pages_text.append(text)
        except Exception as e:
            print(f"[PyPDF2] Extraction error: {e}")
        return "\n".join(pages_text)

    @staticmethod
    def _clean_text(text: str) -> str:
        """Normalise whitespace and remove junk characters."""
        if not text:
            return ""
        # Replace non-breaking spaces
        text = text.replace("\xa0", " ")
        # Collapse multiple blank lines → single blank line
        text = re.sub(r"\n{3,}", "\n\n", text)
        # Strip leading/trailing whitespace per line
        lines = [line.strip() for line in text.splitlines()]
        text  = "\n".join(lines)
        return text.strip()
