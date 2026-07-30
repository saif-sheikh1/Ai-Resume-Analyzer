"""
Report service — generates PDF reports using ReportLab.
"""
import io
from uuid import UUID
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from app.repositories.analysis_repo import AnalysisRepository
from app.repositories.resume_repo import ResumeRepository
from app.core.logging import get_logger

logger = get_logger(__name__)

# Brand colors
PRIMARY = HexColor("#6366f1")
SECONDARY = HexColor("#8b5cf6")
SUCCESS = HexColor("#22c55e")
WARNING = HexColor("#f59e0b")
DANGER = HexColor("#ef4444")
TEXT_PRIMARY = HexColor("#1e293b")
TEXT_SECONDARY = HexColor("#64748b")
BORDER = HexColor("#e2e8f0")
BG_LIGHT = HexColor("#f8fafc")


def _get_score_color(score: float) -> HexColor:
    """Get color based on score value."""
    if score >= 80:
        return SUCCESS
    elif score >= 60:
        return WARNING
    else:
        return DANGER


class ReportService:
    def __init__(self, db: Session):
        self.db = db
        self.analysis_repo = AnalysisRepository(db)
        self.resume_repo = ResumeRepository(db)

    def generate_pdf(self, analysis_id: UUID, user_id: UUID) -> bytes:
        """Generate a comprehensive PDF report for an analysis."""
        analysis = self.analysis_repo.get_by_id_and_user(analysis_id, user_id)
        if not analysis:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")

        resume = self.resume_repo.get_by_id(analysis.resume_id)

        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=A4,
            rightMargin=50, leftMargin=50,
            topMargin=50, bottomMargin=50
        )

        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            "CustomTitle", parent=styles["Title"],
            fontSize=24, textColor=PRIMARY, spaceAfter=20,
            alignment=TA_CENTER
        )
        heading_style = ParagraphStyle(
            "CustomHeading", parent=styles["Heading2"],
            fontSize=16, textColor=TEXT_PRIMARY, spaceAfter=10,
            spaceBefore=20, borderWidth=0, borderPadding=5,
        )
        body_style = ParagraphStyle(
            "CustomBody", parent=styles["Normal"],
            fontSize=11, textColor=TEXT_PRIMARY, spaceAfter=6,
            leading=16
        )
        sub_style = ParagraphStyle(
            "SubText", parent=styles["Normal"],
            fontSize=9, textColor=TEXT_SECONDARY, spaceAfter=4
        )

        story = []

        # ─── Title ───
        story.append(Paragraph("AI Resume Analysis Report", title_style))
        story.append(Paragraph(
            f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            ParagraphStyle("DateStyle", parent=sub_style, alignment=TA_CENTER)
        ))
        story.append(Spacer(1, 20))

        # ─── Resume Info ───
        if resume:
            story.append(Paragraph("Resume Information", heading_style))
            info_data = [
                ["File Name:", resume.filename],
                ["File Type:", resume.file_type.upper()],
                ["Uploaded:", resume.created_at.strftime("%B %d, %Y")],
            ]
            if resume.parsed_data:
                pd = resume.parsed_data
                if pd.get("name"):
                    info_data.insert(0, ["Candidate:", pd["name"]])
                if pd.get("email"):
                    info_data.append(["Email:", pd["email"]])

            info_table = Table(info_data, colWidths=[120, 350])
            info_table.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
                ("TEXTCOLOR", (0, 0), (0, -1), TEXT_SECONDARY),
                ("TEXTCOLOR", (1, 0), (1, -1), TEXT_PRIMARY),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
            ]))
            story.append(info_table)
            story.append(Spacer(1, 15))

        # ─── ATS Score ───
        story.append(Paragraph("ATS Score Overview", heading_style))
        score = analysis.ats_score or 0
        score_color = _get_score_color(score)
        story.append(Paragraph(
            f'<font size="36" color="{score_color}">{score:.0f}</font><font size="18" color="{TEXT_SECONDARY}"> / 100</font>',
            ParagraphStyle("ScoreStyle", parent=body_style, alignment=TA_CENTER, spaceAfter=15)
        ))

        # Section scores table
        if analysis.section_scores:
            scores_data = [["Category", "Score", "Rating"]]
            for category, cat_score in analysis.section_scores.items():
                rating = "Excellent" if cat_score >= 80 else ("Good" if cat_score >= 60 else "Needs Work")
                display_name = category.replace("_", " ").title()
                scores_data.append([display_name, f"{cat_score:.0f}/100", rating])

            scores_table = Table(scores_data, colWidths=[180, 100, 190])
            scores_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("ALIGN", (1, 0), (1, -1), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#ffffff"), BG_LIGHT]),
            ]))
            story.append(scores_table)
            story.append(Spacer(1, 15))

        # ─── AI Summary ───
        if analysis.ai_summary:
            story.append(Paragraph("AI Analysis Summary", heading_style))
            story.append(Paragraph(analysis.ai_summary, body_style))
            story.append(Spacer(1, 10))

        # ─── Strengths ───
        if analysis.strengths:
            story.append(Paragraph("Strengths", heading_style))
            for s in analysis.strengths:
                story.append(Paragraph(f"✅ {s}", body_style))

        # ─── Weaknesses ───
        if analysis.weaknesses:
            story.append(Paragraph("Areas for Improvement", heading_style))
            for w in analysis.weaknesses:
                story.append(Paragraph(f"⚠️ {w}", body_style))

        # ─── Suggestions ───
        if analysis.suggestions:
            story.append(Paragraph("Recommendations", heading_style))
            for i, s in enumerate(analysis.suggestions[:10], 1):
                story.append(Paragraph(f"{i}. {s}", body_style))

        # ─── Career Advice ───
        if analysis.career_advice:
            story.append(Paragraph("Career Advice", heading_style))
            story.append(Paragraph(analysis.career_advice, body_style))

        # ─── Missing Skills ───
        if analysis.missing_skills:
            story.append(Paragraph("Skills to Develop", heading_style))
            skills_text = ", ".join(analysis.missing_skills[:15])
            story.append(Paragraph(skills_text, body_style))

        # Build PDF
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()

        logger.info(f"PDF report generated for analysis {analysis_id}")
        return pdf_bytes
