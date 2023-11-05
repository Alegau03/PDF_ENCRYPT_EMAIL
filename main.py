import os
import shutil
import PyPDF2 as p
import yagmail
import time
import tkinter as tk
from tkinter import simpledialog

def encrypt(pdf, passw):
    # Il tuo codice di crittografia qui
    writer=p.PdfWriter()
    reader = p.PdfReader(pdf)
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(passw)
    with open(pdf[:-4]+"_encypted.pdf", "wb") as f:
        writer.write(f)

def move():
    # Il tuo codice di spostamento qui
    stringa_finale = "_encrypted.pdf"
    file_con_stringa_finale = [file for file in os.listdir() if file.endswith(stringa_finale)]
    for file in file_con_stringa_finale:
        new_path = 'Encrypted/' + file
        shutil.move(file, new_path)

def main():
    root = tk.Tk()
    root.withdraw()  # Nasconde la finestra principale di Tkinter

    passw = simpledialog.askstring("Password", "Insert password for PDF:")
    if passw is None:
        return

    pdfs = [f for f in os.listdir() if f.lower().endswith('.pdf')]
    for pdf in pdfs:
        encrypt(pdf, passw)
    move()

    time.sleep(1)

    sender = 'youremail@example.com'
    yag = yagmail.SMTP(user=sender, password="yourpassword")

    cartella = "Encrypted_FolderPath"
    elenco_file = os.listdir(cartella)
    stringa_finale = "_encrypted.pdf"
    file_con_stringa_finale = [file for file in elenco_file if file.endswith(stringa_finale)]

    for file in file_con_stringa_finale:
        time.sleep(2)
        stringa = f"Insert email for {file} : "
        email_tmp = simpledialog.askstring(f"Email for {file}", stringa)
        if email_tmp is None:
            continue

        oggetto = "OBJECT"
        contenuto = f"""BODY """
        allegato = os.path.join(cartella, file)
        yag.send(to=email_tmp, subject=oggetto, contents=contenuto, attachments=allegato)
       

if __name__ == "__main__":
    main()
