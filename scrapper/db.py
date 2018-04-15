import config as settings
from pymongo import MongoClient


def connect():
    client = MongoClient(settings.HOST, int(settings.PORT))
    db = client[settings.DB_NAME]
    return db


def insert_queries(queries):

    db = connect()
    collection = db[settings.COL_QUERIES]

    if len(queries) > 0:
        collection.insert_many(queries)


def insert_rows(for_task, rows):

    db = connect()

    if for_task == settings.TASKS[0]:
        collection = db[settings.COL_JOBS]
    else:
        collection = db[settings.COL_RESUMES]

    if len(rows) > 0:
        collection.insert_many(rows)


def update_queries(for_task, key, values):

    db = connect()
    collection = db[settings.COL_QUERIES]
    query = {
        settings.UPDATE_KEY: key
    }
    if for_task == settings.TASKS[0]:
        set_value = {
            settings.QUERIES_COLUMNS['job_status']: values['status']
        }
    else:
        set_value = {
            settings.QUERIES_COLUMNS['resume_status']: values['status']
        }
    collection.update_one(query, {'$set': set_value}, upsert=False)


def update_job_scrap(key, values, add=False):

    db = connect()
    collection = db[settings.COL_JOBS]
    query = {
        settings.UPDATE_KEY: key
    }
    set_value = {
        settings.JOBS_COLUMNS['scrap']: values['status']
    }
    if add:
        set_value[settings.JOBS_COLUMNS['html_content']] = values['content']
    collection.update_one(query, {'$set': set_value}, upsert=False)


def update_job_parse(key, values, add=False):

    db = connect()
    collection = db[settings.COL_JOBS]
    query = {
        settings.UPDATE_KEY: key
    }
    set_value = {
        settings.JOBS_COLUMNS['parse']: values['status']
    }
    if add:
        set_value[settings.JOBS_COLUMNS['parsed_content']] = values['content']
    collection.update_one(query, {'$set': set_value}, upsert=False)


def update_resume_scrap(key, values, add=False):

    db = connect()
    collection = db[settings.COL_RESUMES]
    query = {
        settings.UPDATE_KEY: key
    }
    set_value = {
        settings.RESUMES_COLUMNS['scrap']: values['status']
    }
    if add:
        set_value[settings.RESUMES_COLUMNS['html_content']] = values['content']
    collection.update_one(query, {'$set': set_value}, upsert=False)


def update_resume_parse(key, values, add=False):

    db = connect()
    collection = db[settings.COL_RESUMES]
    query = {
        settings.UPDATE_KEY: key
    }
    set_value = {
        settings.RESUMES_COLUMNS['parse']: values['status']
    }
    if add:
        set_value[settings.RESUMES_COLUMNS['parsed_content']] = values['content']
    collection.update_one(query, {'$set': set_value}, upsert=False)


def fetch_rows(query_for, status_for):

    collection = None
    mongo_query = None

    db = connect()
    queries = []  # Result Set


    if query_for == 'resume_scrap':  # For resumes links with extraction status

        collection = db[settings.COL_RESUMES]

        if status_for == 'pending':
            mongo_query = {settings.RESUMES_COLUMNS['scrap']: settings.HTML_EXTRACTION_PENDING}
        elif status_for == 'done':
            mongo_query = {settings.RESUMES_COLUMNS['scrap']: settings.HTML_EXTRACTION_DONE}
        elif status_for == 'error':
            mongo_query = {settings.RESUMES_COLUMNS['scrap']: settings.HTML_EXTRACTION_ERROR}

    elif query_for == 'job_scrap':  # For jobs links with extraction status

        collection = db[settings.COL_JOBS]

        if status_for == 'pending':
            mongo_query = {settings.JOBS_COLUMNS['scrap']: settings.HTML_EXTRACTION_PENDING}
        elif status_for == 'done':
            mongo_query = {settings.JOBS_COLUMNS['scrap']: settings.HTML_EXTRACTION_DONE}
        elif status_for == 'error':
            mongo_query = {settings.JOBS_COLUMNS['scrap']: settings.HTML_EXTRACTION_ERROR}

    elif query_for == 'resume_parse':  # For resumes html with parse status

        collection = db[settings.COL_RESUMES]

        if status_for == 'pending':
            mongo_query = {settings.RESUMES_COLUMNS['parse']: settings.HTML_PARSING_PENDING}
        elif status_for == 'done':
            mongo_query = {settings.RESUMES_COLUMNS['parse']: settings.HTML_PARSING_DONE}
        elif status_for == 'error':
            mongo_query = {settings.RESUMES_COLUMNS['parse']: settings.HTML_PARSING_ERROR}

    elif query_for == 'job_parse':  # For jobs html with parse status

        collection = db[settings.COL_JOBS]

        if status_for == 'pending':
            mongo_query = {settings.JOBS_COLUMNS['parse']: settings.HTML_PARSING_PENDING}
        elif status_for == 'done':
            mongo_query = {settings.JOBS_COLUMNS['parse']: settings.HTML_PARSING_DONE}
        elif status_for == 'error':
            mongo_query = {settings.JOBS_COLUMNS['parse']: settings.HTML_PARSING_ERROR}

    elif query_for == 'job_queries':

        collection = db[settings.COL_QUERIES]

        if status_for == 'pending':
            mongo_query = {settings.QUERIES_COLUMNS['job_status']: settings.LINK_EXTRACTION_PENDING}
        elif status_for == 'done':
            mongo_query = {settings.QUERIES_COLUMNS['job_status']: settings.LINK_EXTRACTION_DONE}
        elif status_for == 'error':
            mongo_query = {settings.QUERIES_COLUMNS['job_status']: settings.LINK_EXTRACTION_ERROR}

    elif query_for == 'resume_queries':

        collection = db[settings.COL_QUERIES]

        if status_for == 'pending':
            mongo_query = {settings.QUERIES_COLUMNS['resume_status']: settings.LINK_EXTRACTION_PENDING}
        elif status_for == 'done':
            mongo_query = {settings.QUERIES_COLUMNS['resume_status']: settings.LINK_EXTRACTION_DONE}
        elif status_for == 'error':
            mongo_query = {settings.QUERIES_COLUMNS['resume_status']: settings.LINK_EXTRACTION_ERROR}

    cur = collection.find(mongo_query)
    for doc in cur:
        queries.append(doc)

    return queries, len(queries)

def fetch_count(query_for, status_for):

    collection = None
    mongo_query = None

    db = connect()

    if query_for == 'resume_scrap':  # For resumes links with extraction status

        collection = db[settings.COL_RESUMES]

        if status_for == 'pending':
            mongo_query = {settings.RESUMES_COLUMNS['scrap']: settings.HTML_EXTRACTION_PENDING}
        elif status_for == 'done':
            mongo_query = {settings.RESUMES_COLUMNS['scrap']: settings.HTML_EXTRACTION_DONE}
        elif status_for == 'error':
            mongo_query = {settings.RESUMES_COLUMNS['scrap']: settings.HTML_EXTRACTION_ERROR}

    elif query_for == 'job_scrap':  # For jobs links with extraction status

        collection = db[settings.COL_JOBS]

        if status_for == 'pending':
            mongo_query = {settings.JOBS_COLUMNS['scrap']: settings.HTML_EXTRACTION_PENDING}
        elif status_for == 'done':
            mongo_query = {settings.JOBS_COLUMNS['scrap']: settings.HTML_EXTRACTION_DONE}
        elif status_for == 'error':
            mongo_query = {settings.JOBS_COLUMNS['scrap']: settings.HTML_EXTRACTION_ERROR}

    elif query_for == 'resume_parse':  # For resumes html with parse status

        collection = db[settings.COL_RESUMES]

        if status_for == 'pending':
            mongo_query = {settings.RESUMES_COLUMNS['parse']: settings.HTML_PARSING_PENDING}
        elif status_for == 'done':
            mongo_query = {settings.RESUMES_COLUMNS['parse']: settings.HTML_PARSING_DONE}
        elif status_for == 'error':
            mongo_query = {settings.RESUMES_COLUMNS['parse']: settings.HTML_PARSING_ERROR}

    elif query_for == 'job_parse':  # For jobs html with parse status

        collection = db[settings.COL_JOBS]

        if status_for == 'pending':
            mongo_query = {settings.JOBS_COLUMNS['parse']: settings.HTML_PARSING_PENDING}
        elif status_for == 'done':
            mongo_query = {settings.JOBS_COLUMNS['parse']: settings.HTML_PARSING_DONE}
        elif status_for == 'error':
            mongo_query = {settings.JOBS_COLUMNS['parse']: settings.HTML_PARSING_ERROR}

    elif query_for == 'job_queries':

        collection = db[settings.COL_QUERIES]

        if status_for == 'pending':
            mongo_query = {settings.QUERIES_COLUMNS['job_status']: settings.LINK_EXTRACTION_PENDING}
        elif status_for == 'done':
            mongo_query = {settings.QUERIES_COLUMNS['job_status']: settings.LINK_EXTRACTION_DONE}
        elif status_for == 'error':
            mongo_query = {settings.QUERIES_COLUMNS['job_status']: settings.LINK_EXTRACTION_ERROR}

    elif query_for == 'resume_queries':

        collection = db[settings.COL_QUERIES]

        if status_for == 'pending':
            mongo_query = {settings.QUERIES_COLUMNS['resume_status']: settings.LINK_EXTRACTION_PENDING}
        elif status_for == 'done':
            mongo_query = {settings.QUERIES_COLUMNS['resume_status']: settings.LINK_EXTRACTION_DONE}
        elif status_for == 'error':
            mongo_query = {settings.QUERIES_COLUMNS['resume_status']: settings.LINK_EXTRACTION_ERROR}

    count = collection.count(mongo_query)

    return count

