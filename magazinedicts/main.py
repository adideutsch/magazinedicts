import PyPDF2
import textract
import os
from google_trans_new import google_translator
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from cachier import cachier
from time import sleep
import csv

MAGAZINE_DIR = "/Users/adideutsch/Downloads/eco_mag/"

NUMBER_TOP_WORDS = 1500


@cachier()
def parse_pdf(filepath):
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
        print(
            "Processing pdf using tesseract, this is going to take some time...")
        text = textract.process(filepath, method="tesseract",
                                language="eng").decode("utf-8")

    return text


@cachier()
def in_hebrew(en_word):
    print("waiting for API to rest")
    sleep(3)
    translator = google_translator()
    return translator.translate(en_word, lang_tgt="he")


def main():
    all_filenames = [filename for filename in os.listdir(MAGAZINE_DIR)]
    pdf_filenames = [
        filename for filename in all_filenames if "eco" in filename and "pdf" in filename
    ]
    pdf_full_paths = [os.path.join(MAGAZINE_DIR, filename) for filename in pdf_filenames]

    words_counter = {}

    for filepath in pdf_full_paths:

        text = parse_pdf(filepath)

        texts_words = filter(lambda x: len(x) > 3, [
            str(x.strip().strip(":-&,.'")).lower() for x in text.split()
        ])

        for word in texts_words:
            words_counter[word] = words_counter.setdefault(word, 0) + 1

        # print(text[:500])

    # print(words_counter)

    all_words = list(words_counter.keys())
    all_words.sort(key=lambda x: words_counter[x], reverse=True)

    top_words = all_words[:NUMBER_TOP_WORDS]

    print(top_words)

    top_words_full = [(x, words_counter[x], in_hebrew(x)) for x in top_words]
    print(top_words_full)

    print("Export to csv")

    csv_path = os.path.join(MAGAZINE_DIR, "output.csv")

    PAIR_COLUMNS_IN_PAGE = 6
    ROWS_IN_PAGE = 30
    top_words_full.sort(key=lambda x: x[0])
    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        # writer.writerow(["SN", "Name", "Contribution"]) # Title
        counter = 0
        current_row = []
        for word_data in top_words_full:
            if counter > 0 and counter % 6 == 0:
                writer.writerow(current_row)
                current_row = []
            current_row += [word_data[0], word_data[2]]
            counter += 1


if __name__ == "__main__":
    main()
