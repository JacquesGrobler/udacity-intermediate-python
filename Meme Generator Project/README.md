# Meme Generator 

## Overview
This program can be used to generate memes through a web interface or commend line. It can either generate memes using input from the user or generate random memes if no input is given. 

## Initial Set Up
The first step is to install dependencies. The below steps are for linux, they will be slightly different for other operating systems.

Install python3-venv to make use of a virtual environment:
```bash
apt-get install python3-venv -y
```
Install poppler-utils, which includes the pdftotext application that gets used in the program:
```bash
apt-get update
apt-get install poppler-utils
```
Set up a python 3.5 virtual environment:
```bash
python3.5 -m venv venv
```
Activate the virtual environment:
```bash
source venv/bin/activate
```
Install the pip packages listed in the requirements file:
```bash
pip3 install -r requirements.txt
```
To exit the virtual environment run:
```bash
deactivate
```

Ensure the virtual environment is activated when generating memes.

## Generate Memes
### Command Line
The code for the commadn line module can be found in meme.py.
The command line has three optional arguments:<br>
-- path: a path to the image that should be used in the meme.<br>
-- body: a quote to add to to image.<br>
-- author: the author of the quote. This argument is required if a body argument is provided. <br>

If arguments are not provided, random arguments will be passed in. Once the command has run, the path to the saved meme will be given.

An example of a valid command:
```bash
python3 meme.py --body "Bark like no one is listening" --author Rex --path _data/photos/dog/xander_1.jpg
```

### Web Interface
The code for the web interface can be found in app.py. 
It needs to be set up first by running the following commands:
```bash
export FLASK_APP=app.py
flask run --host 0.0.0.0 --port 3000 --reload
```
The page can then be accessed by pasting the below in your browser:
```bash
http://0.0.0.0:3000/
```

There are two options that can be selected:<br>
1. Random: to generate random memes.
2. Creator: to create your own memes by providing an image url, quote and author.

## Sub-Modules
The command line and web interface makes use of the QuoteEngine and MemeGenerator modules, which are explained below. 
### QuoteEngine
The QuoteEngine can be found in the QuoteEngine folder and makes use the following classes: <br>
- An abstract class used as a template for helper classes.
- Individual helper classes that ingest different file type, e.g. csv, docx, pdf and text. 
- A quotemodel class to encapsulate the body and author.
- The Ingestor module, which contains logic to implement the appropriate helper class based on the file type.

These modules can be run individually, here is an example of running the Ingestor module:<br>
First open the python interactor:
```bash
python3 -q
```
The following commands will create a list of quotes from a csv file (this can also be a text, pdf or docx file):
```python
from QuoteEngine import Ingestor
Ingestor.parse('_data/DogQuotes/DogQuotesCSV.csv')
```

### MemeGenerator
The MemGenerator class requires one argument when being initialized, which is the path to the desired output location of the generated meme. It has a make_meme method, which requires the path to the image being used and three optional arguments, namely: body (a quote to be added to the image), author (the autor of the quote, this is required if a body is provided) and size (the size of the image in pixels, the maximum and default value is 500). A random body and author will be used if they aren't provided.

An example:<br>
First open the python interactor:
```bash
python3 -q
```
The following commands will save the meme to the 'memes' directory.
```python
from MemeGenerator import MemeGenerator
meme = MemeGenerator('memes')
meme.make_meme('_data/photos/dog/xander_1.jpg', 'Bark like no one is listening', 'Rex')
```