import json
from utils.pdf_structure import structure_extracted_data

pdf_path = "C:/Users/umair/Desktop/Misc/Final Year Project Proposal/FYP Proposal (AI Surveillance System).pdf"
data = structure_extracted_data(pdf_path)

print(json.dumps(data, indent=2, ensure_ascii=False))