from pathlib import Path
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

REPORTS_DIR = Path("/app/reports")
FIGURES_DIR = REPORTS_DIR / "figures"


def read_report(filename: str) -> str:
    path = REPORTS_DIR / filename
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Файл звіту ще не створено."


@app.route("/")
def index():
    quality_report = read_report("data_quality_report.txt")
    research_report = read_report("data_research_report.txt")

    figures = []
    if FIGURES_DIR.exists():
        figures = sorted([file.name for file in FIGURES_DIR.glob("*.png")])

    return render_template(
        "index.html",
        quality_report=quality_report,
        research_report=research_report,
        figures=figures,
    )


@app.route("/figures/<path:filename>")
def figure_file(filename):
    return send_from_directory(FIGURES_DIR, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)