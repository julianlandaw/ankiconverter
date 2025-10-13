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
replace_text = 'loading="lazy" alt="" src="Images/'
html_string = replacetext(html_string, search_text, replace_text)

soup = BeautifulSoup(html_string,'html.parser');

divs = soup.find_all('td',attrs={"width": "33.333333333333336%"})

preamble = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>Anki Deck | Welcome!</title>
    <meta charset="utf-8">
    
    <style>
      #bottom-toolbar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #333;
        padding: 10px;
        display: none; /* Hidden by default */
        flex-wrap: wrap;
        justify-content: center;
        gap: 8px;
        z-index: 1000;
      }
    
      #bottom-toolbar button {
        background-color: #555;
        color: white;
        border: none;
        padding: 8px 12px;
        cursor: pointer;
        font-size: 14px;
        border-radius: 4px;
      }
    
      #bottom-toolbar button:hover {
        background-color: #777;
      }
    
      #toolbar-toggle {
        position: fixed;
        bottom: 60px;
        right: 20px;
        background-color: #007bff;
        color: white;
        border: none;
        padding: 10px 14px;
        border-radius: 50%;
        font-size: 18px;
        cursor: pointer;
        z-index: 1001;
      }

      img {
        max-width: 50vw;     /* Max width: 50% of viewport width */
        max-height: 50vh;    /* Max height: 50% of viewport height */
        width: auto;
        height: auto;
        object-fit: contain;
        display: block;
        margin: 1em auto;
        loading: lazy;
      }
        
      .zoomable {
        cursor: zoom-in;
        transition: transform 0.3s ease;
      }

      .zoomed {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        max-width: 90vw;
        max-height: 90vh;
        width: auto;
        height: auto;
        z-index: 1001;
        box-shadow: 0 0 20px rgba(0,0,0,0.5);
        cursor: zoom-out;
      }

      .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0,0,0,0.6);
        z-index: 1000;
        display: none;
      }
    </style>
</head>
"""

buttons = """<!-- Toggle Button -->
<button id="toolbar-toggle">☰</button>

<div id="bottom-toolbar">
"""

javascript = """<!-- JavaScript -->
<script>
  const toggleBtn = document.getElementById('toolbar-toggle');
  const toolbar = document.getElementById('bottom-toolbar');

  toggleBtn.addEventListener('click', () => {
    toolbar.style.display = toolbar.style.display === 'flex' ? 'none' : 'flex';
  });
</script>
<script>
  document.addEventListener("DOMContentLoaded", function () {
    const images = document.querySelectorAll("img");
    const overlay = document.createElement("div");
    overlay.className = "overlay";
    document.body.appendChild(overlay);

    images.forEach(img => {
      img.classList.add("zoomable");
      img.addEventListener("click", () => {
        if (img.classList.contains("zoomed")) {
          img.classList.remove("zoomed");
          overlay.style.display = "none";
        } else {
          img.classList.add("zoomed");
          overlay.style.display = "block";
        }
      });
    });

    overlay.addEventListener("click", () => {
      document.querySelectorAll(".zoomed").forEach(img => img.classList.remove("zoomed"));
      overlay.style.display = "none";
    });
  });
</script>
"""


body = """<body id="home">

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
    body = body + '<section id="Q' + str(qcount+1) + '">(' + str(qcount+1) + '):<br>' + question + '<hr><hr></section>'
    buttons = buttons + """<button onclick="location.href='#Q""" + str(qcount+1) + """'">Q""" + str(qcount+1) + """</button>"""
    qcount = qcount+1

buttons = buttons + """</div>"""

html_stringout = preamble + buttons + javascript + body + conclusion
soup = BeautifulSoup(html_stringout, 'html.parser')
pretty_html = soup.prettify()

text_file = open("formatted.html", "w")
n = text_file.write(pretty_html)
text_file.close()