import qrcode
import json
import uuid

identity = {
    "id": uuid.uuid4().hex,
    "role":"Operator",
    "name":"John Will Doe",
    "acess_level":2    
}

qrCodeImg = qrcode.make(json.dumps(identity));

qrCodeImg.save("Operator1.png")