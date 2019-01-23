# window.QRLogin.code = 200;
# window.QRLogin.uuid = "wa7irFC_0Q==";


import re


data = 'window.QRLogin.code = 200; window.QRLogin.uuid = "wa7irFC_0Q==";'
ret = re.findall('uuid = "(.*)";',data)

print(ret)