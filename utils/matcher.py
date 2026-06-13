"""
utils/matcher.py
-----------------
Skill-based job description matcher.

Compares skills extracted from a resume against skills mentioned in a
job description to calculate a match score and identify gaps.
"""

import re
from utils.extractor import SKILL_KEYWORDS


class JobMatcher:
    """
    Calculates how well a candidate's skill set matches a job description.

    Args:
        resume_skills: List of skills extracted from the resume.
        job_description: Raw job description text.
    """

    def __init__(self, resume_skills: list[str], job_description: str):
        self.resume_skills  = [s.lower() for s in resume_skills]
        self.job_description = job_description.lower()

    # ── Public API ──────────────────────────────────────────────────────────

    def match(self) -> dict:
        """
        Returns:
            {
                "score":   float (0-100),
                "matched": list[str],
                "missing": list[str],
            }
        """
        jd_skills = self._extract_jd_skills()

        if not jd_skills:
            return {"score": 0.0, "matched": [], "missing": []}

        matched = [s for s in jd_skills if s in self.resume_skills]
        missing = [s for s in jd_skills if s not in self.resume_skills]
        score   = (len(matched) / len(jd_skills)) * 100

        return {
            "score":   round(score, 1),
            "matched": [s.title() for s in matched],
            "missing": [s.title() for s in missing],
        }

    # ── Private helpers ─────────────────────────────────────────────────────

    def _extract_jd_skills(self) -> list[str]:
        """Extract skill keywords from the job description."""
        found = []
        for skill in SKILL_KEYWORDS:
            if " " in skill:
                if skill in self.job_description:
                    found.append(skill)
            else:
                pattern = rf"\b{re.escape(skill)}\b"
                if re.search(pattern, self.job_description):
                    found.append(skill)
        return list(set(found))
