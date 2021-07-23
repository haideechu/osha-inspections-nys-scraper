import pandas as pd
import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.osha.gov/pls/imis/establishment.search?establishment=&state=NY&officetype=all&office=253600&sitezip=100000&startmonth=01&startday=01&startyear=2021&p_case=all&p_violations_exist=both&p_show=99999')
doc = BeautifulSoup(response.text, 'html.parser')
tables = doc.select('table.table')
records = tables[2]
rows = records.find_all('tr')

inspections = []
url_list = []
for row in rows:
    a = row.find_all('a')
    for hrefs in a:
        href = hrefs.get('href')
        url = f'https://www.osha.gov/pls/imis/{href}'
        url_list.append(url)
    cells = row.find_all('td')
    row_list = []
    for cell in cells:
        row_list.append(cell.text)
    inspections.append(row_list)

df = pd.DataFrame(inspections)
df.drop(index=df.index[0], axis=0, inplace=True)
df['inspection_url'] = url_list
df = df.drop(columns={0,1,2})

df = df.rename(columns ={
    3: 'date_opened',
    4: 'report_id',
    5: 'state',
    6: 'inspection_type',
    7: 'scope',
    8: 'sic_code',
    9: 'naics_code',
    10: 'violations',
    11: 'establishment_name'
})

df.to_csv('osha-inspection-nys.csv')
