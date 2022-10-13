from PIL import Image, ImageDraw, ImageFont


class MemeEngine():

    def __init__(self, out_img_folder:str):
        self.out_img_folder = out_img_folder

    def make_meme(self, img_path, text, author, width=500):
        """Create a Meme With a quote

        Arguments:
            in_path {str} -- the file location for the input image.
            out_path {str} -- the desired location for the output image.
            crop {tuple} -- The crop rectangle, as a (left, upper, right, lower)-tuple. Default=None.
            width {int} -- The pixel width value. Default=None.
        Returns:
            str -- the file path to the output image.
        """
        img = Image.open(img_path)
        if(width <= 500):
            ratio = width / float(img.size[0])
            height = int(ratio * float(img.size[1]))
            img = img.resize((width, height), Image.NEAREST)
        if text is not None:
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype('./fonts/LilitaOne-Regular.ttf',
                                      size=20)
            draw.text((10, 30), text, font=font, fill='yellow')
            draw.text((20, 60), author, font=font, fill='black')
        img.save(self.out_img_folder + "/out.jpg")
        return self.out_img_folder + "/out.jpg"