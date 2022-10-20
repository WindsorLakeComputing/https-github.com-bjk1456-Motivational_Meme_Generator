"""Create a Meme that contains: an image, a quote, and an author."""

from PIL import Image, ImageDraw, ImageFont
from random import randint
import textwrap


class MemeEngine():
    """Create a Meme."""

    def __init__(self, out_img_folder: str):
        """:param out_img_folder: The directory to store the created memes."""
        self.out_img_folder = out_img_folder

    def make_meme(self, in_path, text, author, width=500):
        """Create a Meme With a quote.

        Arguments:
            in_path {str} -- the file location for the input image.
            text {str} -- The actual quote.
            author {str} -- The author of the quote.
            width {int} -- The pixel width value. Default=None.
        Returns:
            str -- the file path to the output image.
        """
        img = self.read(in_path)

        if(width <= 500):
            img = self.resize_img(img, width)

        if text is not None:
            self.draw(img, text, author)

        meme_file = f'{self.out_img_folder}/{randint(0, 100000000)}.jpg'
        img.save(meme_file)
        return meme_file

    def read(selfself, img_path):
        """Open the file of the image that will be modified with the quote.

        :param img_path: The path to the file that will be modified.
        """
        return Image.open(img_path)

    def resize_img(self, img, width):
        """Change the dimensions of the image.

        :param img: The image that will be modified.
        :width: The new width of the image
        """
        ratio = width / float(img.size[0])
        height = int(ratio * float(img.size[1]))
        return img.resize((width, height), Image.NEAREST)

    def draw(self, img, text, author):
        """Draw the new meme.

        :param img: The image that will be modified.
        :text: The quote to be painted on the image.
        :author: THe author of the quote.
        """
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('./fonts/LilitaOne-Regular.ttf',
                                  size=20)
        h, w = img.size
        four_fifths = int(w * .8)
        one_fifth = w * .20
        rand_x = randint(1, four_fifths)
        if((len(text) * 6) > one_fifth):
            wrap_amount = one_fifth / 6
            text = textwrap.fill(text=text, width=wrap_amount)
            draw.text((rand_x + 10, rand_x + 80), author, font=font,
                      fill='black')
        else:
            draw.text((rand_x + 10, rand_x + 40), author, font=font,
                      fill='black')
        draw.text((rand_x, rand_x + 20), text, font=font, fill='yellow')
