# Python-ETL-certPdfScrapper
Created on Jun 13, 2020

### By Johany A. Carmona C.
GitHub: https://github.com/JohanyCarmona/
#####
Email: johany.carmona@pm.me; johany.carmona@tuta.io; johany.carmona@udea.edu.co

### About: Legal Tradition Certificate PDF Scrapper
Info: Extract Main Data from a PDF file, then transform it to Data Object and finally load it to a JSON file.

### Help: Execute from terminal using the following command.
Command: python3 cert.py [fileName]
#####
TIPs: fileName must be in *.pdf format.
#####
If you want execute the script more restrictively, then use #Particular case comment lines to prevent invalid file extraction.
#####
Warning: Script haven't been tested over production environment.

### Third Party Dependencies: 
pdfplumber Third Party Library
#####
GitHub: https://github.com/jsvine/pdfplumber
#####
Installation: pip install pdfplumber
### Virtual Environment: 
VEnv Installation: ./environment.sh 
#####
VEnv Execution: ./environment/bin/python3 cert.py [fileName]


### Windows:
Generate Virtual Environment
#####
On Windows, invoke the venv command as follows:
#####
c:\>c:\Python35\python3 -m venv --p python3 c:\<path>\environment
#####
Alternatively, if you configured the PATH and PATHEXT variables for your Python installation, use:
#####
c:\>python3 -m venv --p python3 c:\<path>\environment
#####
Enable Virtual Environment on Windows PowerShell
#####
PS C:\> <path>\environment\bin\Activate.ps1
#####
Install requirements
#####
c:\> python3 -m pip install -r requirements.txt
#####
Disable Virtual Environment
#####
deactivate
#####
To Execute python script, use
#####
c:\> <path>\environment\bin\python3 <path>\cert.py [fileName]
#####
Where: [path] = C:\Users\'Username'
