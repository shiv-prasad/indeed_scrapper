import config as settings
import db as database_methods
import link_scrapper
from multiprocessing import Process


if __name__ == '__main__':

    print "##################################################"

    if settings.WEBDRIVER_REQUIRED:
        print "# Execution with Selenium Webdriver"
    else:
        print "# Execution with Requests and Beautiful Soup"
    print

    if settings.FOR_JOB and settings.FOR_RESUME:

        print "# For: <Jobs and Resumes>"

        queries_jobs, total_jobs = database_methods.fetch_rows(query_for="job_queries", status_for="pending")
        queries_resumes, total_resumes = database_methods.fetch_rows(query_for="resume_queries", status_for="pending")

        if settings.MULTIPROCESS_REQUIRED:

            print "# Multiprocessing: <True>"

            if settings.MULTIPROCESS_TYPE == "sequential":

                print "# Type: <Sequential>"
                print "# Flow: <Jobs -> Resumes>"
                print "# No. of processes for each flow: <{processes}>".format(processes=settings.NO_OF_PROCESSES)

                print "# Total Job Queries (Pending): <{total}>".format(total=total_jobs)
                link_scrapper.fetch_links(settings.TASKS[0], queries_jobs)
                print "# Total Resume Queries (Pending): <{total}>".format(total=total_resumes)
                link_scrapper.fetch_links(settings.TASKS[1], queries_resumes)

            else:

                print "# Type: <Shared>"
                print "# Flow: <Jobs and Resumes as different processes>"
                print "# No. of processes: <2>"
                print "# No. of processes for each flow: <{processes}>".format(processes=settings.NO_OF_PROCESSES)

                print "# Total Job Queries (Pending): <{total}>".format(total=total_jobs)
                print "# Total Resume Queries (Pending): <{total}>".format(total=total_resumes)
                job_process = Process(target=link_scrapper.fetch_links, args=(settings.TASKS[0], queries_jobs,))
                resume_process = Process(target=link_scrapper.fetch_links, args=(settings.TASKS[1], queries_resumes,))

                job_process.start()
                resume_process.start()
                job_process.join()
                resume_process.join()

        else:

            print "# Multiprocessing: <False>"
            print "# Flow: <Jobs -> Resumes>"

            print "# Total Job Queries (Pending): <{total}>".format(total=total_jobs)
            link_scrapper.fetch_links(settings.TASKS[0], queries_jobs)
            print "# Total Resume Queries (Pending): <{total}>".format(total=total_resumes)
            link_scrapper.fetch_links(settings.TASKS[1], queries_resumes)

    elif settings.FOR_JOB or settings.FOR_RESUME:

        if settings.FOR_JOB:

            task_for = settings.TASKS[0]
            queries, total = database_methods.fetch_rows(query_for="job_queries", status_for="pending")
            print "# For: <Jobs>"

        elif settings.FOR_RESUME:

            task_for = settings.TASKS[1]
            queries, total = database_methods.fetch_rows(query_for="resume_queries", status_for="pending")
            print "# For: <Resumes>"

        if settings.MULTIPROCESS_REQUIRED:

            print "# Multiprocessing: <True>"
            print "# No. of processes: <{processes}>".format(processes=settings.NO_OF_PROCESSES)

        else:

            print "# Multiprocessing: <False>"

        print "# Total Queries (Pending): <{total}>".format(total=total)

        link_scrapper.fetch_links(task_for, queries)

    print "##################################################"



