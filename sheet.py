import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

# define the scope
# scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

# # authorize the clientsheet 
client = gspread.authorize(creds)

# # get the instance of the Spreadsheet
# sheet = client.open('DKMLB2')
rosters = "Rosters"
sheet = client.open('DKMLB2').worksheet(rosters)

row = 2
new = "change"

sheet.update_cell(row,2, new)

# data = sheet.get_all_records()
# pprint(data)

# # # get the first sheet of the Spreadsheet
# sheet_instance = sheet.get_worksheet(0)

# # get the total number of columns
# sheet_instance.col_count
# # ## >> 26


# # get the value at the specific cell
# sheet_instance.cell(col=3,row=2)
# ## >> <Cell R2C3 '63881'>