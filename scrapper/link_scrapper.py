import config as settings
import query_builder
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import db
import pagination
from multiprocessing import Process
import browser

headers = {'User-Agent': UserAgent().chrome}


def get_soup(url, driver=None, for_task=None):

    """
    Fetch soup for the webpage opened. if webdriver given then process will be selenium automation otherwise requests

    :param url: url of the webpage
    :param driver: Webdriver instance (optional)
    :param for_task: process for jobs/resumes
    :return: soup for the webpage opened
    """

    if driver:
        if for_task == settings.TASKS[1]:
            class_name = 'app_link'
        else:
            class_name = 'turnstileLink'
        browser.wait_till(driver, 'class', class_name)
        page = driver.page_source
    else:
        page = requests.get(url, headers=headers).text

    return BeautifulSoup(page, 'html.parser')


def get_links_from_page(for_task, url=None, driver=None):

    """
    Get all the links for the url provided

    :param for_task: process for jobs/resumes
    :param url: query url for which links should be fetched
    :param driver: process for jobs/resumes
    :return: all the links found on the webpage
    """

    if driver:
        soup = get_soup(url, driver=driver, for_task=for_task)
    else:
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


def fetch_pool_results(for_task, queries, starts, driver=None):

    """
    Fetch all the links for the list of queries provided

    :param for_task: process for jobs/resumes
    :param queries: list of all the queries
    :param starts: pagination values
    :param driver: Webdriver instance (optional)
    :return:
    """

    final_results = []

    if driver:

        start_chunks = [starts[i:i + settings.MAX_TABS] for i in xrange(0, len(starts), settings.MAX_TABS)]

        for each_chunk in start_chunks:

            main_window = browser.get_main_window(driver)
            start_indexes = each_chunk

            for j in range(len(each_chunk)):

                if for_task == settings.TASKS[1]:
                    new_url = query_builder.fetch_resume_link_url(queries, start_indexes[j])
                else:
                    new_url = query_builder.fetch_job_link_url(queries, start_indexes[j])

                browser.execute_javascript(driver, 'window.open("{url}","_blank");'.format(url=new_url))

            for each_window in browser.get_window_handles(driver):

                if each_window != main_window:

                    browser.switch_to_window(driver, each_window)

                    results = get_links_from_page(for_task, driver=driver)
                    final_results.extend(results)

            while len(browser.get_window_handles(driver)) != 1:

                browser.switch_to_window(driver, browser.get_window_handles(driver)[0])
                browser.close_tab(driver)

            browser.switch_to_window(browser.get_window_handles(driver)[0])

    else:
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

    """
    Main caller for the links extraction process

    :param for_task: process for jobs/resumes
    :param queries: list of all the queries
    :return: Null
    """

    filtered_queries = list(map(lambda query: {
        'queries': query[settings.QUERIES_COLUMNS['queries']],
        'key': query[settings.UPDATE_KEY]
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

            if settings.WEBDRIVER_REQUIRED:
                driver = browser.get_browser()
                browser.open_link(driver, url)
                soup = get_soup(url, driver=driver, for_task=for_task)
                browser.close_browser(driver)
            else:
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
                    if settings.WEBDRIVER_REQUIRED:
                        driver = browser.get_browser()
                        processes = [Process(target=fetch_pool_results, args=(for_task, each_query['queries'], each_chunk, driver, )) for each_chunk in start_chunks]
                    else:
                        processes = [Process(target=fetch_pool_results, args=(for_task, each_query['queries'], each_chunk,)) for each_chunk in start_chunks]
                    for process in processes:
                        process.start()
                    for process in processes:
                        process.join()
                    if settings.WEBDRIVER_REQUIRED:
                        browser.close_browser(driver)
                else:
                    if settings.WEBDRIVER_REQUIRED:
                        driver = browser.get_browser()
                        fetch_pool_results(for_task, each_query['queries'], starts, driver)
                        browser.close_browser(driver)
                    else:
                        fetch_pool_results(for_task, each_query['queries'], starts)

            else:

                print "# Result Present: <False>"

            db.update_queries(for_task, each_query['key'], {'status': settings.LINK_EXTRACTION_DONE})

        except Exception as e:

            db.update_queries(for_task, each_query['key'], {'status': settings.LINK_EXTRACTION_ERROR})
            print "# Error: {error}".format(error=str(e))

