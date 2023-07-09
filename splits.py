######### Time Testing ##########
# https://datatofish.com/measure-time-to-run-python-script/

import time
startTime = time.time()

########## Import data ##########

startTime_import = time.time()

# from oauth2client.service_account import ServiceAccountCredentials
# import gspread
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from pprint import pprint
import unicodedata

executionTime_import = (time.time() - startTime_import)
print('Time to import modules: ' + str(executionTime_import))

startTime_scrape = time.time()

########## Date ##########

year = '2022'
month = '06'
day = '23'


options = Options()
options.headless = True  
options.add_argument("--window-size=1920,1200")

service = Service(GeckoDriverManager().install())
# service = Service(
#     executable_path='/Applications/MAMP/htdocs/Python/WebScraping/Selenium/ScrapingBee/geckodriver')
driver = webdriver.Firefox(service=service, options=options)

p_splits = [ 
    # ("FGHittersvL","https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=1&splitArrPitch=&position=B&autoPt=true&splitTeams=false&statType=player&statgroup=2&startDate=2022-03-01&endDate=" + year + "-" + month + "-" + day + "&players=&filter=&groupBy=season&wxTemperature=&wxPressure=&wxAirDensity=&wxElevation=&wxWindSpeed=&sort=22,1&pageitems=10000000000000&pg=0"),
    ("FGHittersvR","https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=2&splitArrPitch=&position=B&autoPt=true&splitTeams=false&statType=player&statgroup=2&startDate=2022-03-01&endDate=" + year + "-" + month + "-" + day + "&players=&filter=&groupBy=season&wxTemperature=&wxPressure=&wxAirDensity=&wxElevation=&wxWindSpeed=&sort=22,1&pageitems=10000000000000&pg=0")
]

# # v LHP
# url = "https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=1&splitArrPitch=&position=B&autoPt=true&splitTeams=false&statType=player&statgroup=2&startDate=2022-03-01&endDate=" + year + "-" + month + "-" + day + "&players=&filter=&groupBy=season&wxTemperature=&wxPressure=&wxAirDensity=&wxElevation=&wxWindSpeed=&sort=22,1&pageitems=10000000000000&pg=0"
# sheetName = "FGHittersvL"

# # v RHP
# url = "https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=2&splitArrPitch=&position=B&autoPt=true&splitTeams=false&statType=player&statgroup=2&startDate=2022-03-01&endDate=" + year + "-" + month + "-" + day + "&players=&filter=&groupBy=season&wxTemperature=&wxPressure=&wxAirDensity=&wxElevation=&wxWindSpeed=&sort=22,1&pageitems=10000000000000&pg=0"
# sheetName = "FGHittersvR"

for sheetName, url in p_splits:
    driver.get(url)
    # driver.get("https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=1&splitArrPitch=&position=B&autoPt=true&splitTeams=false&statType=player&statgroup=2&startDate=2022-03-01&endDate=2022-06-01&players=&filter=&groupBy=season&wxTemperature=&wxPressure=&wxAirDensity=&wxElevation=&wxWindSpeed=&sort=22,1&pageitems=10000000000000&pg=0")
    # table = driver.find_element(By.XPATH, "//div[@class='table-scroll']/table/tbody/tr").text

    players = driver.find_elements(By.XPATH, "//div[@class='table-scroll']/table/tbody/tr")
    player_splits = len(players)

    splits = []

    # https://getridbug.com/mysql/looping-through-a-dynamic-table-python/


    def remove_accents(text):
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore')
        return text.decode('utf-8')

    for i in range(player_splits):
        data = {
            'name': remove_accents(players[i].find_element(By.XPATH,"./td[3]").text),
            'woba': players[i].find_element(By.XPATH,"./td[17]").text,
            'iso': players[i].find_element(By.XPATH,"./td[13]").text,
            'avg': players[i].find_element(By.XPATH,"./td[9]").text,
        }
        # print(data)

        splits.append(data)

    print("---------- Splits List ----------")
    # print(splits)

    executionTime_import = (time.time() - startTime_import)
    print('Time to scrape data: ' + str(executionTime_import))


    ########## Write to sheet ##########

    from oauth2client.service_account import ServiceAccountCredentials
    import gspread

    # Connect to Sheets
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)


    client = gspread.authorize(creds)
    workbook = 'DKMLB2'
    spreadsheet = client.open(workbook)
    worksheet = spreadsheet.worksheet(sheetName)

    header_to_key = {
        'Name': 'name',
        'wOBA': 'woba',
        'ISO': 'iso',
        'AVG': 'avg'
    }

    headers = worksheet.row_values(1)
    # temp = []
    # for h in headers:
    #     print(header_to_key[h])
    #     temp.append(header_to_key[h])
    # print(temp)

    put_values = []
    print("---------- Put Values ----------")
    for v in splits:
        # pprint(v)
        temp = []
        for h in headers:
            temp.append(v[header_to_key[h]])
        # pprint(temp)
        put_values.append(temp)

    # pprint(put_values)


    spreadsheet.values_append(sheetName, {'valueInputOption': 'USER_ENTERED'}, {
                            'values': put_values})

    driver.close()


    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(executionTime))










# # # from StackOverflow https://stackoverflow.com/questions/60424508/python-gspread-how-to-populate-google-sheet-dictionaries-within-list

# spreadsheetId = "DKMLB2"  # Please set the Spreadsheet ID.
# sheetName = "FGHittersvL"  # Please set the sheet name.

# Test export with static data
# sheet_data = [{
#     "timestamp": "09-04-2019",
#     "value": "10.0",
#     "company_name": "Xbox",
#     "product": "Buy"
# }, {
#     "timestamp": "09-03-2019",
#     "value": "2.0",
#     "company_name": "something",
#     "product": "Sell"
# }]

# header_to_key = {
#     'Date': 'timestamp',
#     'Company_Name': 'company_name',
#     'Traffic': 'value',
#     'Product': 'product'
# # }

# client = gspread.authorize(creds)
# # spreadsheet = client.open_by_key(spreadsheetId)
# spreadsheet = client.open(spreadsheetId)
# worksheet = spreadsheet.worksheet(sheetName)

# # Read headers in sheet
# headers = worksheet.row_values(1)

# put_values = []
# for v in sheet_data:
#     temp = []
#     for h in headers:
#         temp.append(v[header_to_key[h]])
#     put_values.append(temp)
# spreadsheet.values_append(sheetName, {'valueInputOption': 'USER_ENTERED'}, {
#                           'values': put_values})

