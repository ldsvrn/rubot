#!/usr/bin/env python

import requests
import bs4 as bs

def get_menu(url):
    soup = bs.BeautifulSoup(requests.get(url).text, "lxml").find_all(class_="menu")

    ret = []

    for jour in soup:
        date = jour.find("time").get_text()
        menu = jour.find(class_="meal_foodies").find_all("li", recursive=False)

        ret.append(
            {
                "date": date,
                "menu": [repas.get_text() for repas in menu[0].find("ul").find_all("li")],
                "grillades": [repas.get_text() for repas in menu[1].find("ul").find_all("li")],
                "pastabox": [repas.get_text() for repas in menu[2].find("ul").find_all("li")],
                "sandwichs": [repas.get_text() for repas in menu[3].find("ul").find_all("li")],
            }
        )
    
    return ret
