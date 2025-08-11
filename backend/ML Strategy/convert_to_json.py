import fitz  # PyMuPDF
import json
import re


def extract_paragraphs_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    all_paragraphs = []

    for page in doc:
        text = page.get_text()
        paragraphs = text.split("\n")
        all_paragraphs.extend([p.strip() for p in paragraphs if p.strip() != ""])

    return all_paragraphs


def extract_mitigation_data(paragraphs):
    mitigation_blocks = []
    current_block = {}

    for p in paragraphs:
        # Capture section headings
        if re.match(r"^\d+\.\s", p) or "Mitigation" in p:
            if current_block:
                mitigation_blocks.append(current_block)
                current_block = {}
            current_block["section"] = p

        # Extract metrics
        elif "percent native" in p.lower():
            current_block["native_vegetation_threshold"] = re.findall(r"\d+%", p)
        elif "invasive species" in p.lower():
            current_block["invasive_species_threshold"] = re.findall(r"\d+%", p)
        elif "monitoring" in p.lower():
            current_block.setdefault("monitoring_notes", []).append(p)
        elif "cover" in p.lower() or "canopy" in p.lower():
            current_block.setdefault("vegetation_metrics", []).append(p)

    if current_block:
        mitigation_blocks.append(current_block)

    return mitigation_blocks


def save_to_json(data, output_file):
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)


# ==== Example Usage ====
pdf_path = "data sources/mit_054.pdf"  # Path to your PDF
paragraphs = extract_paragraphs_from_pdf(pdf_path)
structured_data = extract_mitigation_data(paragraphs)
save_to_json(structured_data, "invasive_species_mitigation_guidelines.json")
