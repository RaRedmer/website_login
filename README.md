# Automated Scraping for Ecampus Overview
This repository contains the script for downloading all course contents
from the Ecampus overview. 


## Function
 Go through each element in the courses from Ecampus from the overview and download it, given that it 
 is a file. 
 The directory structure from ecampus will be adopted regarding the saving of the files on your 
 computer. 
 
 
## Usage
- **Config Specification:** Replace your_user_name and your_password from the config file by your actual username 
and password: <p align="center"><img src="https://i.imgur.com/IEiHJTa.png"></p> 
 
- **Execution**: Just run script "ecampus_overview_scraping.py" 


## Process Illustration 
Assume that below is your overview as specified in the file "links.ini": <p align="center"><img src="https://i.imgur.com/LT4KJ5I.png"></p>

1. Go into the finance folder: <p align="center"><img src="https://i.imgur.com/MXeSq8K.png"></p> 
 
2. Download all files from it: <p align="center"><img src="https://i.imgur.com/lrK60DZ.png"></p>

3. Go back into the previous directory "Finance" and start to check folder "Papers" 
for more files and folders

4. Repeat until all files got downloaded and start the process all over again 
for the next course "Mathematics" from the overview