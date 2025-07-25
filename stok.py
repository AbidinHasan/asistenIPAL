#gnti /storage/emulated/0/serverbot/stokbahan/nutrisi.txt sesuai lokasi pathmu

#nutrisi
def read_nutrisi(user_id):
    try:
        with open("/storage/emulated/0/serverbot/stokbahan/nutrisi.txt", 'r') as f:
            return int(f.read())
    except:
        return 0

def write_nutrisi(user_id, value):
    with open("/storage/emulated/0/serverbot/stokbahan/nutrisi.txt", 'w') as f:
        f.write(str(value))

#pac
def read_pac(user_id):
    try:
        with open("/storage/emulated/0/serverbot/stokbahan/pac.txt", 'r') as f:
            return int(f.read())
    except:
        return 0

def write_pac(user_id, value):
    with open("/storage/emulated/0/serverbot/stokbahan/pac.txt", 'w') as f:
        f.write(str(value))

#polimer anion
def read_polimerani(user_id):
    try:
        with open("/storage/emulated/0/serverbot/stokbahan/polimerani.txt", 'r') as f:
            return int(f.read())
    except:
        return 0

def write_polimerani(user_id, value):
    with open("/storage/emulated/0/serverbot/stokbahan/polimerani.txt", 'w') as f:
        f.write(str(value))

#polimer cation
def read_polimerCAT(user_id):
    try:
        with open("/storage/emulated/0/serverbot/stokbahan/polimerCAT.txt", 'r') as f:
            return int(f.read())
    except:
        return 0

def write_polimerCAT(user_id, value):
    with open("/storage/emulated/0/serverbot/stokbahan/polimerCAT.txt", 'w') as f:
        f.write(str(value))

#chlorine
def read_chlorine(user_id):
    try:
        with open("/storage/emulated/0/serverbot/stokbahan/chlorine.txt", 'r') as f:
            return int(f.read())
    except:
        return 0

def write_chlorine(user_id, value):
    with open("/storage/emulated/0/serverbot/stokbahan/chlorine.txt", 'w') as f:
        f.write(str(value))

#naoh soda caustic
def read_naoh(user_id):
    try:
        with open("/storage/emulated/0/serverbot/stokbahan/naoh.txt", 'r') as f:
            return int(f.read())
    except:
        return 0

def write_naoh(user_id, value):
    with open("/storage/emulated/0/serverbot/stokbahan/naoh.txt", 'w') as f:
        f.write(str(value))

#reagen cod LR
def read_codLR(user_id):
    try:
        with open("/storage/emulated/0/serverbot/stokbahan/codLR.txt", 'r') as f:
            return int(f.read())
    except:
        return 0

def write_codLR(user_id, value):
    with open("/storage/emulated/0/serverbot/stokbahan/codLR.txt", 'w') as f:
        f.write(str(value))

#reagen cod HR
def read_codHR(user_id):
    try:
        with open("/storage/emulated/0/serverbot/stokbahan/codHR.txt", 'r') as f:
            return int(f.read())
    except:
        return 0

def write_codHR(user_id, value):
    with open("/storage/emulated/0/serverbot/stokbahan/codHR.txt", 'w') as f:
        f.write(str(value))

#bakteri starter
def read_bakteri(user_id):
    try:
        with open("/storage/emulated/0/serverbot/stokbahan/bakteri.txt", 'r') as f:
            return float(f.read())
    except:
        return 0.0

def write_bakteri(user_id, value):
    with open("/storage/emulated/0/serverbot/stokbahan/bakteri.txt", 'w') as f:
       f.write(str(value))

#karung sak
def read_karung(user_id):
    try:
        with open("/storage/emulated/0/serverbot/stokbahan/karung.txt", 'r') as f:
            return int(f.read())
    except:
        return 0

def write_karung(user_id, value):
    with open("/storage/emulated/0/serverbot/stokbahan/karung.txt", 'w') as f:
        f.write(str(value))