from bs4 import BeautifulSoup

team1 = 'tigers'
team2 = 'orioles'

year = '2021'
month = '08'
day = '12'

# Box score URLs
baseball_monster = 'https://baseballmonster.com/boxscores.aspx'
mlb = 'https://www.mlb.com/gameday/tigers-vs-orioles/2021/08/12/632938#game_state=final,lock_state=final,game_tab=box,game=632938'
# mlb = f'https://www.mlb.com/gameday/{team1}-vs-{team2}/{year}/{month}/{day}/632938#game_state=final,lock_state=final,game_tab=box,game=632938'

url = baseball_monster

# import requests


# # # HTML parser with Requests
# response = requests.get(url)
# soup = BeautifulSoup(response.text, "html.parser")



# from urllib.request import urlopen as uReq
from urllib.request import Request, urlopen

# opening up connection, grabbing the page
# client = uReq(url)

# req = Request(url)
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
content = urlopen(req).read()

soup = BeautifulSoup(content, 'html.parser')

# print(soup.find_all('section'))
# print(soup.find('section', class_="box away secondary-content t116"))
# print(soup.find('section', {"class": "box away secondary-content t116"}))
# print(content)

boxscores = soup.find('tbody')

print(boxscores)