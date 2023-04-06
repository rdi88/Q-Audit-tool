import os
import time
from selenium import webdriver
import glob
import requests
import json
import pandas as pd
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta, timezone

#Webhook URL
url = 'https://hooks.chime.aws/incomingwebhooks/48d335bb-77ef-421e-960b-368c0c29c168?token=cmp1T3Y2RXN8MXxNaUduQk5wcVdyazZJaUkxbU1YdVM4M0V4cjJSNnQwVDJaOFhDTTlqc09N'


#fetching midway cookie
def get_mwinit_cookie():
    MidwayConfigDir = os.path.join(os.path.expanduser("~"), ".midway")
    MidwayCookieJarFile = os.path.join(MidwayConfigDir, "cookie")
    fields = []
    keyfile = open(MidwayCookieJarFile, "r")
    for line in keyfile:
        # parse the record into fields (separated by whitespace)
        fields = line.split()
        if len(fields) != 0:
            # get the yubi session token and expire time
            if fields[0] == "#HttpOnly_midway-auth.amazon.com":
                session_token = fields[6].replace("\n", "")
                expires = fields[4]
            # get the user who generated the session token
            elif fields[0] == "midway-auth.amazon.com":
                username = fields[6].replace("\n", "")
    #keyfile.close()
    # make sure the session token hasn't expired
    if time.gmtime() > time.gmtime(int(expires)):
        raise SystemError("Your Midway token has expired. Run mwinit to renew")
    # construct the cookie value required by calls to k2
    cookie = {"username": username, "session": session_token}
    return cookie

#Once We have the function to fetch cookies we can add the fetched cookies to selenium Browser.

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Firefox(service=FirefoxService(executable_path=GeckoDriverManager().install()))
midway_url = 'https://issues.amazon.com/issues/search?q=containingFolder%3A(8bf39aff-61c2-42c5-84c6-f0e70037978a+OR+ab581ba7-9201-4846-9f2d-c300f2dbaa56+OR+8e0510b4-b0dc-4823-a7a0-be5440d19eb4+OR+8bf39aff-61c2-42c5-84c6-f0e70037978a+OR+f28d4a06-61e2-4259-a411-19fbb3bb2b31+OR+615224c5-5f17-41f9-9fa8-81bbfafd4634+OR+891ae51c-6da5-4959-bb5a-3c8093402eb2+OR+d759d1b3-a363-48ef-a9c6-7f4293827ce7+OR+53b9a5d6-7f91-47f8-8886-3f7890669952+OR+81700399-d08d-4f2b-9af9-c693d5d88e45+OR+2cef5079-d2c1-4fb3-bb7d-edee851e29b9)+requester%3A(qdarchan+OR+amznhk+OR+orrathik+OR+aravnz+OR+smjya+OR+prarul+OR+tranadee+OR+vinodhia+OR+slak+OR+kasidevi+OR+gandhid+OR+aisshwav+OR+bbalak)+createDate%3A(%5B2022-03-31T18%3A30%3A00.000Z..%5D)+lastUpdatedDate%3A(%5BNOW-7DAYS..NOW%5D)&sort=createDate+asc&selectedDocument=3322b622-ef12-47e5-b418-d7f81a500146'
cookie = get_mwinit_cookie()
driver.get(midway_url)
cookie_dict1 = {'domain': '.midway-auth.amazon.com',
                'name': 'user_name',
                'value': cookie['username'],
                'path': '/',
                'httpOnly': False,
                'secure': True}

cookie_dict2 = {'Domain': 'sim.amazon.com',
                'name': 'session',
                'value': cookie['session'],
                'path': '/',
                'httpOnly': True,
                'secure': True}

driver.add_cookie(cookie_dict1)
driver.add_cookie(cookie_dict2)

match = False
while not match:
    driver.get(midway_url)
    #time.sleep(3)
    if driver.current_url == 'https://issues.amazon.com/issues/search?q=containingFolder%3A(8bf39aff-61c2-42c5-84c6-f0e70037978a+OR+ab581ba7-9201-4846-9f2d-c300f2dbaa56+OR+8e0510b4-b0dc-4823-a7a0-be5440d19eb4+OR+8bf39aff-61c2-42c5-84c6-f0e70037978a+OR+f28d4a06-61e2-4259-a411-19fbb3bb2b31+OR+615224c5-5f17-41f9-9fa8-81bbfafd4634+OR+891ae51c-6da5-4959-bb5a-3c8093402eb2+OR+d759d1b3-a363-48ef-a9c6-7f4293827ce7+OR+53b9a5d6-7f91-47f8-8886-3f7890669952+OR+81700399-d08d-4f2b-9af9-c693d5d88e45+OR+2cef5079-d2c1-4fb3-bb7d-edee851e29b9)+requester%3A(qdarchan+OR+amznhk+OR+orrathik+OR+aravnz+OR+smjya+OR+prarul+OR+tranadee+OR+vinodhia+OR+slak+OR+kasidevi+OR+gandhid+OR+aisshwav+OR+bbalak)+createDate%3A(%5B2022-03-31T18%3A30%3A00.000Z..%5D)+lastUpdatedDate%3A(%5BNOW-7DAYS..NOW%5D)&sort=createDate+asc&selectedDocument=3322b622-ef12-47e5-b418-d7f81a500146':
        match = True
    time.sleep(1)
    #driver.refresh()
driver.maximize_window()

wait1 = WebDriverWait(driver, 30)
wait1.until(EC.element_to_be_clickable(
    (By.XPATH, '/html/body/div[1]/div/div[1]/div[1]/div/div[1]/div/div[1]/div[1]/div[1]/div[1]/div/button[1]'))).click()
# 2.Downloadingcsvfile
driver.find_element(by=By.XPATH,
                    value='/html/body/div[1]/div/div[1]/div[1]/div/div[1]/div/div[1]/div[1]/div[1]/div[1]/div/ul/li[1]/a').click()

export_button = wait1.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submit-custom-export-job"]')))
# scrolldown
driver.execute_script("arguments[0].scrollIntoView();", export_button)
wait1.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submit-custom-export-job"]'))).click()
wait1.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div[1]/div/div/div/div[1]/div/section[1]/div/section/div/div/table/tbody/tr/td[1]/a'))).click()
time.sleep(5)

# 3.Selecting recently downloaded csv file
os.chdir("C:/Users/amznhk/Downloads")
csv_files = glob.glob("*.csv")
if len(csv_files) > 0:
    csv_files.sort(key=os.path.getmtime)
    most_recently_downloaded_file = csv_files[-1]
    df = pd.read_csv(most_recently_downloaded_file)
    print(most_recently_downloaded_file)

# Calculating total issues
total_issues_audited = len(df)
label = list()
# labels
for i in range(len(df)):
    label = str(df.loc[i, "Labels"])

# To print improper sims:
not_proper_issues = []
result = 0
not_valid_deviation = []
result1 = 0
# Close webdriver
driver.close()
# To validate required columns are present
if all([item in df.columns for item in ['IssueUrl', 'RequesterIdentity', 'Status', 'Labels', 'Tags', 'RootCauses', 'Resolution (string)', 'AssignedFolderLabel', 'ResolvedDate']]):
    # For open sims:
    # For open sims:
    for i in range(len(df)):
        if 'Open' in df.loc[i, "Status"]:
            if 'GDQ_QS_Detected_AWS_AppStream' not in str(df.loc[i, "Labels"]):
                if 'SKIP_AUDIT' not in str(df.loc[i, "Labels"]) and "AWS AppStream VOC" not in df.iloc[i, 'AssignedFolderLabel'] and '[Project] AS2 Seamless Logon' not in df.iloc[i, "AssignedFolderLabel"] and 'General Bug Backlog' not in df.iloc[i, "AssignedFolderLabel"]:
                    if 'QS_Adhoc' not in str(df.loc[i, "Labels"]) and 'QS_Testcase' not in str(df.loc[i, "Labels"]):
                        result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' Label missing: GDQ and QS_Adhoc/QS_Testcase or SKIP_AUDIT label')
                        not_proper_issues.append(result)
                    elif 'QS_Adhoc' in str(df.loc[i, "Labels"]) and 'QS_Testcase' in str(df.loc[i, "Labels"]):
                        result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' Both QS_Adhoc and QS_Testcase present')
                        not_proper_issues.append(result)
                    elif 'QS_Adhoc' in str(df.loc[i, "Labels"]) or 'QS_Testcase' in str(df.loc[i, "Labels"]):
                        result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' GDQ_QS_Detected_AWS_AppStream/Chime_SDK not present')
                        not_proper_issues.append(result)
                    elif 'QS_Adhoc' in str(df.loc[i, "Labels"]) and 'DA-TestCase' in str(df.loc[i, "Tags"]):
                        result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' Label mismatch: Adhoc label and Testcase tag')
                        not_proper_issues.append(result)
                    elif 'QS_Testcase' in str(df.loc[i, "Labels"]) and 'DA-Adhoc' in str(df.loc[i, "Tags"]):
                        result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' Label mismatch: Testcase label and Adhoc tag')
                        not_proper_issues.append(result)
            elif 'GDQ_QS_Detected_AWS_AppStream' in str(df.loc[i, "Labels"]):
                if 'SKIP_AUDIT' not in str(df.loc[i, "Labels"]) and "AWS AppStream VOC" not in df.iloc[i, 'AssignedFolderLabel'] and '[Project] AS2 Seamless Logon' not in df.iloc[i, "AssignedFolderLabel"] and 'General Bug Backlog' not in df.iloc[i, "AssignedFolderLabel"]:
                    if 'QS_Adhoc' not in str(df.loc[i, "Labels"]) and 'QS_Testcase' not in str(df.loc[i, "Labels"]):
                        result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + " Label missing: QS_Adhoc or QS_Testcase")
                        not_proper_issues.append(result)
                    elif 'QS_Adhoc' in str(df.loc[i, "Labels"]) and 'QS_Testcase' in str(df.loc[i, "Labels"]):
                        result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' Both QS_Adhoc and QS_Testcase present')
                        not_proper_issues.append(result)
                    elif 'QS_Adhoc' in str(df.loc[i, "Labels"]) and 'DA-TestCase' in str(df.loc[i, "Tags"]):
                        result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' Label mismatch: Adhoc label and Testcase tag')
                        not_proper_issues.append(result)
                    elif 'QS_Testcase' in str(df.loc[i, "Labels"]) and 'DA-Adhoc' in str(df.loc[i, "Tags"]):
                        result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' Label mismatch: Testcase label and Adhoc tag')
                        not_proper_issues.append(result)
        elif 'Resolved' in df.loc[i, "Status"]:
            if 'QS_Detected_Valid' in str(df.loc[i, "Labels"]) and 'QS_Detected_Invalid' in str(df.loc[i, "Labels"]):
                result = ('@' + df.loc[i, "RequesterIdentity"] + "- " + df.loc[i, "IssueUrl"] + " Both valid and invalid label is present")
                not_proper_issues.append(result)
            elif 'QS_Detected_Valid' not in str(df.loc[i, "Labels"]) and 'QS_Detected_Invalid' not in str(df.loc[i, "Labels"]):
                if 'SKIP_AUDIT' not in str(df.loc[i, "Labels"]) and "AWS AppStream VOC" not in df.iloc[i, 'AssignedFolderLabel'] and '[Project] AS2 Seamless Logon' not in df.iloc[i, "AssignedFolderLabel"] and 'General Bug Backlog' not in df.iloc[i, "AssignedFolderLabel"]:
                    if 'Fixed' in str(df.loc[i, "Tags"]) and 'Fixed' not in str(df.loc[i, "Resolution (string)"]):
                        date_string = df.loc[i, "ResolvedDate"]
                        datetime_obj = datetime.fromisoformat(date_string).replace(tzinfo=timezone.utc)
                        # Get the current datetime object in UTC timezone
                        now = datetime.now(timezone.utc)
                        if now.weekday() == 0:
                            # Check if the datetime object is more than 72 hours ago
                            if now - datetime_obj > timedelta(hours=72):
                                result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' No QS_Detected_Valid/Invalid label, Resolution/ SKIP_AUDIT label more than 72 hours passed since resolved')
                                not_proper_issues.append(result)
                            else:
                                result1 = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' No QS_Detected_Valid/Invalid label, Resolution/ SKIP_AUDIT label less than 72 hours passed since resolved')
                                not_valid_deviation.append(result1)
                        else:
                            # Check if the datetime object is less than 24 hours ago
                            if now - datetime_obj > timedelta(hours=24):
                                result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' No QS_Detected_Valid/Invalid label, Resolution/ SKIP_AUDIT label more than 24 hours passed since resolved')
                                not_proper_issues.append(result)
                            else:
                                result1 = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' No QS_Detected_Valid/Invalid label, Resolution/ SKIP_AUDIT label less than 24 hours passed since resolved')
                                not_valid_deviation.append(result1)
                    else:
                        date_string = df.loc[i, "ResolvedDate"]
                        datetime_obj = datetime.fromisoformat(date_string).replace(tzinfo=timezone.utc)
                        # Get the current datetime object in UTC timezone
                        now = datetime.now(timezone.utc)
                        if now.weekday() == 0:
                            # Check if the datetime object is more than 72 hours ago
                            if now - datetime_obj > timedelta(hours=72):
                                result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' No QS_Detected_Valid/Invalid label/ SKIP_AUDIT label resolved time passed 72 hours ')
                                not_proper_issues.append(result)
                            else:
                                result1 = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' No QS_Detected_Valid/Invalid label/ SKIP_AUDIT label resolved within 72 hours')
                                not_valid_deviation.append(result1)
                        else:
                            # Check if the datetime object is less than 24 hours ago
                            if now - datetime_obj > timedelta(hours=24):
                                result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' No QS_Detected_Valid/Invalid label/ SKIP_AUDIT label resolved time passed 24 hours')
                                not_proper_issues.append(result)
                            else:
                                result1 = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' No QS_Detected_Valid/Invalid label/ SKIP_AUDIT label resolved within 24 hours')
                                not_valid_deviation.append(result1)
            elif 'QS_Detected_Valid' in str(df.loc[i, "Labels"]) or 'QS_Detected_Invalid' in str(df.loc[i, "Labels"]):
                if 'Fixed' in str(df.loc[i, "Tags"]) and 'Fixed' not in str(df.loc[i, "Resolution (string)"]):
                    if 'SKIP_AUDIT' not in str(df.loc[i, "Labels"]) and "AWS AppStream VOC" not in df.iloc[i, 'AssignedFolderLabel'] and '[Project] AS2 Seamless Logon' not in df.iloc[i, "AssignedFolderLabel"] and 'General Bug Backlog' not in df.iloc[i, "AssignedFolderLabel"]:
                        result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' No Fixed Resolution')
                        not_proper_issues.append(result)
                elif 'GDQ_QS_Detected_AWS_AppStream' not in str(df.loc[i, "Labels"]):
                    if 'QS_Adhoc' not in str(df.loc[i, "Labels"]) and 'QS_Testcase' not in str(df.loc[i, "Labels"]):
                        result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' GDQ_QS_Detected_AWS_AppStream/Chime_SDK, QS_Adhoc or QS_Testcase for closed sim')
                        not_proper_issues.append(result)
                    elif 'QS_Adhoc' in str(df.loc[i, "Labels"]) and 'QS_Testcase' in str(df.loc[i, "Labels"]):
                        result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' Both QS_Adhoc and QS_Testcase present for closed sim')
                        not_proper_issues.append(result)
                    elif 'QS_Adhoc' in str(df.loc[i, "Labels"]) or 'QS_Testcase' in str(df.loc[i, "Labels"]):
                        result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' GDQ_QS_Detected_AWS_AppStream/Chime_SDK not present for closed sim')
                        not_proper_issues.append(result)
                    elif 'QS_Adhoc' in str(df.loc[i, "Labels"]) and 'DA-TestCase' in str(df.loc[i, "Tags"]):
                        result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' Label mismatch: Adhoc label and Testcase tag for closed sim')
                        not_proper_issues.append(result)
                    elif 'QS_Testcase' in str(df.loc[i, "Labels"]) and 'DA-Adhoc' in str(df.loc[i, "Tags"]):
                        result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' Label mismatch: Testcase label and Adhoc tag for closed sim')
                        not_proper_issues.append(result)
                elif 'GDQ_QS_Detected_AWS_AppStream' in str(df.loc[i, "Labels"]):
                    if 'QS_Adhoc' not in str(df.loc[i, "Labels"]) and 'QS_Testcase' not in str(df.loc[i, "Labels"]):
                        result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + " QS_Adhoc or QS_Testcase for closed sim")
                        not_proper_issues.append(result)
                    elif 'QS_Adhoc' in str(df.loc[i, "Labels"]) and 'QS_Testcase' in str(df.loc[i, "Labels"]):
                        result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' Both QS_Adhoc and QS_Testcase present for closed sim')
                        not_proper_issues.append(result)
                    elif 'QS_Adhoc' in str(df.loc[i, "Labels"]) and 'DA-TestCase' in str(df.loc[i, "Tags"]):
                        result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' Label mismatch: Adhoc label and Testcase tag for closed sim')
                        not_proper_issues.append(result)
                    elif 'QS_Testcase' in str(df.loc[i, "Labels"]) and 'DA-Adhoc' in str(df.loc[i, "Tags"]):
                        result = ('@' + df.loc[i, "RequesterIdentity"] + " - " + df.loc[i, "IssueUrl"] + ' Label mismatch: Testcase label and Adhoc tag for closed sim')
                        not_proper_issues.append(result)
    valid_deviation = len(not_proper_issues)
    invalid_deviation = len(not_valid_deviation)
    print(valid_deviation)
    print(invalid_deviation)
    # webhook
    if invalid_deviation == 0 and valid_deviation == 0:
        header = '/md **Total Issue Audited : ' + str(total_issues_audited)
        message = '**\n **Audit completed! No miss found**'
        table = header + message
        playload = {'Content': table}
        headers = {"Content-Type": "application/json"}
        r = requests.post(url, data=json.dumps(playload), headers=headers)
        print(r)
        print(r.text)
        print(table)
    elif invalid_deviation == 0 and valid_deviation > 0:
        header = '/md **Total Issue Audited : ' + str(total_issues_audited)
        message = '**\n\n **Deviation = ' + str(valid_deviation) + '** \n ***UserID - SIM ID - Missed*** \n ' + str(
            '\n'.join(not_proper_issues))
        table = header + message
        playload = {'Content': table}
        headers = {"Content-Type": "application/json"}
        r = requests.post(url, data=json.dumps(playload), headers=headers)
        print(r)
        print(r.text)
        print(table)
    elif valid_deviation == 0 and invalid_deviation > 0:
        header = '/md **Total Issue Audited : ' + str(total_issues_audited)
        message = '**\n **Non deviations = ' + str(
            invalid_deviation) + '** \n ***UserID - SIM ID - Missed*** \n ' + str('\n'.join(not_valid_deviation))
        table = header + message
        playload = {'Content': table}
        headers = {"Content-Type": "application/json"}
        r = requests.post(url, data=json.dumps(playload), headers=headers)
        print(r)
        print(r.text)
        print(table)
    else:
        header = '/md **Total Issue Audited : ' + str(total_issues_audited)
        message = '**\n\n **Deviation = ' + str(valid_deviation) + '** \n ***UserID - SIM ID - Missed*** \n ' + str(
            '\n'.join(not_proper_issues)) + '\n\n **Non deviations = ' + str(
            invalid_deviation) + '** \n ***UserID - SIM ID - Missed*** \n ' + str('\n'.join(not_valid_deviation))
        table = header + message
        playload = {'Content': table}
        headers = {"Content-Type": "application/json"}
        r = requests.post(url, data=json.dumps(playload), headers=headers)
        print(r)
        print(r.text)
        print(table)
else:
    header = '/md **Audit not completed as required columns are not present in the doc downloaded**'
    playload = {'Content': header}
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, data=json.dumps(playload), headers=headers)
    print(r)
    print(r.text)
# Delete the file
os.remove(most_recently_downloaded_file)