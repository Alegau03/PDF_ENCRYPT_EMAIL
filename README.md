# PDF_ENCRYPT_EMAIL

For the script to work, create a folder in the main folder called "Encrypted"


The provided code is a Python program that performs the following actions:

1) PDF file encryption: The program prompts the user to enter a password to encrypt PDF files. It then searches for all PDF files in the current directory that have the extension ".pdf" and encrypts them using the specified password. The encrypted files are saved in the "Encrypted" directory.

2) Moving the encrypted files: After encrypting the PDF files, the program moves the encrypted files from the current directory to the "Encrypted" directory. This step is useful for keeping track of encrypted files.

3) Sending emails with encrypted files: The program uses the Yagmail library to send emails containing the encrypted files as attachments. For each encrypted file, the program prompts the user to enter a destination e-mail address. It then sends the e-mail with the encrypted attachment and a password to unlock it.

If you encounter problems do not exist and contact me
