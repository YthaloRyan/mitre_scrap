import requests
from bs4 import BeautifulSoup

url = 'https://attack.mitre.org/techniques/T1589/003/'

res = requests.get(url).content

soup = BeautifulSoup(res, 'html.parser')

title1 = soup.find('span', {'id': 'subtechnique-parent-name'}).text
title2 = soup.find('h1').text

title2 = title2[:title2.find('/n')]

print(title2)
# print(' '.join([title1, title2]))




