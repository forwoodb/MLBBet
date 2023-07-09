from datetime import datetime
time_now = datetime.now().strftime("%H:%M")
print(time_now)

from uritemplate import expand
########## Import data ##########

import requests 
from bs4 import BeautifulSoup
import unicodedata
from pprint import pprint

########## Write to sheet ##########

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)
# book = 'MLBBet2022'
book = 'FGTest'


########## Get data ##########
month_day = 'Jul 4'
year = '2023'

teams = ['angels', 'astros', 'athletics', 'bluejays', 'braves',
         'brewers', 'cardinals', 'cubs', 'diamondbacks', 'dodgers',
         'giants', 'guardians', 'mariners', 'marlins', 'mets',
          'nationals','orioles', 'padres', 'phillies', 'pirates',
         'rangers', 'rays', 'reds', 'redsox', 'rockies',
         'royals', 'tigers', 'twins', 'whitesox','yankees']

# different arrays due to Google Sheets write limits
    # for backtesting
# teams = ['angels', 'astros', 'athletics', 'bluejays', 'braves',
#          'brewers', 'cardinals', 'cubs', 'diamondbacks', 'dodgers']

# teams = [ 'giants', 'guardians', 'marlins', 'mets', 'nationals',
#          'orioles', 'mariners', 'padres', 'phillies', 'pirates']

# teams = ['rangers', 'rays', 'reds', 'redsox', 'rockies', 
#          'royals', 'tigers', 'twins', 'whitesox','yankees']

# teams = ['tigers']

dates = []
home_team = []
locations = []
opponents = []
win_probs = []
runs_scored = []
runs_allowed = []
time_run = []

outcomes = []
print("Games")
for team in teams:
    print(team.upper())

    url = "https://www.fangraphs.com/teams/" + team + "/schedule?season=" + year

    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', class_='team-schedule-table')
    table = div.find('table')

    rows = table.find_all('tr')

    for row in rows:
        cells = row.find_all('td')

        if len(cells) >= 9:
            date = cells[0]
            clean_date = date.text.split(',').pop(0)
            location = cells[1]

            # Game Day
            if clean_date == month_day and location.text == "vs":
                opponent = cells[2]
                win_prob = cells[3]
                scored = cells[5]
                allowed = cells[6]

                dates.append([clean_date])
                home_team.append([team])
                locations.append([location.text])
                opponents.append([opponent.text])
                win_probs.append([win_prob.text])
                if scored.text != '':
                    runs_scored.append([int(scored.text)])
                # runs_scored.append([scored.text])
                if allowed.text != '':
                    runs_allowed.append([int(allowed.text)])
                # runs_allowed.append([allowed.text])
                time_run.append([time_now])
    
print(year)

########## Write to sheet ##########
sheet = "Games"
print(sheet)

spreadsheet = client.open(book).worksheet(sheet)

spreadsheet.update('A5:A5000', dates)
spreadsheet.update('B5:B5000', home_team)
spreadsheet.update('C5:C5000', locations)
spreadsheet.update('D5:D5000', opponents)
spreadsheet.update('F5:F5000', runs_scored)
spreadsheet.update('G5:G5000', runs_allowed)

# Games
spreadsheet.update('E5:E5000', win_probs)
spreadsheet.update('I5:I5000', time_run)

# dates = []
# home_team = []
# locations = []
# opponents = []
# win_probs = []
# runs_scored = []
# runs_allowed = []
# time_run = []

# print(dates)



########## Write to CSV with pandas dataframe ##########

# import pandas as pd

# df_scores = pd.DataFrame()

# # Need double square brackets because of the square brackets in the append statement
#     # Square brackets needed in append statement in order to export to Google Sheets
# df_scores[['Date']] = dates  
# amended_date = df_scores['Date'].str.split(',', expand=True)
# df_scores['Date'] = amended_date[0]
# df_scores[['RS']] = runs_scored
# df_scores[['RA']] = runs_allowed

# print(df_scores)

# # # df_scores.to_csv(
# # #     # '/Applications/MAMP/htdocs/Python/Django/DataApps/MLBWeb/csv_data/06-18-22/rosters.csv'
# # #     '/Applications/MAMP/htdocs/Python/WebScraping/MLB/csv_data/04-26-23/scores.csv'
# # #     )

# # # pd.set_option('display.max_rows', None)
# # # print(df_scores)







