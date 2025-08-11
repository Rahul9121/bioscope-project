from flask import Flask, request, render_template, jsonify
from backend.api.data_query import get_biodiversity_risks
import os
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

app = Flask(__name__, template_folder="../frontend/templates")

GEOCODING_API_URL = "https://nominatim.openstreetmap.org/search"

# Function to fetch latitude and longitude from ZIP code
def get_lat_lon_from_zip(zipcode):
    response = requests.get(
        GEOCODING_API_URL,
        params={
            "postalcode": zipcode,
            "countrycodes": "us",
            "format": "json"
        },
        headers={"User-Agent": "BiodivProScopeApp/1.0"}
    )
    if response.status_code == 200:
        data = response.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
        else:
            raise ValueError("Invalid ZIP code or no data found")
    else:
        raise ValueError(f"Failed to fetch data: {response.status_code} - {response.text}")

@app.route('/')
def index():
    return render_template('zip_code.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        zipcode = request.form.get('zipcode')
        lat, lon = get_lat_lon_from_zip(zipcode)
        risks = get_biodiversity_risks(lat, lon)

        print(f"ZIP Code: {zipcode}, Lat: {lat}, Lon: {lon}, Risks: {risks}")  # Debug log

        return render_template("results.html", results={
            "center": {"latitude": lat, "longitude": lon, "zipcode": zipcode},
            "risks": risks
        })
    except Exception as e:
        print(f"Error in /search route: {e}")
        return f"Error: {e}", 400



# Report generation route
@app.route('/generate-report', methods=['POST'])
def generate_report_route():
    try:
        zipcode = request.form.get('zipcode')
        print(f"Received ZIP code: {zipcode}")  # Debug log

        if not zipcode or not zipcode.strip():
            return jsonify({"status": "error", "message": "ZIP code is required."}), 400

        lat, lon = get_lat_lon_from_zip(zipcode)
        risks = get_biodiversity_risks(lat, lon)

        # Ensure the reports directory exists
        reports_dir = os.path.join("../../../PycharmProjects/BiodivProScopeTeam/backend/static", "reports")
        os.makedirs(reports_dir, exist_ok=True)  # Create directory if it doesn't exist

        pdf_filename = f"risk_report_{zipcode.strip()}.pdf"
        pdf_path = os.path.join(reports_dir, pdf_filename)

        def generate_report(pdf_path, zipcode, lat, lon, risks):
            try:
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

                    if y < 50:  # Avoid writing too close to the bottom
                        c.showPage()
                        y = height - 50

                c.save()
                print(f"PDF generated at {pdf_path}")  # Debug log
            except Exception as e:
                print(f"Error in PDF generation: {e}")
                raise e

        pdf_url = f"/static/reports/{pdf_filename}"
        return jsonify({"status": "success", "report_url": pdf_url}), 200
    except Exception as e:
        print(f"Error generating report: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)
