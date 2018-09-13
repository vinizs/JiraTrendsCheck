import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import base64
import getpass
import os

#disable warnings in requests
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#username is what you are using on machine
username=os.environ['LOGNAME']
password=getpass.getpass('Password for '+username+': ')

#aPIbase URL
jira_server='https://jira2.workday.com/rest/api/2/search?'

#All jiras from https://confluence.workday.com/display/SUPOPS/New+Trending+Report (Jiras that are already created for trending items)
Trends_filter='jql=filter%3D100089&fields=customfield_10302,key,customfield_14621'

#All FGCs in the past 24-42 hours
Daily_filter='jql=filter%3D100745&fields=customfield_10302,key,customfield_14621&maxResults=100'

#All FGCs for the past Month
Thirty_filter='jql=filter%3D91177&fields=customfield_10302,customfield_14621,key&maxResults=1000'

#NON API Base URL
jira2 = "https://jira2.workday.com/" 

#Store trending Customers to compare 
Customer =[]
Possible_Trend = []
Repeat = []

#Store the jiras that might be trending so we can reference them if needed
Issue = []

#API requests based on the three queries (Daily_filter, Trends_Filter, Thirty_Filter) 
os.system('clear')
print ('Loading 1/3\n')
response1=requests.request('GET', jira_server+Trends_filter, verify=True, auth=(username,password))
Trends_Response = json.loads(response1.text)

os.system('clear')
print ('Loading 2/3\n')
response2=requests.request('GET', jira_server+Daily_filter, verify=True, auth=(username,password))
Daily_Response = json.loads(response2.text)

os.system('clear')
print ('Loading 3/3\n')
response3=requests.request("GET", jira_server+Thirty_filter, verify=True, auth=(username,password))
Monthly_Response = json.loads(response3.text)

os.system('clear')
print ('Loading DONE!\n')

#Go Through all the issues That are trending
for a in Trends_Response['issues']:

    #Check if we have stored them already
    if a['fields']['customfield_10302'][0]['value'] not in Customer:
        #Store trending customers to reference them later
        Customer.append(a['fields']['customfield_10302'][0]['value'])
    



#Go Through the issues for the past 42 hours
for item in Daily_Response['issues']:

    #Check the Trends Again (This could be easier but this line works so I don't want to change it.) 
    for stuff in Trends_Response['issues']:
        # Check the there is an issue the past 42 hours that has a customer already trending  
        if item['fields']['customfield_10302'][0]['id'] == stuff['fields']['customfield_10302'][0]['id']:
                #Lets link this jira to the trending jira
                print("Already trend:", item['key'], " ", stuff['fields']['customfield_10302'][0]['value'], jira2, "browse/", stuff['key'],  "\n", sep='')
                
    #Lets open the Issues over the past month
    for i in Monthly_Response['issues']:

        #Has this customer seen an issue the past 30 days? 
        if item['fields']['customfield_10302'][0]['id'] == i['fields']['customfield_10302'][0]['id']:
            #Rule out that it is this same jira as this one
            if item['key'] != i['key']:
                #Have we already checked this jira?
                if item['key'] not in Issue:
                    Issue.append(item['key'])

                    #Make sure they are not Trending already
                    if item['fields']['customfield_10302'][0]['value'] not in Customer:
                        if item['fields']['customfield_10302'][0]['value'] not in Possible_Trend:
                            Possible_Trend.append(item['fields']['customfield_10302'][0]['value'])

                

for i in Possible_Trend:
    print("Customer:",i, "is possibly a Trend. Here is a list of issues That has happend over the past month: ")

    for b in Monthly_Response['issues']:

        if i == b['fields']['customfield_10302'][0]['value']:
              print(b['key'],"Root Cause:", b['fields']['customfield_14621'])


            
            
        


        
        
