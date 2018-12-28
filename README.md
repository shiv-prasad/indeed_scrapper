# Indeed Scrapper

Scrapper and Parser for Indeed Jobs and Resumes using Python, BeautifulSoup and Selenium/Requests and storing and manipulating data using mongodb

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* [Python 2.7](https://www.python.org/downloads/)
* [Virtualenv](https://virtualenv.pypa.io/en/stable/)
* [MongoDb](https://docs.mongodb.com/)

### Setup the project

* Clone the [Repository](https://github.com/shiv-prasad/indeed_scrapper) 
```
$ git clone https://github.com/shiv-param/indeed_scrapper
```

* Create your virtual environment
```
$ virtualenv venv
$ source venv/bin/activate
```

* Go to the `scrapper/` directory
```
$ cd scrapper
```

* Install all the libraries required
```
$ pip install -r requirements.txt
```

* If you are going to use **Selenium** for scrapping (Recommended for Resumes), you need to download either of [Chrome](http://chromedriver.chromium.org/), [Firefox](https://developer.mozilla.org/en-US/docs/Web/WebDriver) or [PhantomJS](http://phantomjs.org/release-1.8.html) Webdrivers and save them into `tools/` directory and add their path to your Environemnt's `PATH` variable.

* Make a file in your `scrapper/` directory named `local_config.py` and add the configuration parameters provided in [config.py](https://github.com/shiv-param/indeed_scrapper/blob/master/scrapper/config.py) to this file. We are going to change these paramters according to the requirements of the problem.

Now we are ready to change the configuration paramters and run the project.

**Note:** Do not push your webdrivers and `local_config.py` to git

## Preparing your QuerySet

If we see the url for a jobs/resumes results page, for example
```
For Jobs: https://www.indeed.co.in/jobs?q=Android&l=Bangalore
For Resumes: https://www.indeed.com/resumes?q=Android&l=Hyderabad%2C+Telangana
```
We will find out that the urls are constructed as following:
```
For Jobs: <job_base_url>?<query1_key>=<query1_value>&<query2_key>=<query2_value>....
For Resumes: <resume_base_url>?<query1_key>=<query1_value>&<query2_key>=<query2_value>....
```
So according to the pattern,
The following paramters of our `local_config.py` file will be set as:
```
JOB_BASE_URL = "https://www.indeed.co.in/jobs"
RESUME_BASE_URL = "https://www.indeed.com/resumes"
JOB_QUERIES_COLUMNS = ["q", "l"]
RESUME_QUERIES_COLUMNS = ["q", "l"]
```
And we will be setting the values for these `query_keys` in a sepeate csv file which we are going to place in our `tools/data/` directory and update the following parameters of our `local_config.py` file:
```
JOB_QUERIES_INPUT_CSV_PATH = "../tools/data/job_queries.csv"
RESUME_QUERIES_INPUT_CSV_PATH = "../tools/data/resume_queries.csv"
```
*Please refer to [queries_template.csv](https://github.com/shiv-param/indeed_scrapper/blob/master/tools/data/queries_template.csv) to know the format of the csv.*

Now we are ready with our **QuerySet** for the project.

**Note:** Do not push your `queries.csv` to git.

## Understanding the Configuration

To select for which scrapping (Jobs or Resumes or both) you are going to run the code, change the following parameters in our `local_config.py`:
```
FOR_RESUME = False
FOR_JOB = False
```

### Webdriver Settings

If you are going to use **Selenium**, change the following parameters in our `local_config.py`:
```
WEBDRIVER_REQUIRED = True
WEBDRIVER_TYPE = "chrome"   # Use 'firefox' and 'phantom' for Firefox and PhantomJS Webdrivers respectively
WEBDRIVER_EXECUTABLE_PATH = "path to your webdriver"
MAX_TABS = 10   #Maximum no of tabs you want to allow the code to open at a time
```

In case if you are scrapping for Resume, we recommend you to use the login feature as number of records are limited to **1000** for resumes in case of **no login** and **5000** in case of **login**. For this, change the following parameters in our `local_config.py`:
```
LOGIN_REQUIRED = True
LOGIN_URL = "https://secure.indeed.com/account/login"
LOGIN_DETAILS = [  ## List of login credentials eg [{'username': 'someone@example.com', 'password': 'password'} ... ]
    {
        'username': 'someone@example.com',
        'password': 'password'
    }
]
```

### Multiprocessing Settings

In case if you want to use Multiprocessing while scrapping and parsing, change the following parameters in our `local_config.py`:
```
MULTIPROCESS_REQUIRED = True
MULTIPROCESS_TYPE = "sequential"  # if you want to run jobs for Job and Resume parallely then 'shared'. Otherwise 'sequential'. By default 'sequential'
NO_OF_PROCESSES = 10
```

### Database Settings

Set up your **mongodb** database. Create your collections for queries, jobs and resumes. Change the following database parameters in our `local_config.py` for database support:
```
HOST = "" # Your DB host
PORT = "" # Your DB port
DB_NAME = "" # Your DB name
COL_QUERIES = "" # Your Queries Collection Name
COL_JOBS = "" # Your Jobs Collection Name
COL_RESUMES = "" # Your Resume Collection Name
```

Now we are ready with our configuration for the project.

## Execution

The basic flow of our codes is:
```
Add Queries to DB -> Run Link Extraction -> Run HTML Extraction -> Run HTML Parser
```

Assuming you have already configured your `local_settings.py` and `queries.csv`,

* To add queries to DB:
```
$ cd scrapper/
$ python queries_addition.py
```

* To run link extraction:
```
$ cd scrapper/
$ python link_extractor.py
```

* To run html extraction:
```
$ cd scrapper/
$ python html_extractor.py
```

* To run html parsing:
```
$ cd scrapper/
$ python html_parser.py
```

**Note:** Run `python status.py` to know the status of your execution process.

## Final Data

Please refer to the sample output data for [Jobs](https://raw.githubusercontent.com/shiv-prasad/indeed_scrapper/master/tools/data/jobs.json) and [Resumes](https://raw.githubusercontent.com/shiv-prasad/indeed_scrapper/master/tools/data/resumes.json) for your reference

## Author

* **Shiv Prasad** - *Initial work* - [shiv-prasad](https://github.com/shiv-prasad/)
