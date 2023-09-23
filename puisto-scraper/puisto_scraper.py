from bs4 import BeautifulSoup
import requests
import datetime

# Constants
URL = "https://www.ravintolasulo.fi/lounas-puisto/"


def get_current_weekday():
    weekdays = ["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai", "Lauantai", "Sunnuntai"]
    weekday_int = datetime.datetime.now().weekday()
    return weekdays[weekday_int]

def fetch_page():
    response = requests.get(URL)
    if response.status_code != 200:
        return None
    return BeautifulSoup(response.text, "html.parser")

def find_food_elements(soup, weekday):
    # Find the div with the current weekday
    weekday_div = soup.find('div', string=weekday.upper(), class_='elementor-tab-title elementor-tab-mobile-title')
    if weekday_div:
        # We connect the right weekday to the food list with data tab attribute
        data_tab_value = weekday_div['data-tab']
        return soup.find("div", {"data-tab": data_tab_value, 'class': 'elementor-tab-content elementor-clearfix'})
    return None


def main():
    current_weekday = get_current_weekday()
    print("Tänään on " + current_weekday)
    print("Sulo Puistossa tänään tarjolla: ")
    
    soup = fetch_page()
    if soup is None:
        print("Virhe: Sulo Puisto sivun hakeminen ei onnistunut...")
        return

    content_div = find_food_elements(soup, current_weekday)
    if content_div:
        p_elements = content_div.find_all('p')
        for p in p_elements:
            print(p.text)
    else:
        print(f"Ruokatietoja ei löytynyt päivälle {current_weekday}")

if __name__ == "__main__":
    main()