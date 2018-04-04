## Webdriver
WEBDRIVER_EXECUTABLE_PATH = ""

## Login
LOGIN_REQUIRED = False
LOGIN_URL = ""
USERNAME = ""
PASSWORD = ""

## Base urls
JOB_BASE_URL = ""
RESUME_BASE_URL = ""

## Results
# Pagination
MAX_PAGINATION_WITHOUT_LOGIN = 20
MAX_PAGINATION_WITH_LOGIN = 100
# Result per page
MAX_RESULTS_PER_JOB_PAGE = 10
MAX_RESULTS_PER_RESUME_PAGE = 50
# Total results
MAX_RESULTS_FOR_JOB_IN_LOGIN_STATE = (MAX_PAGINATION_WITH_LOGIN * MAX_RESULTS_PER_JOB_PAGE)
MAX_RESULTS_FOR_RESUME_IN_LOGIN_STATE = (MAX_PAGINATION_WITH_LOGIN * MAX_RESULTS_PER_RESUME_PAGE)
MAX_RESULTS_FOR_JOB_OUTSIDE_LOGIN_STATE = (MAX_PAGINATION_WITHOUT_LOGIN * MAX_RESULTS_PER_JOB_PAGE)
MAX_RESULTS_FOR_RESUME_OUTSIDE_LOGIN_STATE = (MAX_PAGINATION_WITHOUT_LOGIN * MAX_RESULTS_PER_RESUME_PAGE)

## Database Settings
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

## STATUSES
LINK_EXTRACTION_PENDING = "0"
LINK_EXTRACTION_ERROR = "1"
LINK_EXTRACTION_DONE = "2"
HTML_EXTRACTION_PENDING = "0"
HTML_EXTRACTION_ERROR = "1"
HTML_EXTRACTION_DONE = "2"
HTML_PARSING_PENDING = "0"
HTML_PARSING_ERROR = "1"
HTML_PARSING_DONE = "2"
