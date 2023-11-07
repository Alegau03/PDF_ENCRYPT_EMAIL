import os
import shutil
import PyPDF2 as p
import yagmail
import time
import tkinter as tk
from tkinter import simpledialog
import fitz  # Modulo PyMuPDF
from PIL import Image
import pytesseract
import enum
import re  # Importa il modulo re per le espressioni regolari

class OS(enum.Enum):
    Mac = 0
    Windows = 1

class Language(enum.Enum):
    ENG = 'eng'
    ITA = 'ita'

class ImageReader:
    def __init__(self, os: OS):
        if os == OS.Windows:
            windows_path = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' #may change depending on the installation path
            pytesseract.pytesseract.tesseract_cmd = windows_path

    def convert_pdf_to_png(self, pdf_path: str, output_folder: str):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        documento_pdf = fitz.open(pdf_path)
        for pagina_num in range(documento_pdf.page_count):
            pagina = documento_pdf.load_page(pagina_num)
            immagine = pagina.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))
            immagine_png = Image.frombytes("RGB", [immagine.width, immagine.height], immagine.samples)
            percorso_immagine = os.path.join(output_folder, f"pagina_{pagina_num + 1}.png")
            immagine_png.save(percorso_immagine)
        documento_pdf.close()

    def extract_text_from_png(self, image_path: str, lang: str) -> str:
        img = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(img, lang=lang)
        return extracted_text

    def extract_codice_fiscale(self, text: str) -> str:
        pattern = r"CODICE FISCALE : ([^\n]+)"
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        return ""

    def convert_pdf_and_extract_codice_fiscale(self, pdf_path: str, output_folder: str, lang: str) -> str:
        self.convert_pdf_to_png(pdf_path, output_folder)
        extracted_text = ""
        for root, _, files in os.walk(output_folder):
            for file in files:
                if file.lower().endswith(".png"):
                    image_path = os.path.join(root, file)
                    extracted_text += self.extract_text_from_png(image_path, lang)
        codice_fiscale = self.extract_codice_fiscale(extracted_text)
        codice_fiscale = codice_fiscale.replace(" ", "").lower()
        return codice_fiscale

def encrypt(pdf, passw):
    writer = p.PdfWriter()
    reader = p.PdfReader(pdf)
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(passw)
    encrypted_pdf = pdf[:-4] + "_protetto.pdf"
    with open(encrypted_pdf, "wb") as f:
        writer.write(f)
    return encrypted_pdf

def move():
    stringa_finale = "_protetto.pdf"
    file_con_stringa_finale = [file for file in os.listdir() if file.endswith(stringa_finale)]
    for file in file_con_stringa_finale:
        new_path = 'Encrypted/' + file
        shutil.move(file, new_path)

def main():
    root = tk.Tk()
    root.withdraw()

    pdfs = [f for f in os.listdir() if f.lower().endswith('.pdf')]
    for pdf in pdfs:
        ir = ImageReader(OS.Windows)
        pdf_path = pdf
        output_folder = 'cartella_immagini'
        lang = 'ita'
        codice_fiscale = ir.convert_pdf_and_extract_codice_fiscale(pdf_path, output_folder, lang)
        encrypted_pdf = encrypt(pdf, codice_fiscale)
    move()
    print("File protetti e spostati")
    time.sleep(1)

    ################################################################################
    ################################################################################
    sender = 'youremail@example.com'                #INSERIRE NUOVI PARAMETRI
    yag = yagmail.SMTP(user=sender, password="your password")
    ################################################################################
    ################################################################################


    cartella = "Encrypted/"
    elenco_file = os.listdir(cartella)
    stringa_finale = "_protetto.pdf"
    file_con_stringa_finale = [file for file in elenco_file if file.endswith(stringa_finale)]

    for file in file_con_stringa_finale:
        time.sleep(2)
        stringa = f"INSERISCI L'EMAIL PER {file} : "
        email_tmp = simpledialog.askstring(f"Email per {file}", stringa)
        if email_tmp is None:
            continue

        oggetto = "INVIO REFERTO - Fisiogym"
        contenuto = """
                        <html>
                        <head></head>
                        <body>
                        <img src='https://imgur.com/a/3Kpmnwp' alt="Logo" width="200"><br>
                        <p style="font-size: 20px; font-weight: bold;">Fisiogym Referti Online</p>
                        <p style="font-size: 12px;">Buonasera, il centro medico Fisiogym augurandole una buona giornata le invia il referto dell'esame effettuato presso la nostra struttura.</p>
                        <p style="font-size: 12px;"><strong>ATTENZIONE il pdf è protetto da password!</strong></p>
                        <p style="font-size: 12px;">La password è il tuo codice fiscale scritto in minuscolo.</p>

                        <br><br>
                        <em style="font-size: 14px; font-family: 'Courier New', monospace;">Centro Medico Diagnostico Fisiogym</em>
                        </body>
                        </html>
                    """
        allegato = os.path.join(cartella, file)
        yag.send(to=email_tmp, subject=oggetto, contents=contenuto, attachments=allegato)
        print("Email inviata per:", file)

if __name__ == "__main__":
    main()