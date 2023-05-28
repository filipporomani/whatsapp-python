## internal use only

def update_version():
    f = open("./whatsapp/constants.py", "r")
    f = f.read()

    with open("./constants.py", "w+") as f1:
        f1.write(f)