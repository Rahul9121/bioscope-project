from backend.test_haversine_app import app
from flask import request, jsonify


from backend.test_haversine_app import get_lat_lon_from_zip
from backend.utils.pdf_generator import generate_report

@app.route('/generate-report', methods=['POST'])
def generate_report_route():
    try:
        # Get data from the form or a session
        zipcode = request.form.get('zipcode')
        lat, lon = get_lat_lon_from_zip(zipcode)

        # Generate the report
        pdf_path = f"reports/risk_report_{zipcode}.pdf"
        generate_report(pdf_path, zipcode, lat, lon, risks)

        # Serve the generated PDF to the client
        return jsonify({"status": "success", "report_url": pdf_path}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
