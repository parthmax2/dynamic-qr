import qrcode

url = "https://parthmax.hf.space/qr"
img = qrcode.make(url)
img.save("static/qr.png")
