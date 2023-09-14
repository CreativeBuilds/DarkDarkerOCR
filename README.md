# Dark Darker OCR

This is a python script designed to extract prices and items sales from screenshots of Dark and Darker trade chat


# Install

You'll need [tesseract](https://github.com/tesseract-ocr/tesseract) installed on your system.

Use virtualenv

```bash
virtualenv -p python3 venv
source venv/bin/activate
```

or windows

```bash
virtualenv -p python3 venv
venv\Scripts\activate
```

then pip install

```bash
pip install -r requirements.txt
```

after that place your images in the `images` folder and run the script

```bash
python run.py
```