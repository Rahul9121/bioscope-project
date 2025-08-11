from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_report(pdf_path, zipcode, lat, lon, risks):
    """
    Generate a PDF report with risks and mitigation actions.
    """
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "Biodiversity Risk Report")

    # Subtitle
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, height - 100, f"ZIP Code: {zipcode}")
    c.drawString(50, height - 120, f"Location: Latitude {lat}, Longitude {lon}")

    # Risks Section
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 160, "Identified Risks:")
    c.setFont("Helvetica", 12)
    y = height - 180
    for idx, risk in enumerate(risks, start=1):
        c.drawString(50, y, f"{idx}. {risk['risk_type']}: {risk['description']}")
        y -= 20

        # Mitigation Actions
        mitigation_action = get_mitigation_action(risk['risk_type'])
        c.drawString(70, y, f"Mitigation: {mitigation_action}")
        y -= 40

        # Ensure there's enough space for more content
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()

def get_mitigation_action(risk_type):
    """
    Return mitigation actions based on the risk type.
    """
    actions = {
        "Threatened Species": "Limit human activity and protect habitats.",
        "Freshwater Pollution": "Reduce agricultural runoff and industrial waste.",
        "Invasive Species": "Implement eradication and monitoring programs.",
    }
    return actions.get(risk_type, "No specific mitigation available.")
