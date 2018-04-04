import config as settings


def fetch_job_link_url(query, location, page_count):
    return "{base_uri}/jobs?q={query}&l={location}&start={page_count}".format(base_uri=settings.JOB_BASE_URL, query=query, location=location, page_count=page_count)


def fetch_resume_link(query, location, page_count):
    return "{base_uri}/resumes?q={query}&l={location}&start={page_count}".format(base_uri=settings.RESUME_BASE_URL, query=query, location=location, page_count=page_count)


def fetch_job_url(link):
    return "{base_uri}{url}".format(base_uri=settings.JOB_BASE_URL, url=link)


def fetch_resume_url(link):
    return "{base_uri}{url}".format(base_uri=settings.RESUME_BASE_URL, url=link)