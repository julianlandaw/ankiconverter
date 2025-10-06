cp print.html original.html
python3 runcode.py
mv formatted.html anki.html
wkhtmltopdf --enable-local-file-access anki.html anki.pdf
pandoc anki.html -o anki.docx
