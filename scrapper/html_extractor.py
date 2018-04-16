import config as settings
import db as database_methods
import html_scrapper
from multiprocessing import Process

if __name__ == '__main__':

    if settings.WEBDRIVER_REQUIRED:

        print "##################################################"
        print "# Execution with Selenium Webdriver>"
        print "##################################################"

    else:

        print "##################################################"
        print "# Execution with Requests and Beautiful Soup"
        print

        if settings.FOR_JOB and settings.FOR_RESUME:

            print "# For: <Jobs and Resumes>"

            scrap_jobs, total_jobs = database_methods.fetch_rows(query_for="job_scrap", status_for="pending")
            scrap_resumes, total_resumes = database_methods.fetch_rows(query_for="resume_scrap", status_for="pending")

            if settings.MULTIPROCESS_REQUIRED:

                print "# Multiprocessing: <True>"

                if settings.MULTIPROCESS_TYPE == "sequential":

                    print "# Type: <Sequential>"
                    print "# Flow: <Jobs -> Resumes>"
                    print "# No. of processes for each flow: <{processes}>".format(processes=settings.NO_OF_PROCESSES)

                    print "# Total Job Links (Pending): <{total}>".format(total=total_jobs)
                    html_scrapper.fetch_html(settings.TASKS[0], scrap_jobs)
                    print "# Total Resume Links (Pending): <{total}>".format(total=total_resumes)
                    html_scrapper.fetch_html(settings.TASKS[1], scrap_resumes)

                else:

                    print "# Type: <Shared>"
                    print "# Flow: <Jobs and Resumes as different processes>"
                    print "# No. of processes: <2>"
                    print "# No. of processes for each flow: <{processes}>".format(processes=settings.NO_OF_PROCESSES)

                    print "# Total Job Links (Pending): <{total}>".format(total=total_jobs)
                    print "# Total Resume Links (Pending): <{total}>".format(total=total_resumes)
                    job_process = Process(target=html_scrapper.fetch_html, args=(settings.TASKS[0], scrap_jobs,))
                    resume_process = Process(target=html_scrapper.fetch_html, args=(settings.TASKS[1], scrap_resumes,))

                    job_process.start()
                    resume_process.start()
                    job_process.join()
                    resume_process.join()

            else:

                print "# Multiprocessing: <False>"
                print "# Flow: <Jobs -> Resumes>"

                print "# Total Job Links (Pending): <{total}>".format(total=total_jobs)
                html_scrapper.fetch_html(settings.TASKS[0], scrap_jobs)
                print "# Total Resume Links (Pending): <{total}>".format(total=total_resumes)
                html_scrapper.fetch_html(settings.TASKS[1], scrap_resumes)

        elif settings.FOR_JOB or settings.FOR_RESUME:

            if settings.FOR_JOB:

                task_for = settings.TASKS[0]
                scrap, total = database_methods.fetch_rows(query_for="job_scrap", status_for="pending")
                print "# For: <Jobs>"

            elif settings.FOR_RESUME:

                task_for = settings.TASKS[1]
                scrap, total = database_methods.fetch_rows(query_for="resume_scrap", status_for="pending")
                print "# For: <Resumes>"

            if settings.MULTIPROCESS_REQUIRED:

                print "# Multiprocessing: <True>"
                print "# No. of processes: <{processes}>".format(processes=settings.NO_OF_PROCESSES)

            else:

                print "# Multiprocessing: <False>"

            print "# Total Links (Pending): <{total}>".format(total=total)
            html_scrapper.fetch_html(task_for, scrap)

        print "##################################################"

