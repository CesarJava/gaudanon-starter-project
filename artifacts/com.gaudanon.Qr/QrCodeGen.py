import qrcode
import json

identity = {
    "role":"Operator",
    "name":"John Doing Doe",
    "acess_level":1    
}

qrCodeImg = qrcode.make(json.dumps(identity));

qrCodeImg.save("Operator1.png")