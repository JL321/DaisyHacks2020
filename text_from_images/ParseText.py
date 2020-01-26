import keywords
import texthelper
#global unit_set
#global unit_promo_price

def offers(ad_str):
    ad_str = ad_str.lower()
    ad_lines = ad_str.split("\n")

    # MAIN vars that will go in the output csv     
    save_per_unit = 0.0
    uom = ""
    discount = 0.0
    least_unit_for_promo = 0
    unit_promo_price = 0.0

    saved = False  #bool to check if the keyword save has been used
    
    for line in ad_lines:
        if not line:
            continue
        if not uom or uom == "":
            uom = texthelper.find_qty_unit(line, keywords.unitset)
            if uom:
                index = line.find(uom.split()[0])
                uom = line[0:index+len(uom.split()[0])+1].strip()
        line = texthelper.replace(line)

        # Off case ########################################################################################
        if "off" in line:

            if "%" in line:
                line = texthelper.strip2num(line)
                num = texthelper.strip2float(line)
                try:
                    discount += float(num)/100 if num else 0.0
                except:
                    pass

            elif "$" in line and not save_per_unit:
                line = texthelper.strip2num(line)
                num = texthelper.strip2float(line) 
                try:
                    save_per_unit = float(num) if num else 0.0
                except:
                    save_per_unit = 0.0

            elif "¢" in line and not save_per_unit:
                line = texthelper.strip2num(line)
                num = texthelper.strip2float(line)
                try:
                    save_per_unit = float(num)/100 if num else 0.0
                except:
                    save_per_unit = 0.0 

        # Save case ##########################################################################################
        elif "save" in line and not saved:
            saved = True
            if "on" in line:
                
                on = ""
                i = line.index("on")

                for k in range(i, len(line)):      #after "on" part
                    if (texthelper.isnumbers(line[k])):
                        on += line[k] 
                if on == "." or on == "":
                    on = ""
                else:
                    try:
                        on = float(texthelper.strip2float(on))
                    except:
                        on = ""
                        print(line)
                
                line = line[0:i+2]
                for k in range(0, i+2):      #before "on" part
                    if (line[k].isalpha()):
                        line = line.replace(line[k]," ")
                line = line.replace(" ", "")   
                    
                if "$" in line: 
                    line = line.replace("$", "")
                    num = texthelper.strip2float(line)
                    try: 
                        amt =  float(num) if num else 0.0
                    except:
                        amt = 0.0
                        print(line)
                elif "¢" in line:
                    line = line.replace("¢", "")
                    num = texthelper.strip2float(line) 
                    try:
                        amt = float(num)/100 if num else 0.0
                    except:
                        amt = 0.0
                        print(line)

                if not on:
                    on = 1.0

                try:
                    amt = amt if amt else 0.0
                except:
                    amt = 0.0
                least_unit_for_promo = on if not(least_unit_for_promo) else 0
                save_per_unit += amt/on if not(save_per_unit) else 0.0
                discount += save_per_unit/unit_promo_price if(unit_promo_price) else 0.0

            elif "/" in line:
                
                on = ""
                i = line.index("/")

                for k in range(i+1, len(line)):      #after "on" part 
                    if (texthelper.isnumbers(line[k])):
                        on += line[k]
                if on == "." or on == "":
                    on = ""
                else:
                    try:
                        on = float(texthelper.strip2float(on))
                    except:
                        on = ""
                        print(line)
                
                line = line[0:i+2]
                for k in range(0, i+2):      #before "on" part
                    if (line[k].isalpha()):
                        line = line.replace(line[k]," ")
                line = line.replace(" ", "")       

                if "$" in line: 
                    line = line.replace("$", "")
                    num = texthelper.strip2float(line)  
                    try: 
                        amt =  float(num) if num else 0.0
                    except:
                        amt = 0.0
                        print(line)
                elif "¢" in line:
                    line = line.replace("¢", "")
                    num = texthelper.strip2float(line)
                    try:
                        amt = float(num)/100 if num else 0.0
                    except:
                        amt = 0.0
                        print(line)
                if not on:
                    on = 1.0
                try:
                    amt = amt if amt else 0.0
                except:
                    amt = 0.0
                least_unit_for_promo = on if not(least_unit_for_promo) else 0
                save_per_unit += amt/on if not(save_per_unit) else 0.0
                discount += save_per_unit/unit_promo_price if (unit_promo_price) else 0.0

            elif "up to" in line:
                on = ""
                i = line.index("up to")

                for k in range(i+5, len(line)):      #after "on" part
                    if (texthelper.isnumbers(line[k])):
                        on += line[k] 
                if on == "." or on == "":
                    on = ""
                else:
                    try:
                        on = float(texthelper.strip2float(on))
                    except:
                        on = ""
                        print(line)

                line = line[0:i+2]
                for k in range(0, i+2):      #before "on" part
                    if (line[k].isalpha()):
                        line = line.replace(line[k]," ")
                line = line.replace(" ", "")   
                    
                if "$" in line: 
                    line = line.replace("$", "")
                    num = texthelper.strip2float(line) 
                    amt = float(num) if num else 0.0
                elif "¢" in line:
                    line = line.replace("¢", "")
                    num = texthelper.strip2float(line) 
                    amt = float(num)/100 if num else 0.0
                if not on:
                    on = 1.0
                try:
                    amt = amt if amt else 0.0
                except:
                    amt = 0.0
                least_unit_for_promo = on if not(least_unit_for_promo) else 0
                save_per_unit += amt/on if not(save_per_unit) else 0.0
                discount += save_per_unit/unit_promo_price if (unit_promo_price) else 0.0

            else:
                on = ""
                for k in range(0, len(line)):
                    if (line[k].isalpha()):
                        line = line.replace(line[k]," ")
                line = line.replace(" ", "")     

                if "$" in line: 
                    line = line.replace("$", "")
                    num = texthelper.strip2float(line)
                    try:  
                        amt =  float(num) if num else 0.0
                    except:
                        amt = 0.0
                        print(line)
                elif "¢" in line:
                    line = line.replace("¢", "")
                    num = texthelper.strip2float(line)
                    try:  
                        amt = float(num)/100 if num else 0.0
                    except:
                        amt = 0.0
                        print(line)
                    
                    
                if not on:
                    on = 1.0
                try:
                    amt = amt if amt else 0.0
                except:
                    amt = 0.0
                least_unit_for_promo = on if not(least_unit_for_promo) else 0
                save_per_unit += amt/on if not(save_per_unit) else 0.0
                discount += save_per_unit/unit_promo_price if (unit_promo_price) else 0.0


        # Buy one get one ########################################################################################
        elif "buy one get one free" in ad_str.replace("\n", " "):
            discount = 0.5
            least_unit_for_promo = 1
            unit_promo_price = 2*save_per_unit if save_per_unit else 0.0



        # Brand Wide Sale case ########################################################################################
        if "brand wide sale" in ad_str.replace("\n", " "):
            least_unit_for_promo = 1
            save_per_unit = 0.0



        # Price Identification ########################################################################################
        else:

            if "¢" in line:
                for k in line:
                    if k.isalpha() or (k == "¢"):
                        line = line.replace(k, " ")
                line = line.replace(" ", "")
                try:
                    num = texthelper.strip2float(line)
                    unit_promo_price = float(num)/100 if num else 0.0
                except:
                    print(line)
            
            elif "$" in line:
                for k in line:
                    if (k.isalpha() or k == "$"):
                        line = line.replace(k, " ")
                line = line.replace(" ", "")
                try:
                    num = texthelper.strip2float(line)
                    unit_promo_price = float(num) if num else 0.0
                except:
                    print(line)


            
        # Half off##################################################################################################
            #included in off
    if not save_per_unit or save_per_unit == 0:
        save_per_unit = ""
    if not uom or uom == "":
        uom = ""
    if not discount or discount == 0.0:
        discount = ""
    if not least_unit_for_promo or least_unit_for_promo == 0:
        least_unit_for_promo = "1"
    if not unit_promo_price or unit_promo_price == 0:
        unit_promo_price = ""

    return (unit_promo_price, save_per_unit, uom, least_unit_for_promo, discount)



if __name__ == "__main__":
    adstring = "SAVE $2.98 on 2 \nBlueberries\nHalf Pint \nA healthy snack-perfect for \nsmoothies, added to yogurt, or \nmake blueberry pancakes! High\nin Vitamin C and antioxidants. \nDiscount Taken at Register2/$6HEALTHY REWARDS \nOFFER WITH CARD"
    print(offers(adstring))

