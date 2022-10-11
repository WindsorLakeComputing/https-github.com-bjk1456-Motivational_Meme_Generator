import random
import os
from ctypes import Union

import requests
from flask import Flask, render_template, abort, request
from parse import ingestor_interface
from parse import csv_ingestor, txt_ingestor, pdf_ingestor, docx_ingestor

# @TODO Import your Ingestor and MemeEngine classes

app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    # TODO: Use the Ingestor class to parse all files in the
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
                quote_lines.append(p.parse(f))
                continue
    for qs in quote_lines:
        print(f"QQQQQ is {qs}")
        for q in qs:
            quotes.append(q)

    for q in quotes:
        print(f"the q is {q}")
    images_path = "./_data/photos/dog/"

    # TODO: Use the pythons standard library os class to find all
    # images within the images images_path directory
    imgs = None

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    # @TODO:
    # Use the random python standard library class to:
    # 1. select a random image from imgs array
    # 2. select a random quote from the quotes array

    img = None
    quote = None
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


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

    path = None

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    #app.run()
    setup()

