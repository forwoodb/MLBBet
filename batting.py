import requests
from bs4 import BeautifulSoup
import pprint
pp = pprint.PrettyPrinter(indent=2)

# # month_day = 'Jun 5'
# year = '2023'

# teams = ['angels', 'astros', 'athletics', 'bluejays', 'braves',
#          'brewers', 'cardinals', 'cubs', 'diamondbacks', 'dodgers',
#          'giants', 'guardians', 'mariners', 'marlins', 'mets',
#           'nationals','orioles', 'padres', 'phillies', 'pirates',
#          'rangers', 'rays', 'reds', 'redsox', 'rockies',
#          'royals', 'tigers', 'twins', 'whitesox','yankees']

# dates = []
# home_team = []
# locations = []
# opponents = []
# win_probs = []
# runs_scored = []
# runs_allowed = []
# # start_pitchers = []
# opp_pitchers = []

# outcomes = []
# print("Games")
# for team in teams:
#     print(team.upper())

#     url = "https://www.fangraphs.com/teams/" + team + "/schedule?season=" + year

#     res = requests.get(url)
#     html = res.text
#     soup = BeautifulSoup(html, 'html.parser')
#     div = soup.find('div', class_='team-schedule-table')
#     table = div.find('table')

#     rows = table.find_all('tr')

#     for row in rows:
#         cells = row.find_all('td')

#         if len(cells) >= 9:
#             date = cells[0]
#             clean_date = date.text.split(',').pop(0)
#             location = cells[1]

#             # Game Day
#             # if clean_date == month_day and location.text == "vs":
#             opponent = cells[2]
#             win_prob = cells[3]
#             scored = cells[5]
#             allowed = cells[6]
#             pitcher = cells[7]
#             opp_pitcher = cells[8]

#             dates.append([clean_date])
#             home_team.append([team])
#             locations.append([location.text])
#             opponents.append([opponent.text])
#             win_probs.append([win_prob.text])
#             # if scored.text != '':
#             #     runs_scored.append([int(scored.text)])
#             runs_scored.append([scored.text])
#             # if allowed.text != '':
#             #     runs_allowed.append([int(allowed.text)])
#             runs_allowed.append([allowed.text])
#             # start_pitchers.append([pitcher.text])
#             opp_pitchers.append([opp_pitcher.text])
    
# print(year)

import pandas as pd

# df_games = pd.DataFrame()

# # Need double square brackets because of the square brackets in the append statement
#     # Square brackets needed in append statement in order to export to Google Sheets
# df_games[['Date']] = dates  
# # amended_date = df_games['Date'].str.split(',', expand=True)
# # df_games['Date'] = amended_date[0]
# df_games[['Team']] = home_team
# df_games[['Loc']] = locations
# df_games[['Opp']] = opponents
# df_games[['RS']] = runs_scored
# df_games[['RA']] = runs_allowed
# # df_games[['tSP']] = start_pitchers
# df_games[['Name']] = opp_pitchers

# print(df_games)

# # # df_games.to_csv(
# # #     # '/Applications/MAMP/htdocs/Python/Django/DataApps/MLBWeb/csv_data/06-18-22/rosters.csv'
# # #     '/Applications/MAMP/htdocs/Python/WebScraping/MLB/csv_data/04-26-23/scores.csv'
# # #     )

# # # pd.set_option('display.max_rows', None)
# # # print(df_games)



year = '2023'

# # min_ip = 'y'  # MLB qualified
# min_ip = '0'


# # Single Day
# month = '06'
# day = '05'



# # url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=y&type=8&season=2023&month=0&season1=2023&ind=0&page=1_50"
# url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=" + min_ip + "&type=8&season=2023&month=1000&season1=2023&ind=0&team=&rost=&age=&filter=&players=&startdate=2023-03-01&enddate=" + year + "-" + month + "-" + day + "&page=1_5000"
# # url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=y&type=8&season=2023&month=1000&season1=2023&ind=0&team=&rost=&age=&filter=&players=&startdate=2023-03-01&enddate=2023-05-03&page=1_5000"

# res = requests.get(url)
# html = res.text
# soup = BeautifulSoup(html, 'html.parser')
# table = soup.find('table', class_='rgMasterTable')
# # print(table)
# # tbody
# # if tbody == None:
# #     pass
# # else:
# tbody = table.find('tbody')
# rows = tbody.find_all('tr')

# # # month_day for Standings
# # if month == 3:
# #     month = 'Mar'
# # elif month == 4:
# #     month = 'Apr'
# # elif month == 5:
# #     month = 'May'
# # elif month == 6:
# #     month = 'Jun'

# print(str(month) + ' ' + str(day))

# # month_days = []
# names = []
# eras = []
# fips = []

# for row in rows:
#     cells = row.find_all('td')
#     name = cells[1]
#     era = cells[17]
#     fip = cells[19]
#     # print(month_day + ' ' + name.text + ' ' + era.text + ' ' + fip.text)

#     # month_day = str(month) + ' ' + str(day)

#     # month_days.append([month_day])
#     names.append([name.text])
#     eras.append([float(era.text)])
#     fips.append([float(fip.text)])

# df_batting = pd.DataFrame()

# # df_batting[['Date']] = month_days 
# df_batting[['Name']] = names
# df_batting[['ERA']] = eras
# df_batting[['FIP']] = fips

# # df_batting = pd.merge(df_games, df_batting, on=['Name','Date'])

# # pd.set_option('display.max_rows', None)
# print(df_batting)

# df_batting.to_csv(
# # '/Applications/MAMP/htdocs/Python/Django/DataApps/MLBWeb/csv_data/06-18-22/rosters.csv'
# '/Applications/MAMP/htdocs/Python/WebScraping/MLB/csv_data/pitchers/' + str(month) + '-' + str(day) + '-23.csv'
# )

# Team Name


# Multiple days

for month in range(6,7): 
    start_day = 9
    end_day = 32
    if month == 3:
        start_day = 30
    if month == 4 or month == 6:
        end_day = 31

    if month == 6:
        end_day = 10

    for day in range(start_day,end_day):
        if day < 10:
            url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2023&month=1000&season1=2023&ind=0&team=0%2Cts&rost=&age=&filter=&players=0&startdate=2023-03-01&enddate=" + year + "-0" + str(month) + "-0" + str(day)
            print(url)
        else:
            url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2023&month=1000&season1=2023&ind=0&team=0%2Cts&rost=&age=&filter=&players=0&startdate=2023-03-01&enddate=" + year + "-0" + str(month) + "-" + str(day)
            # print('0' + str(month) + '-0' + str(day))


        res = requests.get(url)
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', class_='rgMasterTable')
        # print(table)
        # tbody
        # if tbody == None:
        #     pass
        # else:
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')

        # month_day for Standings
        if month == 3:
            this_month = 'Mar'
        elif month == 4:
            this_month = 'Apr'
        elif month == 5:
            this_month = 'May'
        elif month == 6:
            this_month = 'Jun'

        # if day < 10:
        #     today = '0' + str(day)
        # else:
        #     today = str(day)

        # print(str(this_month) + ' ' + str(today))
        
        month_days = []
        teams = []
        obps = []

        for row in rows:
            cells = row.find_all('td')
            team = cells[1]
            obp = cells[14]
            # print(month_day + ' ' + name.text + ' ' + era.text + ' ' + fip.text)

            month_day = this_month + ' ' + str(day + 1)

            month_days.append([month_day])
            teams.append([team.text])
            obps.append([float(obp.text)])

        df_batting = pd.DataFrame()

        df_batting[['Date']] = month_days 
        df_batting[['Team']] = teams
        df_batting[['OBP']] = obps

        # df_batting = pd.merge(df_games, df_batting, on=['Name','Date'])

        # pd.set_option('display.max_rows', None)
        print(df_batting)

        # df_batting.to_csv(
        #     # '/Applications/MAMP/htdocs/Python/Django/DataApps/MLBWeb/csv_data/06-18-22/rosters.csv'
        #     '/Applications/MAMP/htdocs/Python/WebScraping/MLB/csv_data/batting/' + str(month) + '-' + str(day) + '-23.csv',
        #     index=False
        # )



    