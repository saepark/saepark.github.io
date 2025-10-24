from PIL import Image, ImageDraw, ImageFont
import os

# Create a 256x256 image with transparency (will be scaled down for favicon)
size = 256
img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))  # Transparent background
draw = ImageDraw.Draw(img)

# Rotman pink color
pink = (226, 7, 120, 255)  # RGB + Alpha

# Draw a circle background with pink
circle_margin = 20
draw.ellipse([circle_margin, circle_margin, size-circle_margin, size-circle_margin],
             fill=pink)

# Try to use Garamond font for the initials
try:
    font_size = 120
    fonts_to_try = [
        '/System/Library/Fonts/Supplemental/EB Garamond Bold.ttf',
        '/System/Library/Fonts/Supplemental/Garamond.ttc',
        '/Library/Fonts/Adobe Garamond Pro.otf',
        '/System/Library/Fonts/Supplemental/AppleGaramond.ttf',
        '/Library/Fonts/Garamond.ttf',
    ]

    font = None
    for font_path in fonts_to_try:
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
            break

    if font is None:
        # Fallback to a serif font if Garamond not found
        fallback_fonts = [
            '/System/Library/Fonts/Supplemental/Times New Roman.ttf',
            '/System/Library/Fonts/Supplemental/Georgia.ttf',
        ]
        for font_path in fallback_fonts:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, font_size)
                break

    if font is None:
        font = ImageFont.load_default()
except:
    font = ImageFont.load_default()

# Draw "SP" text in white
text = "SP"
# Get text bounding box to center it properly
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

# Calculate center position accounting for the bbox offset
x = (size - text_width) // 2 - bbox[0]
y = (size - text_height) // 2 - bbox[1]

draw.text((x, y), text, fill='white', font=font)

# Save as PNG (will convert to .ico and smaller sizes)
img.save('favicon-256.png')

# Create standard favicon sizes
for favicon_size in [16, 32, 64]:
    img_resized = img.resize((favicon_size, favicon_size), Image.Resampling.LANCZOS)
    img_resized.save(f'favicon-{favicon_size}.png')

# Save as .ico (contains multiple sizes)
img.save('favicon.ico', sizes=[(16,16), (32,32), (64,64)])

print("Favicons created successfully!")
print("- favicon.ico (multi-size)")
print("- favicon-16.png, favicon-32.png, favicon-64.png, favicon-256.png")
