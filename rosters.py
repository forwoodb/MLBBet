import time

from uritemplate import expand
startTime = time.time()

########## Import data ##########

import requests 
from bs4 import BeautifulSoup
import unicodedata
from pprint import pprint


teams = ['angels', 'astros', 'athletics', 'bluejays', 'braves',
         'brewers', 'cardinals', 'cubs', 'dbacks', 'dodgers',
         'giants', 'guardians', 'marlins', 'mets', 'nationals',
         'orioles', 'mariners', 'padres', 'phillies', 'pirates',
         'rangers', 'rays', 'reds', 'redsox', 'rockies',
         'royals', 'tigers', 'twins', 'whitesox','yankees']
# url = "https://www.espn.com/mlb/team/roster/_/name/det/detroit-tigers"
# # url = "https://www.espn.com/mlb/team/roster/_/name/min/minnesota-twins"

# # Remove accents - example from https://www.codegrepper.com/code-examples/python/python+remove+accents+from+characters
# def simplify(text):
# 	import unicodedata
# 	try:
# 		text = unicode(text, 'utf-8')
# 	except NameError:
# 		pass
# 	text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
# 	return str(text)

def remove_accents(text):
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    return text.decode('utf-8')

players = []
handed = []

for team in teams:
    players.append([team.upper()])
    handed.append([team.upper()])
    print(team.upper())
    url = "https://www.mlb.com/" + team + "/roster"
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
# }

    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')

    for table in tables:
        rows = table.find_all('tr')

        for row in rows:
            names = row.find_all('a', text=True)
            bt = row.find_all('td', class_='bat-throw')
            name_list = [name.text for name in names]
            bt_list = [i.text for i in bt]
            
            # MLB.com 
            for name in names:
                players.append([remove_accents(name.text)])
                # print(remove_accents(name.text))

            for h in bt:
                if h.text != 'B/T':
                    handed.append([h.text])
                    # print(h.text)

            # ESPN 
            # for i in cells:
            #     data = i.find('div')
            #     if data.find('a'):
            #         print(i.a.text)
            #     # print(data.text)


print(players)

########## Write to CSV ##########
import pandas as pd

# rosters = list(zip(players, handed))

df_rosters = pd.DataFrame()

# Need double square brackets because of the square brackets in the append statement
    # Square brackets needed in append statement in order to export to Google Sheets
df_rosters[['Name']] = players
df_rosters[['B/T']] = handed
df_rosters[['B','T']] = df_rosters['B/T'].str.split('/', expand=True)
# df_rosters = pd.DataFrame(rosters, columns=['Player', 'B/T'])
# df_rosters.columns = ['Player', 'B/T']
# df_rosters = df_rosters[['Player', 'B/T']]
# df_rosters = df_players.append(rosters)

# df_rosters.to_csv(
#     # '/Applications/MAMP/htdocs/Python/Django/DataApps/MLBWeb/csv_data/06-18-22/rosters.csv'
#     '/Applications/MAMP/htdocs/Python/WebScraping/MLB/csv_data/04-26-23/rosters.csv'
#     )

print(df_rosters)

# ########## Write to sheet ##########

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
# client = gspread.authorize(creds)
# book = 'DKMLB2'
# sheet = "Rosters"
# spreadsheet = client.open(book).worksheet(sheet)

# spreadsheet.update('A2:A820', players)
# spreadsheet.update('B2:B820', handed)
# # print(players)


