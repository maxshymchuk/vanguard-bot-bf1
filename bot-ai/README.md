# Vanguard Bot Tool AI

## Requirements

| Tool | Why? | Where? |
| --- | --- | --- |
| Python 3 | Python language interpreter | [Download](https://www.python.org/downloads/) |
| Tesseract 3 Portable | Text recognition service | [Download](https://sourceforge.net/projects/tesseract-ocr-alt/files/tesseract-ocr-3.02-win32-portable.zip/download) |

## Installation

### If you want to run the bot

1. Install dependencies
   
   Run `pip install -r requirements.txt`

2. Place Tesseract OCR binaries
   
   Unzip the downloaded `tesseract-ocr-...-portable.zip` and place all files in the `tesseract` folder in the root of this project

3. Run the script

   Run `python .\main.py` to enable the bot


### If you want to train the bot

1. Install dependencies

   Run `pip install -r requirements.training.txt` 

2. Run the script
   
   Run `python .\train\train.py` to start training process


