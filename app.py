import random
import os

import requests
from flask import Flask, render_template, abort, request

from MemeGenerator.MemeEngine import MemeEngine
from QuoteEngine import csv_ingestor, txt_ingestor, pdf_ingestor, docx_ingestor

# @TODO Import your Ingestor and MemeEngine classes

app = Flask(__name__)

meme = MemeEngine('./static')

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
    for f in quote_files:
        for p in parsers:
            if(p.can_ingest(f)):
                quote_lines.append(p.parse(f))
                continue
    for qs in quote_lines:
        for q in qs:
            quotes.append(q)
    imgs = []
    images_path = "./_data/photos/dog/"
    with os.scandir(images_path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                imgs.append(entry.path)

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote[0], quote[1])
    return render_template('meme.html', path="static/out.jpg")


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """
    image_url = request.form.get('image_url')
    text = request.form.get('body')
    author = request.form.get('author')
    r = requests.get(image_url)
    tmp = f'./tmp/{random.randint(0, 100000000)}.png'

    with open(tmp, 'wb') as img:
        img.write(r.content)
    path = meme.make_meme(tmp, text, author)
    os.remove(tmp)

    return render_template('meme.html', path=path)

if __name__ == "__main__":
    app.run()

