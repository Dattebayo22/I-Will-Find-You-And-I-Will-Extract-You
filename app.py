import requests
import json
import os
import PyPDF2
import sys
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/test')
def test():
    book_id_file = "extracted_url.txt"
    api_key = "googlecouldapikey"  # Replace with your Google Cloud API key
    output_file = "isbn_data.txt"
    page_number_file = "extracted_url.txt"  
    get_isbn_and_save(book_id_file, api_key, output_file)
    folder_path = r"" # Replace with your files folder path
    pdf_texts = extract_text_from_pdfs(folder_path, file_name_contains, page_number_file)

    output_text_file = 'extracted_text_from_the_desired_page.txt'

    with open(output_text_file, 'w', encoding='utf-8') as output_file:
        for pdf_text in pdf_texts:
            output_file.write(f"File: {pdf_text['filename']}\n")
            output_file.write(pdf_text['text'] + '\n')
            output_file.write("-" * 30 + '\n')

    print(f"Extracted text saved to {output_text_file}")


def get_isbn_and_save(book_id, api_key, output_file):

    base_url = "https://www.googleapis.com/books/v1/volumes/"
    url = f"{base_url}{book_id}?key={api_key}"

    response = requests.get(url)
    print("Here")
    if response.status_code == 200:
        book_data = response.json()
        if 'volumeInfo' in book_data and 'industryIdentifiers' in book_data['volumeInfo']:
            identifiers = book_data['volumeInfo']['industryIdentifiers']
            for identifier in identifiers:
                if identifier['type'] == 'ISBN_13':
                    isbn = identifier['identifier']
                    break
            with open(output_file, 'w') as json_file:
                json.dump({'isbn': isbn}, json_file, indent=2)

            print(f"ISBN successfully extracted and saved to {output_file}")
            return isbn
        else:
            print("Error: ISBN not found in book data")
            return None
    else:
        print(f"Error: {response.status_code}")
# 
def extract_text_from_pdfs(folder_path, isbn, page_number):
    pdf_texts = []
    #print("Here")
    try:
            page_number = int(page_number)
            for filename in os.listdir(folder_path):
                if filename.endswith(".pdf") and isbn in filename:
                    file_path = os.path.join(folder_path, filename)
                    with open(file_path, "rb") as file:
                        pdf_reader = PyPDF2.PdfReader(file)

                        if 0 < page_number <= len(pdf_reader.pages):
                            text = pdf_reader.pages[page_number - 1].extract_text()

                            pdf_texts.append({"filename": filename, "text": text})
                           
                        else:
                            print(f"Error: Invalid page number {page_number} for file {filename}. "
                                f"Total pages in document: {len(pdf_reader.pages)}. Skipping.")
                else:
                    print(f"Error: Insufficient lines in {page_number}. Please provide a valid page number.")

    except ValueError:
        print(f"Error: Invalid page number '{page_number}' in {page_number}. Please provide a valid integer.")



    return pdf_texts

@app.route("/get/<id>/<page>")
def apply(id,page):
    book_id_file = "extracted_url.txt"
    api_key = "" #use api key here
    output_file = "isbn_data.txt"
    page_number_file = "extracted_url.txt" 

    isbn=get_isbn_and_save(id, api_key, output_file)
    folder_path = r"" #replace with the files folder path
    file_name_contains = "9789332516328"  
    
    pdf_texts = extract_text_from_pdfs(folder_path, isbn, page)
    output_text_file = 'extracted_text_from_the_desired_page.txt'

    with open(output_text_file, 'w', encoding='utf-8') as output_file:
        for pdf_text in pdf_texts:
            output_file.write(f"File: {pdf_text['filename']}\n")
            output_file.write(pdf_text['text'] + '\n')
            output_file.write("-" * 30 + '\n')

    
        
    return f"Extracted text saved to {output_text_file}"



# if __name__ == "__main__":
    app.run(debug=True)





