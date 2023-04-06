Label Audit Script - Self Service Set Up 

1. How to set up your device ?

1. Download the latest version of Python
2. Install python in your device by clicking the python file from the download folder
    1.  Windows 
        1. Check mark Add python to Path
        2. Click Customize installation
        3. Make sure PIP is checked  and click next and install
        4. 
    2. OSX 
        1. Click next in the tabs and click install 
3. Open the command prompt or terminal 
    1. Windows (Command prompt) In keyboard press windows + R button and type cmd and enter
    2. OSX (Terminal) In keyboard press command + space bar 
4. Installation of packages
    1. In windows command prompt enter the below comments one by one 
        1. python -V
        2. pip install pandas
        3. pip install requests
        4. pip install selenium
        5. pip install webdriver_manager
    2. In OSX terminal run the following commands
        1. python3 --version (to check version)
        2. pip3 install pandas
        3. pip3 install requests
        4. pip3 install selenium
        5. pip3 install webdriver_manager

2. How to get URL of Web hook ?

1. Admin of the chatroom to click on the more button
2. Select Manage webhook and bots 
3. Click Add Webhook
4. Give a name and click create
5. In ‘Manage incoming webhooks and bots’ click on the Copy URL 

3. Export result categorising in SIM/ TCORP 

1. Go to SIM/ TCORP. Filter the bugs according to your team. For example, refer Chime team filter. 
2. Now click on export button and select Export Search Results and add the following columns
    1. SIM
        1. IssueUrl
        2. Title 
        3. RequesterIdentity 
        4. CreateDate 
        5. Status 
        6. Labels 
        7. Severity 
        8. PriorityLevel 
        9. Tags 
        10. RootCauses 
        11. Resolution (string) 
        12. AssignedFolderLabel
        13. Last Resolved Date 
        14. 
    2. TCorp
        1. Enable the following while downloading the dump
            1. IssueId 
            2. IssueUrl 
            3. ShortId 
            4. Title 
            5. AssignedGroup
            6. ClosureCode 
            7. CreateDate 
            8. Labels 
            9. PriorityLevel 
            10. RequesterIdentity
            11. ResolvedDate 
            12. RootCause 
            13. Severity 
            14. Status 
            15. Tags
3. Select CSV format 
4. Select Save change so that the selected columns gets saved (When the script downloads the dump all mentioned columns will be present)

4. What to be changed in the Script?

1. GDQ labels to be changed according to your team name - GDQ_QS_Detected_XXXX throughout the code control R (Replace) the current team label to yours
2. URL of your chatroom webhook in the line 17 (Refer 2. How to get URL of Web hook ?)
    1. Open the file in IDLE and change the URL within  '' (Highlighted in green)
3. SIM/ Tcorp filter URL in line 50 and 74
4. To select the downloaded file (We need to set a path to downloads folder)
    1. Go to line 95 →  Set the path to your downloads folder

5. How to create bat file?

To schedule the script to run at a particular time automatically, we need a bat file,

* Open a notepad 
* Paste the following code in the notepad (edit the path according to script location - Line 2)
    * @echo off
        cd "C:\Users\fdivyar\Desktop\python" 
        python Qdesklabelaudit.py"
        pause
* Save the file as name.bat to save notepad as bat file

6. How to run midway bypass (Run every day)

1. Open command prompt 
2. Pass the command mwinit
3. Once username is displayed type the password and press zuckey 
4. Prompt will appear for zuckey, press zuckey again
5. Make sure ‘Successfully authenticated’ message is displayed

7. How to run the script manually  ?

1. To Run the script

    1. In Windows 
        1. Open the script file located folder. Click on the path and type cmd and enter 
        2. In the command prompt, run the command python filename.py
    2. In OSX 
        1. In the terminal, redirect to the folder where script file is located using cd comment
        2. now run the command python3 filename.py
    3. Both (Windows and OSX)
        1. Open the script file with python launcher and click run
1. We will get the response with total bugs audited with message id and room id

8. How to schedule the script to run (Recommended )?

a. In windows, we can use windows task scheduler 

* Open the task scheduler as admin (Enable admin access in ACME)
* Click on action and click create basic task
* Give a name and give next
* In trigger, click weekly and next 
* Give a start date, time.
* Set recur every 1 week on Monday to Friday and click next
* Select start a program 
*  In program/script, click browse and select the bat file
* Create and preview the task. 
* In General tab, make sure Run with highest privileges is check marked
* In Conditions only Wake the computer to run this task should be check marked 
* In setting tab, Check mark allow task to be run on demand, Run as soon as possible after scheduled start is missed
* Click OK to save the changes 




