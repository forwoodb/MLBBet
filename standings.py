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


# ########## Get data ##########
# month_day = 'May 13'
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

def remove_accents(text):
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    return text.decode('utf-8')

dates = []
home_team = []
locations = []
opponents = []
outcomes = []
runs_scored = []
runs_allowed = []
opp_pitchers = []

# win_probs = []


print("Standings")

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

            # Standings
            opponent = cells[2]

            # win_prob = cells[3]
            outcome = cells[4]

            scored = cells[5]
            allowed = cells[6]
            pitcher = cells[7]
            opp_pitcher = cells[8]

            dates.append([clean_date])
            home_team.append([team])
            locations.append([location.text])
            opponents.append([opponent.text])

            # win_probs.append([win_prob.text])
            outcomes.append([outcome.text])

            # if scored.text != '':
            #     runs_scored.append([int(scored.text)])
            runs_scored.append([scored.text])
            # if allowed.text != '':
            #     runs_allowed.append([int(allowed.text)])
            runs_allowed.append([allowed.text])
            # time_run.append([time_now])
            opp_pitchers.append([remove_accents(opp_pitcher.text)])

            # win_prob = cells[3]
            # win_probs.append([win_prob.text])

    dates.append(['na'])
    home_team.append(['na'])
    locations.append(['na'])
    opponents.append(['na'])
    outcomes.append(['na'])
    runs_scored.append(['na'])
    runs_allowed.append(['na'])
    opp_pitchers.append(['na'])

    
print(dates)

########## Write to sheet ##########
sheet = "Standings"
print(sheet)

spreadsheet = client.open(book).worksheet(sheet)

spreadsheet.update('A3:A5000', dates)
spreadsheet.update('B3:B5000', home_team)
spreadsheet.update('C3:C5000', locations)
spreadsheet.update('D3:D5000', opponents)
spreadsheet.update('E3:E5000', outcomes)
spreadsheet.update('F3:F5000', runs_scored)
spreadsheet.update('G3:G5000', runs_allowed)
spreadsheet.update('H3:H5000', opp_pitchers)



# # ########## Write to CSV with pandas dataframe ##########

import pandas as pd

df_standings = pd.DataFrame()

# Need double square brackets because of the square brackets in the append statement
    # Square brackets needed in append statement in order to export to Google Sheets
df_standings[['Date']] = dates  
# amended_date = df_standings['Date'].str.split(',', expand=True)
# df_standings['Date'] = amended_date[0]
df_standings[['Team']] = home_team
df_standings[['Loc']] = locations
df_standings[['Opp']] = opponents
# df_standings[['Prob']] = win_probs
df_standings[['WL']] = outcomes
df_standings[['RS']] = runs_scored
df_standings[['RA']] = runs_allowed
df_standings[['Name']] = opp_pitchers

# print(df_standings)


########## Add Pitchers ##########


this_month = 6
today = 10
abb_year = str(int(year) - 2000)

df_pitchers = pd.DataFrame()

# 2022
# for month in range(4,this_month + 1):  # 2022
#     start_day = 1
#     end_day = 32
#     if month == 4:
#         start_day = 7
#     if month == 4 or month == 6 or month == 9:
#         end_day = 31
#     if month == this_month:
#         end_day = today + 1

for month in range(3,this_month + 1):
    start_day = 1
    end_day = 32
    if month == 3:
        start_day = 30
    if month == 4 or month == 6:
        end_day = 31
    if month == this_month:
        end_day = today + 1

    for day in range(start_day,end_day):
        if day < 10:
            url = "/Applications/MAMP/htdocs/Python/WebScraping/MLB/csv_data/pitchers/" + year + "/" + str(month) + "-" + str(day) + "-" + abb_year + ".csv"
            print(url)
        else:
            url = "/Applications/MAMP/htdocs/Python/WebScraping/MLB/csv_data/pitchers/" + year + "/" + str(month) + "-" + str(day) + "-" + abb_year + ".csv"
            print(url)

        csv_pitchers = pd.read_csv(url)
        df_pitchers = df_pitchers.append(csv_pitchers)

# pd.to_numeric(df_pitchers['FIP'], errors='ignore')
# # df_pitchers['ERA'] = df_pitchers['ERA'].astype(float)
df_pitchers['FIP'] = df_pitchers['FIP'].astype(float)


# df_pitchers.fillna({
#     'FIP': 'fuck you'
# })

# pd.set_option('display.max_rows', None)
# print(df_pitchers)

df_standings = pd.merge(df_standings, 
                        df_pitchers, 
                        on=['Date','Opp','Name'], 
                        how='left'  # keeps all values from left dataframe
                        ).fillna({  # Fill empty values
                            'ERA': df_pitchers['ERA'].mean(), 
                            'FIP': df_pitchers['FIP'].mean()}
                        )
                         

df_standings = df_standings[['Date', 'Team', 'Loc', 'Opp', 'WL', 'RS', 'RA', 'Name','ERA', 'FIP']]
# # 2022
# df_standings = df_standings[['Date', 'Team', 'Loc', 'Opp', 'Prob', 'WL', 'RS', 'RA', 'Name','ERA', 'FIP']]


# df_standings = df_standings.sort_values(['Team', 'Date'])

pd.set_option('display.max_rows', None)
print(df_standings)
df_standings.to_csv('/Applications/MAMP/htdocs/Python/WebScraping/MLB/csv_data/standings' + year + '.csv')

# book2 = 'MLBTest'
# # book2 = 'MLBTest2022'
# sheet2 = 'Standings'
# spreadsheet = client.open(book2).worksheet(sheet2)

# spreadsheet.update('A2',[df_standings.columns.values.tolist()] + df_standings.values.tolist())





