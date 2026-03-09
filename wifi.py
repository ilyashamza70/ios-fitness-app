import qrcode

# Dettagli della rete WiFi
ssid = "WINDTRE-MHMF"
password = "IldadononstatrattO1973!"
auth_type = "WPA"  # Può essere "WPA", "WEP", o lasciare vuoto per nessuna crittografia

# Formatta la stringa per il QR code
wifi_string = f"WIFI:T:{auth_type};S:{ssid};P:{password};;"

# Genera il QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(wifi_string)
qr.make(fit=True)

# Crea un'immagine del QR code
img = qr.make_image(fill="black", back_color="white")

# Salva l'immagine
img.save("wifi_qr.png")

print("QR code generato e salvato come wifi_qr.png")
