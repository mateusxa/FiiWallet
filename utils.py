def parse_real(value):

    parsed_value = value

    try:
        parsed_value = float(str(value[3:]).replace(",", '.'))
    except:
        if(value[-3] == " "):
            unit = value[-2:]
            if(unit == 'bi'):
                value = value[:-3]
                parsed_value = float(str(value[3:]).replace(",", '.')) * 10**9
            
            elif(unit == 'mi'):
                value = value[:-3]
                parsed_value = float(str(value[3:]).replace(",", '.')) * 10**6

            else:
                parsed_value = "error" + str(value)

    return parsed_value

def parse_percent(value):
    return float(str(value.strip('%').replace(",", '.')))

