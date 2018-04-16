import config as settings
import query_builder
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import db
from multiprocessing import Process

headers = {'User-Agent': UserAgent().chrome}


def get_soup(url):

    page = requests.get(url, headers=headers)
    return BeautifulSoup(page.text, 'html.parser')


def fetch_pool_results(for_task, queries):

    for each_query in queries:
        try:
            if for_task == settings.TASKS[0]:
                url = query_builder.fetch_job_url(each_query['url'])
                name = "table"
                attrs = {'id': 'job-content'}
            else:
                url = query_builder.fetch_resume_url(each_query['url'])
                name = "div"
                attrs = {'id': 'resume_body'}

            print "# URL: {url}".format(url=url)
            content = str(get_soup(url).find(name=name, attrs=attrs))
            db.update_scrap(for_task, each_query['key'], {'status': settings.HTML_EXTRACTION_DONE, 'content': content}, add=True)
            print "# Done!"

        except Exception as e:

            db.update_scrap(for_task, each_query['key'], {'status': settings.HTML_EXTRACTION_ERROR})
            print "# Error: {error}".format(error=str(e))


def fetch_html(for_task, queries):

    if for_task == settings.TASKS[0]:
        columns = settings.JOBS_COLUMNS
    else:
        columns = settings.RESUMES_COLUMNS

    filtered_queries = list(map(lambda query: {
        'url': query[columns['link']],
        'key': query[settings.UPDATE_KEY]
    }, queries))

    if settings.MULTIPROCESS_REQUIRED:
        partition = int(len(filtered_queries) / settings.NO_OF_PROCESSES)
        if partition == 0:
            partition += 1
        queries_chunks = [filtered_queries[i:i + partition] for i in xrange(0, len(filtered_queries), partition)]
        processes = [Process(target=fetch_pool_results, args=(for_task, each_chunk,)) for each_chunk in queries_chunks]
        for process in processes:
            process.start()
        for process in processes:
            process.join()
    else:
        fetch_pool_results(for_task, filtered_queries)