# Vanguard Bot Tool AI

## Requirements

| Tool | Why? | Where? |
| --- | --- | --- |
| Python 3 | Python language interpreter | [Download](https://www.python.org/downloads/) |
| Tesseract 3 Portable | Text recognition service | [Download](https://github.com/maxshymchuk/bf1-vg-bot/releases/tag/tesseract) |
| Pre-trained data | PyTorch models and weights | [Download](https://github.com/maxshymchuk/bf1-vg-bot/releases/tag/models) |

## Installation

### If you want to run the bot

1. Download and place packages

   Download all the required packages, unzip them and place the files in the following order: tesseract binaries in the `tesseract` folder, pre-trained data files in the `models` folder

3. Install dependencies

   Run `pip install -r requirements.txt`

4. Run the script

   Run `python .\main.py` to enable the bot


### If you want to train the bot

1. Install dependencies

   Run `pip install -r requirements.training.txt` 

2. Run the script
   
   Run `python .\train\train.py` to start training process


