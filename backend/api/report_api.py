from backend.utils.pdf_generator import create_pdf

def generate_report_pdf(hotel_name, location, risks, mitigation):
    """
    Generate the biodiversity report as a PDF.
    """
    template = 'report_template.html'
    output_file = f'{hotel_name}_biodiversity_report.pdf'
    data = {
        'hotel_name': hotel_name,
        'location': location,
        'risks': risks,
        'mitigation': mitigation
    }
    create_pdf(template, data, output_file)
    return output_file

