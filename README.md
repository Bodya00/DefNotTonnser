# DefNotTonnser
Recruitment task for Tonnser

File notes/SQL_task.md contains solution to task 1(SQL) and description of implementation process. 
All the other files are connected with task 2(Scraper).
This file contains description of implemented solution for task 2.
File notes/Scraper_task.md contains description of implementation process for task 2. 
## Setting up
### Any system
To properly set up project environment you need to:
  - Install Python 3.7.3 as a separate Python virtual environment
  - Activate virtual environment
  - Install requirements.txt (pip3 install -r requirements.txt)
  - Run tests to check if everything is set up correctly ("pytest tests.py" while being in root of project directory)
Script runs standard Python way. File that contains solution is called "scraper.py"
### Linux
If you are using Linux you can use "make" script: (although you need your virtual environment to have name "venv" and be in root of project directory)
  - Use "make install" to install requirements
  - Use "make test" to run tests
  - Use "make run" to run script
 
## Configuration
By default script:
  1. Scrapes [Tesla](https://en.wikipedia.org/wiki/Tesla,_Inc.) company page.
  2. Finds and extracts parameters **operating income**, **revenue**, **net income**, **total assets**, **total equity** in the summary table.
  3. Converts those parameters from USD to DKK.
  4. Outputs those parameters to standard output.
  
By modifying file config.py you can change:
  1. Company to scrape
      * URL must lead to article on Wikipedia page
      * Page must contain summary table
  2. Parameters to scrape 
      * Summary table must contain parameters from config.py ('params_to_extract' variable)
      * Parameters must be financial and described using USD('US$')
      * Multiplicators variable from config.py must contain all the multiplicators contained in string describing parameter
  3. Currency to convert to
      * Currency must ust be a valid floating point value or integer
