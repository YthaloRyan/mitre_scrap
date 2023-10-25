import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json
import yaml

class Mitre:
    def __init__(self):
        self.url_base = 'https://attack.mitre.org'
        
    def organizer(self, name, list_names):
        infos = [item.text.strip() for item in list_names]
            
        if name == 'TACTICS':
            return infos
        
        self.infos = sorted(infos)
        return self.infos
    
    def sub_tech_organizer(self, pos):
        sub_tech_list = []
        sub_tech = self.infos[pos]
        for item in self.sub_techniques:
            infos = item('a')[1]
            name = infos.text.strip()
            splited_id = infos['href'].split('/')

            if splited_id[2] == sub_tech:
                id = '.'.join(splited_id[2:4])
                
                result = f'{id} -> {name}'
                sub_tech_list.append(result)
                
        return sub_tech_list
            
    def questioner(self, title, list_names):
        names = list_names
        space = 1
        size = len(names)
        
        if title != 'SUB-TECHNIQUES':
            names = self.organizer(title, list_names)
            space = len(max(names))
        
        print('='*35)
        print(f'{title.center(35)}')
        print('='*35)
        for num, info in enumerate(names):
            question = f'[{str(num).rjust(2)}]' + f'{"":.<4}' + f'{info:.>{space}}'
            if title == 'SUB-TECHNIQUES':
                print(question)
            else:
                print(f'{question.center(35)}')
        print('='*35)

        choice = input(f'Choose a {title.lower()[:-1]}[0-{size-1}]: ')
        while choice not in [str(i) for i in range(size)]:
            choice = input(f'Invalid, try again [0-{size-1}]: ')
            
        return int(choice)
    
    def get_tactics(self):
        res = requests.get(self.url_base).content
        soup = BeautifulSoup(res, 'html.parser')

        tactics = soup.find('table', class_='matrix side').find_all(class_='tactic name')
        
        return tactics
    
    def get_techniques(self, url):
        res = requests.get(f'{self.url_base}{url}').content
        
        soup = BeautifulSoup(res, 'html.parser')
        all_techniques = soup.find('tbody')

        techniques = all_techniques.find_all('td', {"colspan": "2"})
        self.sub_techniques = all_techniques.find_all('tr')
        
        return techniques
    
    def get_sub_infos_url(self, sub):
        sub_url = sub.split(' ')[0].replace('.', '/')
        url  = f'{self.url_base}/techniques/{sub_url}'
        
        return url
    
    def start(self):
        tactics = self.get_tactics()
        tactics_choice = self.questioner('TACTICS', tactics)
        tactic_url = tactics[int(tactics_choice)].find('a')['href']
        
        techniques = self.get_techniques(tactic_url)
        techniques_choice = self.questioner('TECHNIQUES', techniques)
        
        sub_techniques = self.sub_tech_organizer(techniques_choice)
        sub_tec_choice = self.questioner('SUB-TECHNIQUES', sub_techniques)
        
        infos_url = self.get_sub_infos_url(sub_techniques[sub_tec_choice])
        
        sub_technique_content = getMitreInfos().start(infos_url)
        
        return sub_technique_content
        
class getMitreInfos:
    def get_url_content(self, url):
        res = requests.get(url).content
        soup = BeautifulSoup(res, 'html.parser')
        
        return soup
    
    def get_tables_infos(self):
        tables = self.soup.find_all('table', class_='table table-bordered table-alternate mt-2')
        
        for table in tables:
            if 'Mitigation' in table.text:
                return table

        return None
    
    def get_mitigations(self):
        tables = self.get_tables_infos().find('tbody').find_all('tr')
        result = []
        
        for table in tables:
            dict_infos = {}
            table = table.find_all('td')
                
            dict_infos['id'] = table[0].text.strip()
            dict_infos['name'] = table[1].text.strip()
            dict_infos['infos'] = table[2].text.strip()
            
            result.append(dict_infos)
                
        return result
    
    def get_infos(self):
        soup = self.soup.find('div', class_='col-md-4').find('div', class_='card-body').find_all('div', class_='col-md-11 pl-0')
        result = {}
        infos_list = []
        for t in soup:
            infos = t.get_text(strip=True).split(':')
            infos_list.append(infos)  
        
        for name in infos_list:
            result[name[0]] = name[1]
            
        return result
    
    def start(self, url):
        self.soup = self.get_url_content(url)
        infos = {}
        
        infos['name'] = self.soup.find('title').text.split(',')[0]
        infos['content'] = self.soup.find('div', class_='description-body').get_text(strip=True)
        infos['mitigations'] = self.get_mitigations()
        infos['infos'] = self.get_infos()
        
        return infos
        

namesa = Mitre().start()

with open('teste.yaml', 'w') as f:
    yaml.dump(namesa, f , default_flow_style=False)
# if __name__ == '__main__':
#     Mitre().start()
    