"""
utils/visualization.py
-----------------------
Plotly chart builders for the Resume Parser dashboard.

Functions:
  - create_skill_chart   → Horizontal bar chart of skill categories
  - create_match_gauge   → Gauge chart for job-match percentage
"""

import plotly.graph_objects as go
import plotly.express as px


# ── Skill category mapping ──────────────────────────────────────────────────
CATEGORY_MAP = {
    "Programming": [
        "python", "java", "javascript", "typescript", "c", "c++", "c#",
        "go", "rust", "kotlin", "swift", "ruby", "php", "r", "matlab",
        "scala", "perl", "bash", "shell", "powershell",
    ],
    "Web Dev": [
        "html", "css", "react", "angular", "vue", "node.js", "django",
        "flask", "fastapi", "express", "spring", "laravel", "nextjs",
        "nuxtjs", "bootstrap", "tailwind",
    ],
    "Data / ML": [
        "machine learning", "deep learning", "nlp", "natural language processing",
        "computer vision", "tensorflow", "keras", "pytorch", "scikit-learn",
        "pandas", "numpy", "matplotlib", "seaborn", "plotly",
        "data analysis", "data science", "statistics",
    ],
    "Databases": [
        "sql", "mysql", "postgresql", "mongodb", "sqlite", "redis",
        "cassandra", "oracle", "firebase",
    ],
    "Cloud / DevOps": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
        "jenkins", "ci/cd", "terraform", "ansible", "linux", "git",
        "github", "gitlab",
    ],
    "Tools": [
        "jupyter", "vscode", "pycharm", "intellij", "postman", "jira",
        "confluence", "excel", "power bi", "tableau", "hadoop", "spark",
    ],
    "Concepts": [
        "agile", "scrum", "rest api", "graphql", "microservices", "oop",
        "data structures", "algorithms", "design patterns",
    ],
}

# Colour palette aligned with the app's dark theme
PALETTE = [
    "#7c83fd", "#5eead4", "#fbbf24", "#34d399",
    "#f87171", "#a78bfa", "#38bdf8",
]


def create_skill_chart(skills: list[str]) -> go.Figure:
    """
    Horizontal bar chart showing how many detected skills fall in each category.

    Args:
        skills: List of skill strings from the resume extractor.

    Returns:
        Plotly Figure object.
    """
    skills_lower = [s.lower() for s in skills]
    counts       = {}

    for category, keywords in CATEGORY_MAP.items():
        count = sum(1 for k in keywords if k in skills_lower)
        if count > 0:
            counts[category] = count

    if not counts:
        # Empty-state figure
        fig = go.Figure()
        fig.add_annotation(
            text="No categorisable skills found",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(color="#94a3b8", size=14),
        )
        _apply_dark_layout(fig, title="Skill Category Breakdown")
        return fig

    cats   = list(counts.keys())
    values = list(counts.values())
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(cats))]

    fig = go.Figure(go.Bar(
        x=values,
        y=cats,
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=values,
        textposition="outside",
        textfont=dict(color="#e2e8f0"),
    ))

    _apply_dark_layout(fig, title="Skill Category Breakdown")
    fig.update_layout(
        xaxis=dict(title="Count", gridcolor="#2d3147"),
        yaxis=dict(autorange="reversed"),
        bargap=0.35,
    )
    return fig


def create_match_gauge(score: float) -> go.Figure:
    """
    Semicircular gauge showing the job-match percentage.

    Args:
        score: Float between 0 and 100.

    Returns:
        Plotly Figure object.
    """
    # Colour based on score band
    if score >= 75:
        colour = "#10b981"     # green
    elif score >= 50:
        colour = "#fbbf24"     # amber
    else:
        colour = "#ef4444"     # red

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        delta={"reference": 70, "increasing": {"color": "#10b981"}, "decreasing": {"color": "#ef4444"}},
        number={"suffix": "%", "font": {"size": 36, "color": "#e2e8f0"}},
        title={"text": "Match Score", "font": {"size": 16, "color": "#94a3b8"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#94a3b8", "tickfont": {"color": "#94a3b8"}},
            "bar": {"color": colour, "thickness": 0.25},
            "bgcolor": "#1e2130",
            "bordercolor": "#3a3f5c",
            "steps": [
                {"range": [0,  50], "color": "#1e2130"},
                {"range": [50, 75], "color": "#252840"},
                {"range": [75, 100], "color": "#2a2f4a"},
            ],
            "threshold": {
                "line": {"color": "#7c83fd", "width": 3},
                "thickness": 0.75,
                "value": 70,
            },
        },
    ))

    _apply_dark_layout(fig, title="")
    fig.update_layout(height=280)
    return fig


# ── Shared layout helper ───────────────────────────────────────────────────

def _apply_dark_layout(fig: go.Figure, title: str = "") -> None:
    """Apply consistent dark-theme layout to any figure."""
    fig.update_layout(
        title=dict(text=title, font=dict(color="#e2e8f0", size=15)),
        paper_bgcolor="#0f1117",
        plot_bgcolor="#0f1117",
        font=dict(color="#94a3b8"),
        margin=dict(l=10, r=10, t=40, b=10),
    )
