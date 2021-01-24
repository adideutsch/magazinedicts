import PyPDF2
import textract
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

MAGAZINE_DIR = "/Users/adideutsch/Downloads/eco_mag/"

all_filenames = [filename for filename in os.listdir(MAGAZINE_DIR)]
pdf_filenames = [
    filename for filename in all_filenames if "eco" in filename and "pdf" in filename
]
pdf_full_paths = [os.path.join(MAGAZINE_DIR, filename) for filename in pdf_filenames]

for filepath in pdf_full_paths:
    # filename = '/Users/adideutsch/Downloads/eco_mag/eco_feb_2_2019.pdf'
    pdfFileObj = open(filepath, "rb")

    # The pdfReader variable is a readable object that will be parsed.
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # Discerning the number of pages will allow us to parse through all the pages.
    num_pages = pdfReader.numPages
    count = 0
    text = ""

    # The while loop will read each page.
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count += 1
        text += pageObj.extractText()

    # This if statement exists to check if the above library returned words. It's done because PyPDF2 cannot read scanned files.
    if text != "":
        text = text
    # If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text.
    else:
        text = textract.process(filepath, method="tesseract", language="eng")

    # Now we have a text variable that contains all the text derived from our PDF file. Type print(text) to see what it contains. It likely contains a lot of spaces, possibly junk such as '\n,' etc.
    # Now, we will clean our text variable and return it as a list of keywords.

    print(text)
