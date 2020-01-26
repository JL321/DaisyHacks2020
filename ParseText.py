
#global unit_set
#global unit_promo_price

def offers(ad_str, unit_set):
    ad_str = ad_str.lower()
    ad_lines = ad_str.split("\n")

    offer_unit = ""
    offer_val = 0

    # MAIN vars that will go in the output csv     
    save_per_unit = float()
    uom = str()
    discount = float()
    least_unit_for_promo = float()
    unit_promo_price = float()

    
    for line in ad_lines:

        line_qty_unit = line_units(line, unit_set)
        if(line_qty_unit):
            h = line.index(line_qty_unit)
            uom = line[0,h+len(line_qty_unit)]


        if "per" in line:
            line = line.replace("per", "/")
        if "half" in line:
            line = line.replace("half", "50%")


        # Off case ########################################################################################
        if "off" in line:
            offer_unit = "%"

            if "%" in line:
                for letter in line:                     #just keep numbers and special chars (becz of . in 1.5)
                    if (letter.isalpha()):
                        line = line.replace(letter, "")
                line = line.replace("%", "")
                discount += float(line)/100


            elif "$" in line:
                for letter in line:                     #just keep numbers and special chars (becz of . in 1.5)
                    if (letter.isalpha()):
                        line = line.replace(letter, "")
                line = line.replace("%", "")
                save_per_unit = float(line)
                break



            elif "¢" in line:
                for letter in line:                     #just keep numbers and special chars (becz of . in 1.5)
                    if (letter.isalpha()):
                        line = line.replace(letter, "")
                line = line.replace("%", "")
                save_per_unit = float(line)/100
                break                
        
                    

            
                   


        # Save case ##########################################################################################
        elif "save" in line:
            
            if "on" in line:
                on = "1"
                i = line.index("on")
                
                uom = line[(i+2):len(line)]

                for k in range(i, len(line)):      #after "on" part
                    if (line[k].isnumeric()):
                        on += line[k] 
                on = float(on)

                for k in range(0, i+2):      #before "on" part
                    
                    if (line[k].isalpha()):
                        line = line.replace(line[k],"")
                    
                if "$" in line: 
                    line = line.replace("$", "")    
                    amt =  float(line)
                elif "¢" in line:
                    line = line.replace("¢", "")
                    amt = float(line)/100

                
                least_unit_for_promo = on if not(least_unit_for_promo) else float()
                save_per_unit += amt/on if not(save_per_unit) else float()
                discount = save_per_unit/unit_promo_price if(unit_promo_price) else float()

                break




            elif "/" in line:
                on = "1"
                i = line.index("/")

                uom = line[(i+1):len(line)]


                for k in range(i+1, len(line)):      #after "on" part 
                    if (line[k].isnumeric()):      # isnumeric becuase no. of units always integer
                        on += line[k] 
                on = float(on)


                for k in range(0, i+1):      #before "on" part     
                    if (line[k].isalpha()):
                        line = line.replace(line[k],"")        

                if "$" in line: 
                    line = line.replace("$", "")    
                    amt =  float(line)
                elif "¢" in line:
                    line = line.replace("¢", "")
                    amt = float(line)/100

                least_unit_for_promo = on if not(least_unit_for_promo) else float()
                save_per_unit += amt/on if not(save_per_unit) else float()
                discount = save_per_unit/unit_promo_price if (unit_promo_price) else float()
        
                
                break



            elif "up to" in line:
                on = "1"
                i = line.index("up to")
                
                uom = line[(i+5):len(line)]

                for k in range(i+5, len(line)):      #after "on" part
                    if (line[k].isnumeric()):
                        on += line[k] 
                on = float(on)

                for k in range(0, i+5):      #before "on" part
                    
                    if (line[k].isalpha()):
                        line = line.replace(line[k],"")
                    
                if "$" in line: 
                    line = line.replace("$", "")    
                    amt = float(line)
                elif "¢" in line:
                    line = line.replace("¢", "")
                    amt = float(line)/100
                
                least_unit_for_promo = on if not(least_unit_for_promo) else float()
                save_per_unit += amt/on (save_per_unit > 0) if not(save_per_unit) else float()
                discount = save_per_unit/unit_promo_price if (unit_promo_price) else float()               

                break


            else:

                for k in range(0, len(line)):      #before "on" part     
                    if (line[k].isalpha()):             
                        line = line.replace(line[k],"")        

                if "$" in line: 
                    line = line.replace("$", "")    
                    amt =  float(line)
                elif "¢" in line:
                    line = line.replace("¢", "")
                    amt = float(line)/100

                least_unit_for_promo = on if not(least_unit_for_promo) else float()
                save_per_unit = amt/on if not(save_per_unit) else float()
                discount = save_per_unit/unit_promo_price if (unit_promo_price) else float()

                
                




        # Buy one get one ########################################################################################
        elif "buy one get one free" in ad_str.replace("\n", " "):
            discount = 0.5
            least_unit_for_promo = 1
            unit_promo_price = 2*save_per_unit
            





        # Brand Wide Sale case ########################################################################################
        if "brand wide sale" in ad_str.replace("\n", " "):
            least_unit_for_promo = 1
            save_per_unit = float()
            uom = str()
            discount = float()
            unit_promo_price = float()  

            break  



        # Price Identification ########################################################################################
        else:

            if "¢" in line:
                for k in line:
                    if k.isalpha() or (k == "¢"):
                        line = line.replace(k, "")
                unit_promo_price = float(line)
            
            elif "$" in line:
                for k in line:
                    if (k.isalpha() or k == "$"):
                        line = line.replace(k, "")
                unit_promo_price = float(line)


            
        # Half off##################################################################################################
            #included in off


    return(unit_promo_price, save_per_unit, uom, discount, least_unit_for_promo)

def line_units(ad_line, unit_set):
    for i in ad_line.split():
        if i in unit_set:
            return i



