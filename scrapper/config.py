## Run for
FOR_RESUME = False
FOR_JOB = False
TASKS = ["jobs", "resumes"]


## Login
LOGIN_REQUIRED = False
LOGIN_URL = "indeed login page URL"
LOGIN_DETAILS = []  # List of login credentials eg [{'username': 'someone@example.com', 'password': 'password'} ... ]


## Webdriver
WEBDRIVER_REQUIRED = False
WEBDRIVER_EXECUTABLE_PATH = "path to executable webdriver"
MAX_TABS = 10


## Multiprocessing
MULTIPROCESS_REQUIRED = False
MULTIPROCESS_TYPE = ""  # sequential | shared
NO_OF_PROCESSES = 10


## Base urls
JOB_BASE_URL = "url path to job result page"  # eg: "https://www.indeed.co.in/jobs"
RESUME_BASE_URL = "url path to resume result page"  # eg: "https://www.indeed.com/resumes"
JOB_HTML_BASE_URL = "url path to job page"  # eg: "https://www.indeed.co.in"
RESUME_HTML_BASE_URL = "url path to resume page"  # eg: "http://www.indeed.com"


## Queries Files
JOB_QUERIES_INPUT_CSV_PATH = "path to csv containing job related queries"
JOB_QUERIES_COLUMNS = []  # ["q","l"]
RESUME_QUERIES_INPUT_CSV_PATH = "path to csv containing resume related queries"
RESUME_QUERIES_COLUMNS = []  # ["q","l"]


## Database Settings
# Basic
HOST = ""
PORT = ""
DB_NAME = ""
COL_QUERIES = ""
COL_JOBS = ""
COL_RESUMES = ""
QUERIES_COLUMNS = {
    "queries": "queries",
    "job_status": "job_status",
    "resume_status": "resume_status"
}
RESUMES_COLUMNS = {
    "link": "url",
    "scrap": "scrap_status",
    "html_content": "html",
    "parse": "parse_status",
    "parsed_content": "content"
}
JOBS_COLUMNS = {
    "link": "url",
    "scrap": "scrap_status",
    "html_content": "html",
    "parse": "parse_status",
    "parsed_content": "content"
}
UPDATE_KEY = '_id'

# Status in models
LINK_EXTRACTION_PENDING = "0"
LINK_EXTRACTION_ERROR = "1"
LINK_EXTRACTION_DONE = "2"
HTML_EXTRACTION_PENDING = "0"
HTML_EXTRACTION_ERROR = "1"
HTML_EXTRACTION_DONE = "2"
HTML_PARSING_PENDING = "0"
HTML_PARSING_ERROR = "1"
HTML_PARSING_DONE = "2"


## Results
# Result per page
MAX_RESULTS_PER_JOB_PAGE = 10
MAX_RESULTS_PER_RESUME_PAGE = 50

# Pagination
MAX_PAGINATION_JOBS = 100

if LOGIN_REQUIRED:
    MAX_PAGINATION_RESUMES = 100
else:
    MAX_PAGINATION_RESUMES = 20

# Total results
MAX_RESULTS_FOR_JOB = (MAX_PAGINATION_JOBS * MAX_RESULTS_PER_JOB_PAGE)
MAX_RESULTS_FOR_RESUME = (MAX_PAGINATION_RESUMES * MAX_RESULTS_PER_RESUME_PAGE)


#################################################################
#                   Local Settings (if exists)                  #
#################################################################
try:
    from local_config import *
except:
   pass
