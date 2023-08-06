import binascii
import pypastebin.settings as settings

def add_paste(r):
    if "paste" in r.POST:
        paste = r.POST['paste']
    else:
        paste = r.post_data
    id = gen_id(paste)
    r.database.add(id, paste)
    if "web" in r.POST:
        return """<meta http-equiv="Refresh" content="0; url='/{}'" />""".format(id)
    else:
        return settings.server+"/"+id+"\n"

def gen_id(data):
    return str(hex(binascii.crc32(data.encode('utf-8', errors='ignore'))))[2:]
