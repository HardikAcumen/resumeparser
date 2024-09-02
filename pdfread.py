import PyPDF2

def read_pdf(file_path):
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

# Example usage
pdf_path = r'resumes\resume1.pdf'
pdf_text = read_pdf(pdf_path)
print(pdf_text)
