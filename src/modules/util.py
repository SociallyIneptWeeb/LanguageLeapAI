
def castInt(val):
    try:
        number = int(val)
        return number
    except ValueError:
        return False

def castFloat(val):
    try:
        number = float(val)
        return number
    except ValueError:
        return False