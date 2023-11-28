import random

base93charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,0123456789!@#$%^&*()-_=+[]{};\'\"<>/?\\|`~'
base90charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,0123456789!@#$%^&*()-_=+[]{};:\'\"/?~ '

def convertFromBase10(x, base):
    if base == 93:
        charset = base93charset
    elif base == 90:
        charset = base90charset

    if x < 0:
        sign = -1
    elif x == 0:
        return charset[0]
    else:
        sign = 1

    x *= sign
    chars = []
    while x:
        chars.append(charset[x % base])
        x //= base
    if sign < 0:
        chars.append('-')
    chars.reverse()
    return ''.join(chars)

def convertToBase10(x): # Converts base 93 hex address to base 10 number.
    base10_result = 0
    power = 0

    for char in reversed(x):
        if char in base93charset:
            char_value = base93charset.index(char)
            base10_result += char_value * (93 ** power)
            power += 1

    return base10_result

def searchByText(text, library_coordinate):
    if len(text) < 3200:
        text = text.ljust(3200) # Pads text if it has less than 3200 characters.

    sum_value = 0
    for i, v in enumerate(text[::-1]):
        char_value = base90charset.index(v)
        sum_value += char_value * (len(base90charset) ** i) # Converts base 90 text input to base 10 number.

    seed = library_coordinate * (len(base90charset)**3200) + sum_value
    result = convertFromBase10(seed, 93) # Converts base 10 number to base 93 hex address.
    return result

def searchByAddress(address):
    hexagon_address, wall, shelf, volume, page = address.split(':')
    volume = volume.zfill(2)
    page = page.zfill(3)
    library_coordinate = int(page + volume + shelf + wall)

    seed = convertToBase10(hexagon_address) - library_coordinate * (len(base90charset)**3200) # Converts base 93 hex address to base 10 number.
    result = convertFromBase10(seed, 90) # Converts base 10 number to base 90 text.
    return result

x = input("Type 1 to search for address given text. Type 2 to search for text given an address. \n")
if int(x) == 1:
    text = input("Enter your text: ")

    wall = str(random.randint(1, 4))
    shelf = str(random.randint(1, 5))
    volume = str(random.randint(1, 32)).zfill(2) # Pads the volume number if necessary.
    page = str(random.randint(1, 410)).zfill(3) # Pads the page number if necessary.
    library_coordinate = int(page + volume + shelf + wall) # Randomizes the library coordinate.

    hexagon_address = searchByText(text, library_coordinate)
    total_address = hexagon_address + ':' + wall + ':' + shelf + ':' + volume + ':' + page
    print("Hexagon address:\n" + total_address)
elif int(x) == 2:
    hexagon_address = input("Enter your total hex address: ")
    contentByAddress = searchByAddress(hexagon_address)
    print("Page content: " + contentByAddress)
