# importation des modules
import pandas as pd
from bs4 import BeautifulSoup
import requests
#Declaration et initialisation des variables
article = []
titre = []
paragraphe = ''
# Collecte des urls des differentes rubriques hormis 'A la minute' et 'Ticket'
soup = BeautifulSoup(requests.get('https://lenouvelliste.com/').text, 'html.parser')
page = soup.find('ul' , class_='nav navbar-nav')
rubrique = page.find_all('a')
rubrique.pop(len(rubrique)-1)
rubrique.pop(0)

# Exploration des rubriques et collectes des urls des articles
for l in rubrique:
    print(l['href'])
    soup = BeautifulSoup(requests.get(l['href']).text, 'html.parser')
    b = soup.find_all('div', class_="content_widget")
    # Collecte des urls des articles dont le titre contient covid ou coronavirus
    for li in b:
        a = li.find('a', href=True) 
        sub_soup = BeautifulSoup(requests.get(a['href']).text, 'html.parser')
        #------------------------------------
        titre.append(sub_soup.find('h2').string)
        p = sub_soup.find('article')
        pa = p.find_all('p')
        for l in pa:
            try:
                paragraphe += l.string
            except TypeError:
                pass
        article.append(paragraphe)
        paragraphe =''
        
data = pd.DataFrame(list(zip(titre, article)), columns =['Titre', 'Article']) 
