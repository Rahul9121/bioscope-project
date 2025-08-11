from reportlab.pdfgen import canvas

def generate_pdf():
    # Create a PDF canvas
    c = canvas.Canvas("test_report.pdf")

    # Add content to the PDF
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Hello, ReportLab!")
    c.drawString(100, 730, "This is a test PDF generated using ReportLab.")
    c.line(100, 720, 400, 720)

    # Save the PDF
    c.save()
    print("PDF generated successfully!")

generate_pdf()
