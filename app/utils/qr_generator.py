import qrcode
import os
from flask import current_app

def generate_qr_code(violation_id):
    """
    Generates a QR code for a given violation ID.
    The QR code points to the public status page for that violation.
    Returns the relative path to the generated QR code image.
    """
    domain = os.environ.get('DOMAIN', 'http://127.0.0.1:5000')
    data = f"{domain}/violation/{violation_id}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    filename = f"violation_{violation_id}.png"
    filepath = os.path.join(current_app.config['QR_CODE_DIR'], filename)
    
    img.save(filepath)
    
    return f"qrcodes/{filename}"
