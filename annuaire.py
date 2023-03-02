#!/usr/bin/env python3

import requests
from lxml import html

def annuaire(url, search):
    payload = {'search': search, 'action': 'Chercher'}
    response = requests.post(url, data=payload)
    tree = html.fromstring(response.content)

    surnames = tree.xpath("/html/body/section[2]/div/div/div[1]/p/span[1]/text()")
    names = tree.xpath("/html/body/section[2]/div/div/div[1]/p/span[1]/span/text()")
    emails = tree.xpath("/html/body/section[2]/div/div/div[2]/p/a/text()")
    # tels = tree.xpath("/html/body/section[2]/div/div[1]/div[2]/p/span/a/text()")

    surnames = [str(i).strip() for i in surnames]
    names = [str(i).strip() for i in names]
    emails = [str(i).strip() for i in emails]

    results = []
    if len(emails) == len(names) == len(surnames):
        for i in range(len(emails)):
            results.append({
                'surname': surnames[i],
                'name': names[i],
                'email': emails[i]
            })

    return results
