import config as settings
import query_builder
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import db
import pagination
from multiprocessing import Process

headers = {'User-Agent': UserAgent().chrome}


def get_soup(url):

    page = requests.get(url, headers=headers)
    return BeautifulSoup(page.text, 'html.parser')


def get_links_from_page(for_task, url):

    soup = get_soup(url)

    if for_task == settings.TASKS[1]:
        name = 'a'
        attrs = {'class': 'app_link'}
        columns = settings.RESUMES_COLUMNS

    else:
        name = 'a'
        attrs = {'class': 'turnstileLink'}
        columns = settings.JOBS_COLUMNS

    results = []
    for link in soup.find_all(name=name, attrs=attrs):
        results.append({
            columns['link']: link['href'],
            columns['scrap']: settings.HTML_EXTRACTION_PENDING
        })

    return results


def fetch_pool_results(for_task, queries, starts):

    final_results = []

    for page_count in starts:

        if for_task == settings.TASKS[1]:
            url = query_builder.fetch_resume_link_url(queries, page_count)
        else:
            url = query_builder.fetch_job_link_url(queries, page_count)

        results = get_links_from_page(for_task, url)
        final_results.extend(results)

        print "# Results for Page {page_count}: {total}".format(page_count=page_count, total=len(results))

    db.insert_rows(for_task, final_results)


def fetch_links(for_task, queries):

    filtered_queries = list(map(lambda query: {
        'queries': query['queries'],
        'key': query['_id']
    }, queries))

    for each_query in filtered_queries:

        try:

            print
            print "# Query {query}".format(query=each_query['queries'])

            if for_task == settings.TASKS[0]:
                url = query_builder.fetch_job_link_url(each_query['queries'], 0)
            else:
                url = query_builder.fetch_resume_link_url(each_query['queries'], 0)
            print "# Url: {url}".format(url=url)

            total_results = 0
            result_present = False

            soup = get_soup(url)

            if for_task == settings.TASKS[0]:
                result_divs = soup.find_all(name="div", attrs={"id": "searchCount"})
            else:
                result_divs = soup.find_all(name="div", attrs={"id": "result_count"})

            for res_div in result_divs:

                result_present = True

                if for_task == settings.TASKS[0]:
                    total_results = int(res_div.text.strip().split('of')[1].strip().replace(',', ''))
                else:
                    total_results = int(res_div.text.strip().split(' ')[0].strip().replace(',', ''))

            if result_present:

                print "# Result Present: <True>"
                print "# Total Results: <{total}>".format(total=total_results)

                starts = pagination.make_start_list(for_task, total_results)

                if settings.MULTIPROCESS_REQUIRED:
                    partition = int(len(starts)/settings.NO_OF_PROCESSES)
                    if partition == 0:
                        partition += 1
                    start_chunks = [starts[i:i + partition] for i in xrange(0, len(starts), partition)]
                    processes = [Process(target=fetch_pool_results, args=(for_task, each_query['queries'], each_chunk, )) for each_chunk in start_chunks]
                    for process in processes:
                        process.start()
                    for process in processes:
                        process.join()
                else:
                    fetch_pool_results(for_task, each_query['queries'], starts)

            else:

                print "# Result Present: <False>"

            db.update_queries(for_task, each_query['key'], {'status': settings.LINK_EXTRACTION_DONE})

        except Exception as e:

            db.update_queries(for_task, each_query['key'], {'status': settings.LINK_EXTRACTION_ERROR})
            print "# Error: {error}".format(error=str(e))