# Q-Desk Bug audit script - Phase 2

#### Problem statement 
Global device quality(GDQ) labels and resolution/ closure code was brought in for organisation level audit process. There were lot of misses been happening in the team where any of the label or resolution/ closure code were not added correctly and certain mismatch of labels also occurred. Manual audit performed everyday would take 20 minutes and chances of misses/data errors.

#### Proposed Solution

To mitigate the manual effort of auditing the labels and resolution/ closure code. We can automate the audit process and time taken to convey the misses to the particular user.

#### Implented solution 
  
Implemented a script using python and pandas library which audits bug data has the appropriate labels, tags, rootcause and resolution/closure code. When the SIM or Tcorp does not meet the condition, script will return the user id and SIM or Tcorp link. Through Chime webhook the misses will be posted in a chatroom @mentioning the user along with SIM or Tcorp link and what is missed.

#### Packages used 
Pandas - To read the csv file and to compare between rows to check if it passes given conditions
Requests API - Its a API to get the output and post them in the chime chatroom 
Webdriver_manager- To manage the webdriver which is goining to run the script. (It downloads the latest browser version)
Selenium - To automate the downloading process of csv file from filter URL

#### How script work?
**Midway bypass**
It is used to bypass the manual entering of user id and password in automated browser. By this we can avoid security breach of entering password in code for login. User have to run mwinit command in their system and authenticate the midway in terminal/ command prompt. A cookie will store the user id and security key. This cookie is pushed to automated brower when browser requires to login midway. 

**Webdriver manager (firefox)**
Firefox browser is in the script and webdriver manager will download the latest GeckoDriver. By this we can avoid having a frequent check of latest GeckoDriver release and avoid updation of the path in the code. 

**Filter**
Have a filter with requestors (Including all the teammates present and past), Folder of your team, Create date set to april 01 2022 (The time where QDesk label was manditory) and last update set as per team request. Once this filter URL is given code will download the dump shown in the filter. 

**Download the Dump**
The dump is to be downloaded as CSV file with the required columns. The path is then set to CSV latest file in downloads. To verify the correct file is selected for audit, the filename is printed in terminal.

**Conditions checked in the script  (Subjected to change accroding to the team)**
- If the required columns are present in the downloaded dumps to check
- If the sim is in open state -
	- Label misses: GDQ and QS_Adhoc/QS_Testcase or SKIP_AUDIT label
	- Both QS_Adhoc and QS_Testcase present
	- If only GDQ_QS_Detected_AWS_Chime/Chime_SDK not present
	- Label mismatch: Adhoc label and Testcase tag and vise versa 
	- if only  QS_Adhoc or QS_Testcase Label is missing
- If sim is in resolved state 
	- Both valid and invalid label is present
	- No QS_Detected_Valid/Invalid label/ SKIP_AUDIT and Resolution not present 
	- No QS_Detected_Valid/Invalid label/ SKIP_AUDIT label
	- Only resolution not present 
	- Label misses: GDQ and QS_Adhoc/QS_Testcase or SKIP_AUDIT label
	- Both QS_Adhoc and QS_Testcase present
	- If only GDQ_QS_Detected_AWS_Chime/Chime_SDK not present
	- Label mismatch: Adhoc label and Testcase tag and vise versa 
	- if only  QS_Adhoc or QS_Testcase Label is missing
The script will check these items and store the sim in array when any of the following miss takes place 

**API**
The Misses are then sent through API to the chatroom to post by @mentioning the user along with sim and what is missed. 

**Valid deviation / Non valid deviation**
Since devolopers and QA resolve the bugs, time limit is set for resolved bug actioning. Hence when a bug is resolved within 24 hours will be displayed under non deviation. If its monday the time period is checked as resolved within 72 hours. Other misses will be displayed under Deviation. 

**File detetion**
After the script is runned succesfully the dump file which was downloaded gets deleted.

**Scheduler**
The script can be runned automatically at fixed time by using windows task scheuler or Mac automation application. 
