import config as settings


def fetch_job_link_url(queries, page_count):
    url = "{base_uri}?".format(base_uri=settings.JOB_BASE_URL)
    for query in queries.keys():
        url += "{key}={value}&".format(key=query, value=queries[query])
    url += "start={page_count}".format(page_count=page_count)
    return url


def fetch_resume_link(queries, page_count):
    url = "{base_uri}?".format(base_uri=settings.RESUME_BASE_URL)
    for query in queries.keys():
        url += "{key}={value}&".format(key=query, value=queries[query])
    url += "start={page_count}".format(page_count=page_count)
    return url


def fetch_job_url(link):
    return "{base_uri}{url}".format(base_uri=settings.JOB_BASE_URL, url=link)


def fetch_resume_url(link):
    return "{base_uri}{url}".format(base_uri=settings.RESUME_BASE_URL, url=link)