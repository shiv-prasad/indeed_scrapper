## Run for
FOR_RESUME = False
FOR_JOB = False

## Login
LOGIN_REQUIRED = False
LOGIN_URL = ""
LOGIN_USERNAME = ""
LOGIN_PASSWORD = ""

## Webdriver
WEBDRIVER_EXECUTABLE_PATH = ""

## Base urls
JOB_BASE_URL = ""
RESUME_BASE_URL = ""

## Database Settings
# Basic
HOST = ""
PORT = ""
DB_NAME = ""
COL_QUERIES = ""
COL_JOBS = ""
COL_RESUMES = ""
QUERIES_COLUMNS = {
    "query": "query",
    "location": "location",
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
if LOGIN_REQUIRED:
    MAX_PAGINATION = 100
else:
    MAX_PAGINATION = 20
# Total results
MAX_RESULTS_FOR_JOB = (MAX_PAGINATION * MAX_RESULTS_PER_JOB_PAGE)
MAX_RESULTS_FOR_RESUME = (MAX_PAGINATION * MAX_RESULTS_PER_RESUME_PAGE)


