## internal use only

def update_version():
    f = open("./whatsapp/constants.py", "r")
    f = f.read()

    with open("./constants.py", "w+") as f1:
        f1.write(f)
    
    from constants import VERSION
    
    with open("./.version", "w+") as f2:
        f2.write(VERSION)