from PIL import Image
from pytesseract import pytesseract
import os
import re
import colorlog
import logging

path_to_tesseract = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

pytesseract.tesseract_cmd = path_to_tesseract

path_to_images = r"images/"

# Create a logger with colorized output
logger = logging.getLogger(" ")
logger.setLevel(logging.INFO)

# Define custom log colors
LOG_COLORS = {
    'ITEMS_COLOR': '\033[96m',    # Cyan for 'Items'
    'PRICE_COLOR': '\033[93m',    # Yellow for 'Price'
    'NAME_COLOR': '\033[92m',     # Green for 'Seller/Buyer'
    'RESET_COLOR': '\033[0m',     # Reset color
    'WHITE': '\033[97m',          # White color for tags
}


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_color = LOG_COLORS.get(record.name, LOG_COLORS['RESET_COLOR'])
        log_msg = super(ColoredFormatter, self).format(record)
        return f"{log_color}{log_msg}{LOG_COLORS['RESET_COLOR']}"

handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter(
    '%(message)s'
))

logger.addHandler(handler)

for root, dirs, file_names in os.walk(path_to_images):
    for filename in file_names:
        img = Image.open(path_to_images + filename)
        text = pytesseract.image_to_string(img)
        chat_messages = text.split("\n")

        # Initialize lists to store extracted data
        cleaned_messages = []

        # Regular expressions to extract item, price, and seller's name
        item_pattern = r'\[(.*?)\]'
        price_pattern = r'(\d+)G'
        name_pattern = r'^([^:]+?)\s*:'

        for message in chat_messages:
            # Extract item, price, and seller's name using regular expressions
            item_matches = re.findall(item_pattern, message)
            price_match = re.search(price_pattern, message, re.IGNORECASE)
            name_match = re.search(name_pattern, message)

            if item_matches:
                if name_match:
                    name = name_match.group(1).strip()
                else:
                    name = "Unknown"
                
                # Check if the message contains a price
                price = price_match.group(1) if price_match else None
                items = [item.strip() for item in item_matches if item.strip()]

                # remove all items that include text "Item" or "item" or "|/Q"
                items = [item for item in items if "Item" not in item and "item" not in item and "|/Q" not in item and " Name " not in item and " Rarity " not in item]

                if len(items) == 0:
                    continue

                if price:
                    try:
                        price = int(price)
                    except ValueError:
                        price = price    
                # if price is none set to wts or wtb
                if not price:
                    if "WTS" in message:
                        price = "WTS"
                    elif "WTB" in message:
                        price = "WTB"
                cleaned_messages.append({
                    "items": items,
                    "price": price,
                    "name": name
                })
        
        # Prety Print extracted data
        print("Extracted data from " + filename + ":")
        for message in cleaned_messages:
            log_message = (
                f"{LOG_COLORS['WHITE']}Items: {LOG_COLORS['ITEMS_COLOR']}{', '.join(message['items'])}, "
                f"{LOG_COLORS['WHITE']}Price: {LOG_COLORS['PRICE_COLOR']}{message['price']}, "
                f"{LOG_COLORS['WHITE']}Name: {LOG_COLORS['NAME_COLOR']}{message['name']}{LOG_COLORS['WHITE']}"
            )
            logger.info(log_message)
        print("\n")