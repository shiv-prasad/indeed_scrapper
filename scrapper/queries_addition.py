import config as settings
import csv
import codecs
import db as database_methods


def make_job_queries():

    queries = []
    keys = settings.JOB_QUERIES_COLUMNS

    csvReader = csv.reader(codecs.open(settings.JOB_QUERIES_INPUT_CSV_PATH, 'rU', 'utf-16'))
    for row in csvReader:

        query = {}

        for i in range(len(keys)):
            query[keys[i]] = row[i]

        queries.append({
            settings.QUERIES_COLUMNS['queries']: query,
            settings.QUERIES_COLUMNS['job_status']: settings.LINK_EXTRACTION_PENDING
        })

    database_methods.insert_queries(queries)


def make_resume_queries():

    queries = []
    keys = settings.RESUME_QUERIES_COLUMNS

    csvReader = csv.reader(codecs.open(settings.RESUME_QUERIES_INPUT_CSV_PATH, 'rU', 'utf-16'))
    for row in csvReader:

        query = {}

        for i in range(len(keys)):
            query[keys[i]] = row[i]

        queries.append({
            settings.QUERIES_COLUMNS['queries']: query,
            settings.QUERIES_COLUMNS['resume_status']: settings.LINK_EXTRACTION_PENDING
        })

    database_methods.insert_queries(queries)


if __name__ == '__main__':

    if settings.FOR_JOB:
        make_job_queries()

    if settings.FOR_RESUME:
        make_resume_queries()