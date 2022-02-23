"""Generates memes."""
from PIL import Image, ImageDraw, ImageFont
import random
import textwrap
import os


class MemeGenerator:
    """Generate meme and save it to given output path."""

    def __init__(self,
                 out_path):
        """Initialize output path variable."""
        self.out_path = out_path

    def make_meme(self, img_path, text=None, author=None, width=500) -> str:
        """Create a meme.

        Arguments:
            img_path {str} -- the file location for the input image.
            text {str} -- quote to be added to the image. Default=None.
            author {str} -- author of the quote. Default=None.
            width {int} -- The pixel width value. Default=None.
        Returns:
            str -- the file path to the output meme.
        """
        img = Image.open(img_path)

        if width > 500:
            raise ValueError('width must be smaller than 500px')
        else:
            ratio = width/float(img.size[0])
            height = int(ratio*float(img.size[1]))
            img = img.resize((width, height), Image.NEAREST)

        if (text is not None) and (author is not None):
            draw = ImageDraw.Draw(img)

            font = ImageFont.\
                truetype("./fonts/FreeMonoBold.ttf", 20)

            wrapped_text = textwrap.wrap(text, width=30)
            wrapped_text.append(' - {}'.format(author))
            text_position_x = random.randint(10, 120)
            text_position_y = random.randint(10, 300)

            for line in wrapped_text:
                draw.text((text_position_x,
                           text_position_y),
                          '{}'.format(line),
                          font=font,
                          fill='white')
                text_position_y += 20

        elif (text is not None) and (author is None):
            raise Exception('Author Required if Quote is Used')

        try:
            os.mkdir(self.out_path)
            print("'{} created, saving image.'\n".format(self.out_path))
        except Exception as e:
            print("'{}' exists, saving image.\n".format(self.out_path))

        out_path = '{}/meme.jpg'.format(self.out_path)

        img.save(out_path)
        print('image saved to: ')
        return out_path
