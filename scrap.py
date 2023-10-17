import requests
from bs4 import BeautifulSoup

url_base = 'https://attack.mitre.org'

res = requests.get(url_base).content

soup = BeautifulSoup(res, 'html.parser')

tactics = soup.find('table', class_='matrix side').find_all(class_='tactic name')


# print('='*35)
# print(f'{"TACTICS".center(35)}')
# print('='*35)
# for num, tactic in enumerate(tactics):
#     num = f'[{num}]'
#     print(f'{num:.<4}', end='')
#     print(f'{tactic.text:.>30}')
# print('='*35)

# choice = input('Choose a tactic[0-13]: ')
# while choice not in [str(i) for i in range(14)]:
#     choice = input('Invalid, try again [0-13]: ')


#tmp
choice = 0

tactic_url = tactics[int(choice)].find('a')['href']

#coletar tecnica
res = requests.get(f'{url_base}{tactic_url}').content

soup = BeautifulSoup(res, 'html.parser')

techniques = soup.find('tbody').find_all('td', {"colspan": "2"})

# for num, tecnic in enumerate(techniques):
#     print(num,tecnic.text.strip())
#     print('='*20)
 
choice = 0

techniques_choice = techniques[choice].text.strip()


sub_techniques = soup.find_all('tr', class_='sub technique')

subs = {}
for sub in sub_techniques:
    sub_technique_infos = sub.find_all('a')[1]
    sub_technique_url = sub_technique_infos['href']
    sub_technique_name = sub_technique_infos.text
    
    print(sub_technique_name)
    if techniques_choice == sub_technique_url.split('/')[2].strip():
        subs[sub_technique_name] = sub_technique_url
        
print(subs)
    