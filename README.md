# n-wave
## Installation Instructions: ##
1. Clone project "n-wave": ```https://github.com/eratterman/n-wave```
2. Create python 3 virtual environment outside of project directory
3. Navigate to Scripts directory inside the virtual environment and activate virtual environment.
4. Install python modules from requirements.txt file in project: ```pip install -r requirements.txt```
5. Navigate here: n-wave/nwave and run command: ```python manage.py migrate```
6. Run: ```python manage.py makemigrations "api"```
7. Run: ```python manage.py migrate```
8. Optional step to log into admin site and view data in models: run: ```python manage.py createsuperuser``` - follow prompts
9. Run: ```python manage.py runserver```

## Site Instructions: ##
1. In the browser, log into: ```http://localhost:8000/```
   * this displays two simple api calls to view asset and column data - it should currently be empty

2. Navigate to: http://localhost:8000/import and click Import Files button.
3. Click Choose Files
4. Navigate to the directory where the csv files are stored
5. Select all files and click Open
6. Click the Import Files on the pop up dialog box.
> **NOTE:** This step currently takes around 2 min   
> The import of data into pandas is quick, but it's also loading data into the models  
7. When import completes, you will see some links on the page
> To API Root  
> Plot Data  

8. Click Plot Data link
9. Click Plot Data button and select the Asset, Column, Beginning Date, and Ending Dates from the select lists.
10. Click Plot Selections
  * **NOTE:** The graph is interactive meaning you can select a period of data to zoom in.  Double click to zoom out again.
11) Click Plot Data button again to plot another dataset.
