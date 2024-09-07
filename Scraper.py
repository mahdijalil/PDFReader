from bs4 import BeautifulSoup
import os
from PyPDF2 import PdfReader
import re

# Define the folders
starting_folder = "StartingFolders"
organized_folder = "Organized"

# Ensure the organized folder exists
os.makedirs(organized_folder, exist_ok=True)

# Function to extract the title from the cover page
def get_pdf_title(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        first_page = reader.pages[0]
        text = first_page.extract_text()  # Extract the text of the first page
    
    # Search for the pattern "WX" followed by 4 digits
    match = re.search(r'WX\d{4}', text)
    
    if match:
        return match.group(0)  # Return the first match
    else:
        return None  # Return None if no match is found

# Process each PDF file in the starting folder
for filename in os.listdir(starting_folder):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(starting_folder, filename)
        
        title = get_pdf_title(pdf_path)
        if title == None:
            title = filename
        
        print(title)
        # Create a new folder inside organized_folder using the PDF filename without the extension
        new_folder_name = os.path.splitext(filename)[0]
        new_folder_path = os.path.join(organized_folder, new_folder_name)
        os.makedirs(new_folder_path, exist_ok=True)

        # Define the new PDF path inside the newly created folder
        new_pdf_path = os.path.join(new_folder_path, f"{title}.pdf")

        # Copy the PDF file to the new location with the title as the filename
        with open(pdf_path, 'rb') as src_file:
            with open(new_pdf_path, 'wb') as dst_file:
                dst_file.write(src_file.read())

        print(f"Organized '{filename}' as '{new_pdf_path}'")

print("PDF files have been organized.")
