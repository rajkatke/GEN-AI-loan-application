from fpdf import FPDF

def create_pdf(documents):
    pdf = FPDF()
    for title, content in documents.items():
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, title, ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        # Simple markdown cleanup for PDF and encoding fix
        clean_content = content.replace("**", "").replace("#", "").replace("₹", "Rs. ")
        # Encode to latin-1 compatible text, replacing unknown chars with ?
        clean_content = clean_content.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, clean_content)
    return pdf.output(dest='S').encode('latin-1')

documents = {
    "Sanction Letter": "This is a test sanction letter.\n\nLoan Amount: ₹500,000\n\nCongratulations!"
}

try:
    pdf_bytes = create_pdf(documents)
    print(f"PDF generated successfully. Size: {len(pdf_bytes)} bytes")
except Exception as e:
    print(f"PDF generation failed: {e}")
