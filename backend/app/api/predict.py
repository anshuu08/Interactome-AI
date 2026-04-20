"""
Prediction API Endpoint — The core endpoint.

POST /api/predict
    Body: { "drugs": ["aspirin", "warfarin", "ibuprofen"], "patient_profile": {...} }
    → Returns complete interaction analysis with risk levels, side effects,
      explanations, timing, and graph data.

This is what the patient uses to submit their medication list
and get back a comprehensive safety analysis.
"""
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.schemas import PredictionRequest, PredictionResponse
from app.services.predictor import predict_interactions
import io
import json

router = APIRouter(prefix="/api", tags=["Prediction"])


@router.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Predict drug interactions for a medication list.

    Input: List of 2+ drug names + optional patient profile
    Output: Complete analysis including:
        - Overall risk level (LOW/MEDIUM/HIGH) with confidence score
        - Pairwise interactions between every drug pair
        - Higher-order interactions (3+ drugs)
        - Predicted side effects with explanations
        - Medication timing recommendations
        - Interactive graph data for visualization
    """
    result = predict_interactions(
        drug_names=request.drugs,
        patient_profile=request.patient_profile,
    )
    return result


@router.post("/predict/pdf")
async def predict_pdf(request: PredictionRequest):
    """
    Generate a PDF report of the interaction analysis.
    Same analysis as /predict but returned as a downloadable PDF.
    """
    # Get prediction results
    result = predict_interactions(
        drug_names=request.drugs,
        patient_profile=request.patient_profile,
    )

    # Generate PDF
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        )
        from reportlab.lib.units import inch

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
        styles = getSampleStyleSheet()
        elements = []

        # Title
        title_style = ParagraphStyle(
            'CustomTitle', parent=styles['Title'],
            fontSize=20, spaceAfter=12,
            textColor=colors.HexColor('#0d9488'),
        )
        elements.append(Paragraph("Interactome-AI Drug Interaction Report", title_style))
        elements.append(Spacer(1, 12))

        # Summary
        elements.append(Paragraph(f"<b>Overall Risk:</b> {result.overall_risk.value}", styles['Heading2']))
        elements.append(Paragraph(f"<b>Risk Score:</b> {result.risk_score:.1%}", styles['Normal']))
        elements.append(Paragraph(result.summary, styles['Normal']))
        elements.append(Spacer(1, 12))

        # Drugs analyzed
        elements.append(Paragraph("Medications Analyzed", styles['Heading2']))
        drug_text = ", ".join(request.drugs)
        elements.append(Paragraph(drug_text, styles['Normal']))
        elements.append(Spacer(1, 12))

        # Patient profile
        if request.patient_profile:
            elements.append(Paragraph("Patient Profile", styles['Heading2']))
            pp = request.patient_profile
            if pp.age:
                elements.append(Paragraph(f"Age: {pp.age}", styles['Normal']))
            if pp.bmi:
                elements.append(Paragraph(f"BMI: {pp.bmi}", styles['Normal']))
            if pp.conditions:
                elements.append(Paragraph(f"Conditions: {', '.join(pp.conditions)}", styles['Normal']))
            elements.append(Spacer(1, 12))

        # Pairwise interactions
        if result.pairwise_interactions:
            elements.append(Paragraph("Pairwise Drug Interactions", styles['Heading2']))
            pw_data = [["Drug A", "Drug B", "Risk", "Side Effects"]]
            for pw in result.pairwise_interactions:
                risk_color = (
                    "🔴" if pw.risk == "HIGH" else
                    "🟡" if pw.risk == "MEDIUM" else "🟢"
                )
                pw_data.append([
                    pw.drug_a, pw.drug_b,
                    f"{risk_color} {pw.risk.value}",
                    ", ".join(pw.side_effects[:2]),
                ])
            t = Table(pw_data, colWidths=[1.3*inch, 1.3*inch, 1*inch, 2.5*inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d9488')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 12))

        # Higher-order interactions
        if result.higher_order_interactions:
            elements.append(Paragraph("Multi-Drug Interactions (3+ Drugs)", styles['Heading2']))
            for ho in result.higher_order_interactions:
                drugs_str = " + ".join(ho.drugs)
                elements.append(Paragraph(
                    f"<b>{drugs_str}</b> — Risk: {ho.risk.value} (Confidence: {ho.confidence:.0%})",
                    styles['Normal']
                ))
                elements.append(Paragraph(f"Side effects: {', '.join(ho.side_effects)}", styles['Normal']))
                elements.append(Paragraph(f"Mechanism: {ho.mechanism}", styles['Normal']))
                elements.append(Spacer(1, 6))
            elements.append(Spacer(1, 12))

        # Medication timing
        if result.medication_timing:
            elements.append(Paragraph("Medication Timing Recommendations", styles['Heading2']))
            for mt in result.medication_timing:
                elements.append(Paragraph(
                    f"<b>{mt.drug}:</b> {mt.suggested_time} — {mt.notes}",
                    styles['Normal']
                ))
            elements.append(Spacer(1, 12))

        # Disclaimer
        disclaimer_style = ParagraphStyle(
            'Disclaimer', parent=styles['Normal'],
            fontSize=7, textColor=colors.grey,
        )
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(
            "DISCLAIMER: This report is generated by an AI system and is for informational purposes only. "
            "It is NOT a substitute for professional medical advice. Always consult your healthcare provider "
            "before making changes to your medication regimen.",
            disclaimer_style
        ))

        doc.build(elements)
        buffer.seek(0)

        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=interactome_ai_report.pdf"
            },
        )

    except ImportError:
        # reportlab not installed — return JSON instead
        return result.model_dump()
