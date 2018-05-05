import config as settings
import db as database_methods
from multiprocessing import Process
from bs4 import BeautifulSoup


def get_soup(html):

    """
    Return soup object from html text provided

    :param html: html to be converted to soup object
    :return: soup object
    """

    return BeautifulSoup(html, 'html.parser')


def parse_pool_results(for_task, queries):

    """
    Parsing of html pages provided

    :param for_task: process for jobs/resumes
    :param queries: list of queries for which HTML have to be parsed
    :return: Null
    """

    for each_query in queries:
        try:
            url = each_query['url']
            html = each_query['html']
            print "# P: [Parsing] <{url}>".format(url=url)

            if for_task == settings.TASKS[0]:

                soup = get_soup(html)
                content = {}

                job_title = None
                company = None
                location = None
                job_summary = None

                try:
                    job_titles = soup.find_all('b', attrs={'class': 'jobtitle'})
                    for each_job_title in job_titles:
                        job_title = each_job_title.text.strip()
                except Exception as e:
                    print "# E: [Job Title] <{error}>".format(error=str(e))

                try:
                    companies = soup.find_all('span', attrs={'class': 'company'})
                    for each_company in companies:
                        company = each_company.text.strip()
                        break
                except Exception as e:
                    print "# E: [Company] <{error}>".format(error=str(e))

                try:
                    locations = soup.find_all('span', attrs={'class': 'location'})
                    for each_location in locations:
                        location = each_location.text.strip()
                        break
                except Exception as e:
                    print "# E: [Location]: <{error}>".format(error=str(e))

                try:
                    summaries = soup.find_all('span', attrs={'id': 'job_summary'})
                    for each_summary in summaries:
                        job_summary = each_summary.text.strip()
                        break
                except Exception as e:
                    print "# E: [Job Summary]: <{error}>".format(error=str(e))

                if job_title:
                    content['job_title'] = job_title
                if company:
                    content['company'] = company
                if location:
                    content['location'] = location
                if job_summary:
                    content['job_summary'] = job_summary

            else:
                soup = get_soup(html)
                content = {}

                resume_title = None
                headline = None
                contact_info = None
                res_summary = None
                work_experience = []
                education = []
                skills = []
                links = []
                awards = []
                additional_info = None

                try:
                    resume_titles = soup.find_all('h1', attrs={'id': 'resume-contact'})
                    for each_resume_title in resume_titles:
                        resume_title = each_resume_title.text.strip()
                        break
                except Exception as e:
                    print "# E: [Resume Title] <{error}>".format(error=str(e))

                try:
                    headlines = soup.find_all('h2', attrs={'id': 'headline'})
                    for each_headline in headlines:
                        headline = each_headline.text.strip()
                        break
                except Exception as e:
                    print "# E: [Headline] <{error}>".format(error=str(e))

                try:
                    contact_infos = soup.find_all('div', attrs={'id': 'contact_info_container'})
                    for each_contact_info in contact_infos:
                        contact_info = each_contact_info.text.strip()
                        break
                except Exception as e:
                    print "# E: [Contact Info] <{error}>".format(error=str(e))

                try:
                    res_summaries = soup.find_all('p', attrs={'id': 'res_summary'})
                    for each_summary in res_summaries:
                        res_summary = each_summary.text.strip()
                        break
                except Exception as e:
                    print "# E: [Res Summary] <{error}>".format(error=str(e))

                try:
                    work_experience_contents = soup.find_all('div', attrs={'class': 'workExperience-content'})
                    for each_content in work_experience_contents:
                        work_experience_sections = each_content.find_all('div', attrs={'class': 'work-experience-section'})
                        for each_section in work_experience_sections:
                            work = {}
                            titles = each_section.find_all(name='p', attrs={'class': 'work_title'})
                            for each_title in titles:
                                work['title'] = each_title.text.strip()
                            work_companies = each_section.find_all(name='div', attrs={'class': 'work_company'})
                            for each_company in work_companies:
                                work['company'] = each_company.text.strip()
                            work_dates = each_section.find_all(name='p', attrs={'class': 'work_dates'})
                            for each_date in work_dates:
                                work['work_dates'] = each_date.text.strip()
                            descriptions = each_section.find_all(name='p', attrs={'class': 'work_description'})
                            for each_description in descriptions:
                                work['description'] = each_description.text.strip()
                            work_experience.append(work)
                except Exception as e:
                    print "# E: [Work Experience] <{error}>".format(error=str(e))

                try:
                    education_contents = soup.find_all('div', attrs={'class': 'education-content'})
                    for each_content in education_contents:
                        education_sections = each_content.find_all('div', attrs={'class': 'education-section'})
                        for each_section in education_sections:
                            education_item = {}
                            titles = each_section.find_all(name='p', attrs={'class': 'edu_title'})
                            for each_title in titles:
                                education_item['title'] = each_title.text.strip()
                            edu_schools = each_section.find_all(name='div', attrs={'class': 'edu_school'})
                            for each_edu_school in edu_schools:
                                education_item['school'] = each_edu_school.text.strip()
                            edu_dates = each_section.find_all(name='p', attrs={'class': 'edu_dates'})
                            for each_date in edu_dates:
                                education_item['edu_dates'] = each_date.text.strip()
                            descriptions = each_section.find_all(name='p', attrs={'class': 'edu_description'})
                            for each_description in descriptions:
                                education_item['description'] = each_description.text.strip()
                            education.append(education_item)
                except Exception as e:
                    print "# E: [Education] <{error}>".format(error=str(e))

                try:
                    skill_contents = soup.find_all('div', attrs={'class': 'skills-content'})
                    for each_content in skill_contents:
                        skill_sections = each_content.find_all('div', attrs={'id': 'skills-items'})
                        for each_section in skill_sections:
                            skill_texts = each_section.find_all(name='span', attrs={'class': 'skill-text'})
                            for each_text in skill_texts:
                                skills.append(each_text.text.strip())
                except Exception as e:
                    print "# E: [Skills] <{error}>".format(error=str(e))

                try:
                    links_contents = soup.find_all('div', attrs={'class': 'links-content'})
                    for each_content in links_contents:
                        links_sections = each_content.find_all('div', attrs={'id': 'link-items'})
                        for each_section in links_sections:
                            links_texts = each_section.find_all(name='p', attrs={'class': 'link_url'})
                            for each_text in links_texts:
                                links.append(each_text.text.strip())
                except Exception as e:
                    print "# E: [Links] <{error}>".format(error=str(e))

                try:
                    awards_contents = soup.find_all('div', attrs={'class': 'awards-content'})
                    for each_content in awards_contents:
                        awards_sections = each_content.find_all('div', attrs={'class': 'award-section'})
                        for each_section in awards_sections:
                            award_item = {}
                            titles = each_section.find_all(name='p', attrs={'class': 'award_title'})
                            for each_title in titles:
                                award_item['title'] = each_title.text.strip()
                            award_dates = each_section.find_all(name='p', attrs={'class': 'award_date'})
                            for each_date in award_dates:
                                award_item['date'] = each_date.text.strip()
                            descriptions = each_section.find_all(name='p', attrs={'class': 'award_description'})
                            for each_description in descriptions:
                                award_item['description'] = each_description.text.strip()
                            awards.append(award_item)
                except Exception as e:
                    print "# E: [Awards] <{error}>".format(error=str(e))

                try:
                    additionalInfo_contents = soup.find_all('div', attrs={'class': 'additionalInfo-content'})
                    for each_content in additionalInfo_contents:
                        additionalinfo_sections = each_content.find_all('div', attrs={'id': 'additionalinfo-section'})
                        for each_section in additionalinfo_sections:
                            additional_info = each_section.text.strip()
                except Exception as e:
                    print "# E: [Work Experience] <{error}>".format(error=str(e))

                if resume_title:
                    content['resume_title'] = resume_title
                if headline:
                    content['headline'] = headline
                if contact_info:
                    content['contact_info'] = contact_info
                if res_summary:
                    content['res_summary'] = res_summary
                if len(work_experience) > 0:
                    content['work_experience'] = work_experience
                if len(education) > 0:
                    content['education'] = education
                if len(skills) > 0:
                    content['skills'] = skills
                if len(links) > 0:
                    content['links'] = links
                if len(awards) > 0:
                    content['awards'] = awards
                if additional_info:
                    content['additional_info'] = additional_info

            database_methods.update_parse(for_task, each_query['key'], {'status': settings.HTML_PARSING_DONE, 'content': content}, add=True)
            print "# O: [Parsing] <Done>"

        except Exception as e:

            database_methods.update_parse(for_task, each_query['key'], {'status': settings.HTML_PARSING_ERROR})
            print "# E: [Parsing] <{error}>".format(error=str(e))


def parse_html(for_task, html_queries):

    """
    Mail caller for parsing all the html pages given

    :param for_task: process for job/resumes
    :param html_queries: list of all HTML queries
    :return: Null
    """

    if for_task == settings.TASKS[0]:
        columns = settings.JOBS_COLUMNS
    else:
        columns = settings.RESUMES_COLUMNS

    filtered_queries = list(map(lambda query: {
        'url': query[columns['link']],
        'html': query[columns['html_content']],
        'key': query[settings.UPDATE_KEY]
    }, html_queries))

    if settings.MULTIPROCESS_REQUIRED:
        partition = int(len(filtered_queries) / settings.NO_OF_PROCESSES)
        if partition == 0:
            partition += 1
        queries_chunks = [filtered_queries[i:i + partition] for i in xrange(0, len(filtered_queries), partition)]

        processes = [Process(target=parse_pool_results, args=(for_task, each_chunk,)) for each_chunk in queries_chunks]

        for process in processes:
            process.start()
        for process in processes:
            process.join()
    else:
        parse_pool_results(for_task, filtered_queries)


if __name__ == '__main__':

    print "##################################################"
    print
    print "# I: [Execution] Beautiful Soup"
    print

    if settings.FOR_JOB and settings.FOR_RESUME:

        print "# I: [For] <Jobs and Resumes>"

        parse_jobs, total_jobs = database_methods.fetch_rows(query_for="job_parse", status_for="pending")
        parse_resumes, total_resumes = database_methods.fetch_rows(query_for="resume_parse", status_for="pending")

        if settings.MULTIPROCESS_REQUIRED:

            print "# I: [Multiprocessing] <True>"

            if settings.MULTIPROCESS_TYPE == "sequential":

                print "# I: [Type] <Sequential>"
                print "# I: [Flow] <Jobs -> Resumes>"
                print "# I: [No. of Processes] <{processes}> (For each flow)".format(processes=settings.NO_OF_PROCESSES)

                print "# I: [Total Job HTMLs] <{total}> (Pending)".format(total=total_jobs)
                parse_html(settings.TASKS[0], parse_jobs)
                print "# I: [Total Resume HTMLs]<{total}> (Pending)".format(total=total_resumes)
                parse_html(settings.TASKS[1], parse_resumes)

            else:

                print "# I: [Type] <Shared>"
                print "# I: [Flow] <Jobs and Resumes as different processes>"
                print "# I: [No. of Processes] <2>"
                print "# I: [No. of Processes] <{processes}> (For each flow)".format(processes=settings.NO_OF_PROCESSES)

                print "# I: [Total Job HTMLs] <{total}> (Pending)".format(total=total_jobs)
                print "# I: [Total Resume HTMLs] <{total}> (Pending)".format(total=total_resumes)
                job_process = Process(target=parse_html, args=(settings.TASKS[0], parse_jobs,))
                resume_process = Process(target=parse_html, args=(settings.TASKS[1], parse_resumes,))

                job_process.start()
                resume_process.start()
                job_process.join()
                resume_process.join()

        else:

            print "# I: [Multiprocessing] <False>"
            print "# I: [Flow] <Jobs -> Resumes>"

            print "# I: [Total Job HTMLs] <{total}> (Pending)".format(total=total_jobs)
            parse_html(settings.TASKS[0], parse_jobs)
            print "# I: [Total Resume HTMLs] <{total}> (Pending)".format(total=total_resumes)
            parse_html(settings.TASKS[1], parse_resumes)

    elif settings.FOR_JOB or settings.FOR_RESUME:

        if settings.FOR_JOB:

            task_for = settings.TASKS[0]
            parse, total = database_methods.fetch_rows(query_for="job_parse", status_for="pending")
            print "# I: [For] <Jobs>"

        elif settings.FOR_RESUME:

            task_for = settings.TASKS[1]
            parse, total = database_methods.fetch_rows(query_for="resume_parse", status_for="pending")
            print "# I: [For] <Resumes>"

        if settings.MULTIPROCESS_REQUIRED:

            print "# I: [Multiprocessing] <True>"
            print "# I: [No. of Processes] <{processes}>".format(processes=settings.NO_OF_PROCESSES)

        else:

            print "# I: [Multiprocessing] <False>"

        print "# I: [Total HTMLs] <{total}> (Pending)".format(total=total)
        parse_html(task_for, parse)

    print
    print "##################################################"

