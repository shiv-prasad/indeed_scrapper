import config as settings
import query_builder
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import db
from multiprocessing import Process
import browser

headers = {'User-Agent': UserAgent().chrome}


def get_soup(url, driver=None, for_task=None):

    if driver:
        if for_task == settings.TASKS[1]:
            id_name = 'resume_body'
        else:
            id_name = 'job-content'
        browser.wait_till(driver, 'id', id_name)
        page = driver.page_source
    else:
        page = requests.get(url, headers=headers).text
    return BeautifulSoup(page, 'html.parser')


def fetch_pool_results(for_task, queries, driver=None):

    if driver:

        query_chunks = [queries[i:i + settings.MAX_TABS] for i in xrange(0, len(queries), settings.MAX_TABS)]

        for each_chunk in query_chunks:

            main_window = browser.get_main_window(driver)
            start_indexes = each_chunk

            for j in range(len(each_chunk)):

                if for_task == settings.TASKS[0]:
                    new_url = query_builder.fetch_job_url(start_indexes[j]['url'])
                    name = "table"
                    attrs = {'id': 'job-content'}
                else:
                    new_url = query_builder.fetch_resume_url(start_indexes[j]['url'])
                    name = "div"
                    attrs = {'id': 'resume_body'}

                browser.execute_javascript(driver, 'window.open("{url}","_blank");'.format(url=new_url))

            for j in range(len(browser.get_window_handles(driver))):

                each_window = browser.get_window_handles(driver)[j]

                if each_window != main_window:
                    browser.switch_to_window(driver, each_window)

                    try:

                        content = str(get_soup(new_url, driver=driver, for_task=for_task).find(name=name, attrs=attrs))
                        db.update_scrap(for_task, start_indexes[j]['key'], {'status': settings.HTML_EXTRACTION_DONE, 'content': content}, add=True)
                        print "# Done!"

                    except Exception as e:

                        db.update_scrap(for_task, start_indexes[j]['key'], {'status': settings.HTML_EXTRACTION_ERROR})
                        print "# Error: {error}".format(error=str(e))

            while len(browser.get_window_handles(driver)) != 1:
                browser.switch_to_window(driver, browser.get_window_handles(driver)[0])
                browser.close_tab(driver)

            browser.switch_to_window(browser.get_window_handles(driver)[0])

    else:

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

        if settings.WEBDRIVER_REQUIRED:
            driver = browser.get_browser()
            processes = [Process(target=fetch_pool_results, args=(for_task, each_chunk, driver,)) for each_chunk in queries_chunks]
        else:
            processes = [Process(target=fetch_pool_results, args=(for_task, each_chunk,)) for each_chunk in queries_chunks]

        for process in processes:
            process.start()
        for process in processes:
            process.join()

        if settings.WEBDRIVER_REQUIRED:
            browser.close_browser(driver)
    else:
        if settings.WEBDRIVER_REQUIRED:
            driver = browser.get_browser()
            fetch_pool_results(for_task, filtered_queries, driver)
            browser.close_browser(driver)
        else:
            fetch_pool_results(for_task, filtered_queries)
