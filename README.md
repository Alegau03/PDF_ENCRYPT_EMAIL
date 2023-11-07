# PDF_ENCRYPT_EMAIL

For the script to work, create a folder in the main folder called "Encrypted"


## 1. Text Extractor from PDF with Encryption and Emailing
This program is designed to automate the process of extracting text from PDF files, encrypting the extracted PDF files and emailing them to users, all in an efficient manner.

## 2. Text Extraction from PDF
It uses the PyMuPDF library (Fitz) to extract text from PDF files. Each page of the PDF is converted into a high-resolution PNG image using PyMuPDF.
Uses the Tesseract OCR library via the pytesseract module to extract text from PNG images, ensuring that the images are processed correctly to obtain accurate text.
Extracts a key from each PDF, which is specific to each document but shared among all (all have must have the wording Tax Code, for example):, using regular expressions to look for the string "TAX CODE :" within the extracted text.

## 3. PDF encryption.
Use the PyPDF2 library to encrypt each extracted PDF.
The password for encryption is set as the tax code extracted from the PDF.
Encrypted PDFs are renamed by adding "_protected" in the file name and saved in the "Encrypted" folder.

## 4. Sending via Email
Uses the yagmail library to send encrypted PDFs to users via email.
Requests the recipient's email address via a dialog box.
Includes a custom HTML message in the body of the email, providing information about the report and informing the user that the PDF is password protected, with the password set as the social security number.

## 5. User Interface.
Use the tkinter library to create a minimal user interface to prompt for the recipient's password and email address.
The user interface allows the user to enter this information before starting the extraction and sending process.

## 6. Library Requirements.
A "requirements.txt" file is included in the source code to list all the libraries needed to run the program. You can install them all by running pip install -r requirements.txt.
The program is designed to simplify the process of sharing medical reports or any type of PDF with users, while ensuring data security by encrypting PDFs.
