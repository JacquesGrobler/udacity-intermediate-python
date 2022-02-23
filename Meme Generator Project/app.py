"""App used to generate memes."""
import random
import os
import requests
from flask import Flask, render_template, abort, request

from MemeGenerator import MemeGenerator
from QuoteEngine import Ingestor

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

meme = MemeGenerator('./static')


def setup():
    """Load all resources."""
    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    quotes = []
    for f in quote_files:
        quotes.extend(Ingestor.parse(f))

    images_path = "./_data/photos/dog/"

    imgs = []
    for root, dirs, files in os.walk(images_path):
        imgs = [os.path.join(root, name) for name in files]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme."""
    img = random.choice(imgs)
    quote = str(random.choice(quotes))
    quote_list = quote.split(',')
    body = ', '.join(quote_list[:-1])
    author = quote_list[-1]
    path = meme.make_meme(img, body, author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme."""
    image_url = request.form.get('image_url')
    body = request.form.get('body')
    author = request.form.get('author')

    try:
        r = requests.get(image_url)

        try:
            os.mkdir('./tmp')
        except Exception:
            print('directory already exists.')

        tmp = './tmp/{}.png'.format(random.randint(0, 100000000))

        with open(tmp, 'wb') as img:
            img.write(r.content)

        path = meme.make_meme(tmp, body, author)
        os.remove(tmp)
        return render_template('meme.html', path=path)

    except Exception:
        path = './static/invalid_url.jpg'
        return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
