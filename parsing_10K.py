##############################################################################################
# import libraries
##############################################################################################

# import our libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup

##############################################################################################
# grab the filing xml summary
##############################################################################################

# define the base url needed to create the file url.
base_url = r"https://www.sec.gov"

# convert a normal url to a document url
normal_url = r"https://www.sec.gov/Archives/edgar/data/1265107/0001265107-19-000004.txt"
normal_url = normal_url.replace('-','').replace('.txt','/index.json')

# define a url that leads to a 10k document landing page
documents_url = r"https://www.sec.gov/Archives/edgar/data/1265107/000126510719000004/index.json"

# request the url and decode it.
content = requests.get(documents_url).json()

for file in content['directory']['item']:
    
    # Grab the filing summary and create a new url leading to the file so we can download it.
    if file['name'] == 'FilingSummary.xml':

        xml_summary = base_url + content['directory']['name'] + "/" + file['name']
        
        print('-' * 100)
        print('File Name: ' + file['name'])
        print('File Path: ' + xml_summary)

##############################################################################################
# parsing the filing summary
##############################################################################################

# define a new base url that represents the filing folder. This will come in handy when we need to download the reports.
base_url = xml_summary.replace('FilingSummary.xml', '')

# request and parse the content
content = requests.get(xml_summary).content
soup = BeautifulSoup(content, 'lxml')

# find the 'myreports' tag because this contains all the individual reports submitted.
reports = soup.find('myreports')

# I want a list to store all the individual components of the report, so create the master list.
master_reports = []

# loop through each report in the 'myreports' tag but avoid the last one as this will cause an error.
for report in reports.find_all('report')[:-1]:

    # let's create a dictionary to store all the different parts we need.
    report_dict = {}
    report_dict['name_short'] = report.shortname.text
    report_dict['name_long'] = report.longname.text
    report_dict['position'] = report.position.text
    report_dict['category'] = report.menucategory.text
    report_dict['url'] = base_url + report.htmlfilename.text

    # append the dictionary to the master list.
    master_reports.append(report_dict)

    # print the info to the user.
    print('-'*100)
    print(base_url + report.htmlfilename.text)
    print(report.longname.text)
    print(report.shortname.text)
    print(report.menucategory.text)
    print(report.position.text)