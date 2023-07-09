from oauth2client.service_account import ServiceAccountCredentials
import gspread
import requests
from bs4 import BeautifulSoup

url = "https://www.lines.com/betting/mlb/odds/book-7"
res = requests.get(url)
html = res.text
soup = BeautifulSoup(html, 'html.parser')

games = soup.find_all(class_='odds-list-panel')

teams_list = []
ou_list = []
ml_list = []

for game in games:
    teams = game.find_all(class_='odds-list-team-title-xs')
    odds = game.find_all(class_='odds-list-panel-col')

    for team in teams:
        score = team.find(class_='team-score')
        score.decompose()
        teams_list.append([team.text.strip()])  # Need square brackets to output to spreadsheet

    for col in odds:
        title = col.find(class_='odds-col-title').text.strip()
        if title == 'O/U':
            ou = col.find_all(class_='odds-list-val')
            for i in ou:
                span = i.find('span').decompose()
                ou_list.append([float(i.text.strip('o').strip('u'))])

        if title == 'M/L':
            ml = col.find_all(class_='odds-list-val')
            for i in ml:
                ml_list.append([int(i.text.strip('+'))])

print(ou_list)

# scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
#          "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
# client = gspread.authorize(creds)
# book = 'DKMLB2'
# sheet = "DKOdds"
# spreadsheet = client.open(book).worksheet(sheet)

# spreadsheet.update('A2:A820', teams_list)
# spreadsheet.update('B2:B820', ou_list)
# spreadsheet.update('C2:C820', ml_list)
