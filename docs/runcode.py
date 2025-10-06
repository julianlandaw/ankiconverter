# Importing Path from pathlib2 module
from pathlib2 import Path
from bs4 import *
import requests
import os
  
# Creating a function to
# replace the text in a string
def replacetext(string, search_text, replace_text):
    retstring = string
    ind = retstring.find(search_text)
    strlength = len(search_text)
    while (ind > -1):
        retstring = retstring[0:ind] + replace_text + retstring[(ind+strlength):]
        ind = retstring.find(search_text)
    return retstring    
  
with open('original.html', 'r') as f:
    html_string = f.read()
f.close()    

search_text = "<center>"
replace_text = "<left>"
html_string = replacetext(html_string, search_text, replace_text)

search_text = "</center>"
replace_text = "</left>"
html_string = replacetext(html_string, search_text, replace_text)

search_text = "</left></td><td w"
replace_text = "</left></td></tr><tr><td w"
html_string = replacetext(html_string, search_text, replace_text)

search_text = '%20'
replace_text = ' '
html_string = replacetext(html_string, search_text, replace_text)

search_text = 'src="'
replace_text = 'src ="/Users/julianlandaw/Library/Application Support/Anki2/JLandaw/collection.media/'
html_string = replacetext(html_string, search_text, replace_text)

soup = BeautifulSoup(html_string,'html.parser');
    
images = soup.find_all('img')

print("\n\n*** Copying Images ***\n\n") 
for i, image in enumerate(images):
    os.system('cp ' + '\'' + images[i]["src"] + '\'' + ' Images')
print("*** Images Received ***\n\n")

search_text = 'src ="/Users/julianlandaw/Library/Application Support/Anki2/JLandaw/collection.media/'
replace_text = 'style= "max-height: 500px; max-width: 75%; object-fit: contain" src ="Images/'
html_string = replacetext(html_string, search_text, replace_text)

soup = BeautifulSoup(html_string,'html.parser');

divs = soup.find_all('td',attrs={"width": "33.333333333333336%"})

preamble = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Anki Deck</title>
</head>
<body id="home">

    <article style="margin:2%;">
    """

conclusion = """</article>
    <!-- Page Footer -->
    <footer class="page-footer">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-sm-6">
                    <p>Copyright <script>document.write(new Date().getFullYear())</script> &copy; Julian Landaw</p>
                </div>
            </div>
        </div>
    </footer> 
    <!-- End of page footer -->
</body></html>"""


html_stringout = preamble

questions = []

for i in range(len(divs)):
    tempstr = str(divs[i])
    tempstr = tempstr[38:len(tempstr)-12]
    ind = tempstr.find('<hr id="answer"/>')
    if (ind > 0):
        questions.append(tempstr)

qcount = 0
for i in range(len(questions)):
    question = questions[i]
    length = len(question)
    html_stringout = html_stringout + "<p>(" + str(qcount+1) + "):<br>" + question + "<hr><hr></p>"
    qcount = qcount+1

html_stringout = html_stringout + conclusion

text_file = open("formatted.html", "w")
n = text_file.write(html_stringout)
text_file.close()