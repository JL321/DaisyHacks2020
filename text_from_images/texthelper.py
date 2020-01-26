import keywords
def find_qty_unit(line, unit_set):
    uom = None
    line_qty_unit = line_units(line, unit_set)
    uom = line_qty_unit
    return uom

def replace(line):
    if "per" in line:
        line = line.replace("per", "/")
    if "half" in line:
        line = line.replace("half", "50%")
    return line

def strip2num(line):
    for letter in line:
        if (letter.isalpha()):
            line = line.replace(letter, " ")
    line = line.replace(" ", "")
    for spechar in keywords.special_chars:
        line = line.replace(spechar, "")
    return line

def line_units(ad_line, unit_set):
    output = ""
    for i in ad_line.split():
        if i in unit_set:
            output += i
    return output

def isnumbers(string):
    for char in string:
        if char in keywords.nums:
            pass
        else:
            return False
    return True

def strip2float(line):
    for letter in line:
        if letter not in keywords.nums:
            line = line.replace(letter, " ")
    line = line.replace(" ", "")
    line = line.replace("..", ".")
    if line == ".":
        line = ""
    return line.strip(".")