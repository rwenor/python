from bs4 import BeautifulSoup
from urllib import urlopen
 
url = urlopen('http://bors.e24.no/e24/portal/e24no/list/norway')
soup = BeautifulSoup(url)
tag = soup.find_all('tr', {'class': 'r6'})
aker_value = tag[0].find('td', {'class': 'c2 n'})
print( aker_value.text ) #188,50