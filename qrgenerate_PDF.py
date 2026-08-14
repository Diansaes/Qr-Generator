
import pandas as pd
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
from tqdm import tqdm

# Resolution for the conversion (300 pixels per inch)
dpi = 300
cm_to_inches = 1 / 2.54

# Specify the size
width_cm = 2.5  # Width in centimeters
height_cm = 3.2  # Height in centimeters

# Calculate dimensions in pixels
width_px = int(width_cm * dpi * cm_to_inches)
height_px = int(height_cm * dpi * cm_to_inches)

# Font for the text
try:
    font = ImageFont.truetype(
        "AtkinsonHyperlegibleMono-SemiBold.ttf", size=50)
except:
    font = ImageFont.load_default()


# Function to insert hyphens
def insertar_guiones(clave):
    clave = str(clave)
    if len(clave) < 9:
        return "ERROR-FORMAT"
    # Insert hyphens every 3 characters
    return f"{clave[:3]}-{clave[3:6]}-{clave[6:]}"


# Function to generate QR codes
def generar_codigos_qr(csv_file_path):
    # Get the base file name (without extension) to use as the folder name
    output_dir_name = os.path.splitext(os.path.basename(csv_file_path))[0]
    output_dir = os.path.join(output_dir_name)
    os.makedirs(output_dir, exist_ok=True)  # Create the folder if it does not exist

    # Load the CSV file
    data = pd.read_csv(csv_file_path)

    # Read only the "clave" column and convert to strings
    claves = data['clave'].dropna().astype(str)

    # Define the logo to insert into the QR
    logo_path = 'logo.png'

    # Generate a QR code for each key
    for clave in claves:
        try:

            texto_clave = insertar_guiones(clave)

            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=15,
                border=2,
            )
            qr.add_data(clave)
            qr.make(fit=True)

            # Generate the QR code image
            qr_img = qr.make_image(
                fill_color="black", back_color="white").convert('RGB')

            # Open the logo
            logo = Image.open(logo_path)

            # Resize the logo so it fits in the center of the QR
            qr_width, qr_height = qr_img.size
            logo_size = qr_width // 3  # The width size of the QR logo
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

            # Paste the logo in the center of the QR
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

            # Create a final image that includes the text at the bottom
            final_img_height = qr_height + 100  # Add space for the text
            final_img = Image.new(
                'RGB', (qr_width, final_img_height), color="black")
            final_img.paste(qr_img, (0, 0))

            # Draw the text at the bottom
            draw = ImageDraw.Draw(final_img)
            bbox = tuple(map(int, draw.textbbox(
                (0, 0), texto_clave, font=font)))
            text_width = bbox[2] - bbox[0]
            text_position = ((qr_width - text_width) // 2, qr_height + 7)
            draw.text(text_position, texto_clave, fill="white", font=font)

            # Adjust the final size in centimeters
            final_img = final_img.resize((width_px, height_px), Image.LANCZOS)

            # Save the image in PDF format
            output_path_pdf = os.path.join(output_dir, f"{clave}.pdf")
            final_img.save(output_path_pdf, "PDF", resolution=dpi)

        except Exception as e:
            print(f"Error processing key '{clave}': {e}")


# Specify the folder where the CSV files are located
csv_folder = 'folder_1'

# Get the list of CSV files in the folder
csv_files = [os.path.join(csv_folder, file)
             for file in os.listdir(csv_folder) if file.endswith('.csv')]


for csv_file in tqdm(csv_files, desc="Processing CSV files"):
    generar_codigos_qr(csv_file)


print("*** Files Ready  ***")
