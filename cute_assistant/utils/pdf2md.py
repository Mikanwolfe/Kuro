import pdfplumber
import argparse
import os

def pdf_to_text(input_pdf, output_txt):
    with pdfplumber.open(input_pdf) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages)
    
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(text)

def main():
    parser = argparse.ArgumentParser(description='Convert PDF to TXT')
    parser.add_argument('input_pdf', help='Input PDF file')
    parser.add_argument('-txt', '--text_output', help='Output TXT file', default=None)

    args = parser.parse_args()

    input_pdf = args.input_pdf

    if args.text_output:
        output_txt = args.text_output
    else:
        output_txt = os.path.splitext(input_pdf)[0] + '.txt'

    pdf_to_text(input_pdf, output_txt)

if __name__ == '__main__':
    main()
