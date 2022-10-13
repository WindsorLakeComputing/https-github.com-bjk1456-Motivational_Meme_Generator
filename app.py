import random
import os
from ctypes import Union

import requests
from flask import Flask, render_template, abort, request

from MemeGenerator.MemeEngine import MemeEngine
from QuoteEngine import csv_ingestor, txt_ingestor, pdf_ingestor, docx_ingestor

# @TODO Import your Ingestor and MemeEngine classes

app = Flask(__name__)

meme = MemeEngine('./static')
#meme = MemeEngine()

def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    # TODO: Use the Ingestor class to QuoteEngine all files in the
    # quote_files variable
    _csv = csv_ingestor()
    _pdf = pdf_ingestor()
    _txt = txt_ingestor()
    _docx = docx_ingestor()
    parsers = []
    parsers.append(_csv)
    parsers.append(_pdf)
    parsers.append(_txt)
    parsers.append(_docx)
    quotes = []
    quote_lines = []
    #parsers = list[Union[csv_ingestor, pdf_ingestor, txt_ingestor, docx_ingestor]]
    #ps = list[Union[csv_ingestor, pdf_ingestor, txt_ingestor, docx_ingestor]]
    for f in quote_files:
        print(f"f is {f}")
        for p in parsers:
            if(p.can_ingest(f)):
                print("SHHHHHHHHHHHHHHHHHHOUT")
                quote_lines.append(p.parse(f))
                continue
    print(f"quote_lines are {quote_lines}")
    for qs in quote_lines:
        print(f"QQQQQ is {qs}")
        for q in qs:
            quotes.append(q)
    imgs = []
    images_path = "./_data/photos/dog/"
    with os.scandir(images_path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                imgs.append(entry.path)

    # TODO: Use the pythons standard library os class to find all
    # images within the images images_path directory
    for i in imgs:
        print(f"the i is {i}")

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    # @TODO:
    # Use the random python standard library class to:
    # 1. select a random image from imgs array
    # 2. select a random quote from the quotes array

    img = random.choice(imgs)
    quote = random.choice(quotes)
    print(f"Inside meme_rand ... the quote is {quote[0]}")
    print(f"Inside meme_rand ... the author is {quote[1]}")
    print(f"Inside meme_rand ... the img is {img}")
    path = meme.make_meme(img, quote[0], quote[1])
    print(f"the path is {path}")
    return render_template('meme.html', path="static/out.jpg")


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """

    # @TODO:
    # 1. Use requests to save the image from the image_url
    #    form param to a temp local file.
    # 2. Use the meme object to generate a meme using this temp
    #    file and the body and author form paramaters.
    # 3. Remove the temporary saved image.

    image_url = request.form.get('image_url')
    text = request.form.get('body')
    author = request.form.get('author')

    print(f"the image_url is {image_url}")
    print(f"the text is {text}")
    print(f"the author is {author}")

    r = requests.get(image_url)
    tmp = f'./tmp/{random.randint(0, 100000000)}.png'

    with open(tmp, 'wb') as img:
        img.write(r.content)

    # This approach will also work:
    # img = open(tmp, 'wb')
    # img.write(r.content)
    # img.close()

    path = meme.make_meme(tmp, text, author)

    print(tmp)

    os.remove(tmp)

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
    #setup()

