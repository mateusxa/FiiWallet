import requests
from bs4 import BeautifulSoup


def get_fii_data(fii):
    raw_data = requests.get("https://www.fundsexplorer.com.br/funds/" + fii).content

    soup = BeautifulSoup(raw_data, 'html.parser')
    
    data = []

    #stock price 
    stock_price = parse_list(list(soup.find("div", {"id": "stock-price"}).children)[1].text)
    data.append(['Stock Price', stock_price[0]])

    # main-indicators-carousel -> div cl flickity-viewport -> div cl flickity-slider -> div cl carousel-cell [n]
    carousel = list(soup.find("div", {"id": "main-indicators-carousel"}).children)

    for carousel_item in carousel:
        if len(carousel_item.text) > 2:
            data.append(parse_list(carousel_item.text))

    return serialize_data(data)


def serialize_data(fii_data):
    stock_price = parse_real(fii_data[0][1])
    daily_liquidity = float(fii_data[1][1])
    last_yield = parse_real(fii_data[2][1])
    dividend_yield = parse_percent(fii_data[3][1])
    liquid_assets = parse_real(fii_data[4][1])
    patrimonial_value = parse_real(fii_data[5][1])
    month_prof = parse_percent(fii_data[6][1])
    p_vp = float(str(fii_data[7][1])
                .replace(",", '.'))

    return(
        stock_price, daily_liquidity, last_yield, dividend_yield, liquid_assets, 
        patrimonial_value, month_prof, p_vp
    )


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

def parse_list(parse_item):
    return parse_item.replace("\n", "").strip() \
        .replace("                ", "|") \
        .replace("              ", "|") \
        .split("|")