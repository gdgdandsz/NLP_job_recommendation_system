from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def convert_txt_to_pdf(txt_file, pdf_file):
    with open(txt_file, 'r', encoding='latin-1') as txt:
        lines = txt.readlines()

    pdf = canvas.Canvas(pdf_file, pagesize=letter)
    for line in lines:
        pdf.drawString(100, 800, line.strip())  # You can adjust the coordinates as needed
        pdf.showPage()

    pdf.save()

def batch_convert_to_pdf(txt_folder, pdf_folder):
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    txt_files = [f for f in os.listdir(txt_folder) if f.endswith('.txt')]

    for txt_file in txt_files:
        txt_path = os.path.join(txt_folder, txt_file)
        pdf_file = os.path.join(pdf_folder, os.path.splitext(txt_file)[0] + '.pdf')
        convert_txt_to_pdf(txt_path, pdf_file)

# Example Usage
txt_folder_path = 'resume_txt'
pdf_folder_path = 'resume_pdf'
batch_convert_to_pdf(txt_folder_path, pdf_folder_path)
