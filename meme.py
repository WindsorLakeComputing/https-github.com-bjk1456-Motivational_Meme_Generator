"""Create a meme via the CLI."""
import os
import random
import argparse
import pathlib

from MemeGenerator.MemeEngine import MemeEngine
from QuoteEngine import csv_ingestor, pdf_ingestor, txt_ingestor, docx_ingestor
from QuoteModel import QuoteModel


def generate_meme(path, body, author):
    """Generate a meme given an path and a quote."""
    print(f"the path is {path}")
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path

    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
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
                if (p.can_ingest(f)):
                    quote_lines.append(p.parse(f))
                    continue
        for qs in quote_lines:
            for q in qs:
                quotes.append(q)

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeEngine('./static')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    # path - path to an image file
    # body - quote body to add to the image
    # author - quote author to add to the image
    parser = argparse.ArgumentParser(
        description="A simple cli app for Motivational Meme Generator"
    )

    parser.add_argument('--path', default="_data/photos/dog/xander_4.jpg",
                        type=pathlib.Path,
                        help="An image path")
    parser.add_argument('--body', default="To be or not to be",
                        help="A string quote body.")
    parser.add_argument('--author', default="",
                        help="A string quote author.")

    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
