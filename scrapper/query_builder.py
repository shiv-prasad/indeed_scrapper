import config as settings


def fetch_job_link_url(queries, page_count):

    """
    Url builder for job links

    :param queries: queries to be passed to the parameters
    :param page_count: pagination
    :return: url for the result page
    """

    url = "{base_uri}?".format(base_uri=settings.JOB_BASE_URL)

    for query in queries.keys():
        url += "{key}={value}&".format(key=query, value=queries[query])

    url += "start={page_count}".format(page_count=page_count)

    return url


def fetch_resume_link_url(queries, page_count):

    """
    Url builder for resume links

    :param queries: queries to be passed to the parameters
    :param page_count: pagination
    :return: url for the result page
    """

    url = "{base_uri}?".format(base_uri=settings.RESUME_BASE_URL)

    for query in queries.keys():
        url += "{key}={value}&".format(key=query, value=queries[query])
    url += "start={page_count}".format(page_count=page_count)

    return url


def fetch_job_url(link):

    """
    Url builder for job page

    :param link: link of the job page
    :return: final url of the job page
    """

    return "{base_uri}{url}".format(base_uri=settings.JOB_HTML_BASE_URL, url=link)


def fetch_resume_url(link):

    """
    Url builder for resume page

    :param link: link of the resume page
    :return: final url of the resume page
    """

    return "{base_uri}{url}".format(base_uri=settings.RESUME_HTML_BASE_URL, url=link)