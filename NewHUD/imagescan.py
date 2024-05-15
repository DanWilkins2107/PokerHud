import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Open the image
img = Image.open('pokerimage.jpg')

width, height = img.size
dpi = img.info.get('dpi', (72, 72))  # Default DPI is 72

new_width = 1024
new_height = 768
img = img.resize((new_width, new_height))

img = img.convert('L')

# Crop the image
img = img.crop((50, 200, 180, 220))
# img = img.crop((400, 120, 600, 142))

# Save the cropped image
img.save('cropped.png')

# Perform OCR
text = pytesseract.image_to_string(img)

print(f'Image Resolution: {width}x{height} pixels')
print(f'Image DPI: {dpi[0]}x{dpi[1]}')

print(text)  # Print the recognized text