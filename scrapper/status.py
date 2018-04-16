import db
import time
import config as settings
from prettytable import PrettyTable
import os

def fetch_status(job, resume):

    # Link extraction
    if resume:
        rq_p = db.fetch_count('resume_queries', 'pending')
        rq_d = db.fetch_count('resume_queries', 'done')
        rq_e = db.fetch_count('resume_queries', 'error')
    if job:
        jq_p = db.fetch_count('job_queries', 'pending')
        jq_d = db.fetch_count('job_queries', 'done')
        jq_e = db.fetch_count('job_queries', 'error')

    # HTML extraction
    if resume:
        rs_p = db.fetch_count('resume_scrap', 'pending')
        rs_d = db.fetch_count('resume_scrap', 'done')
        rs_e = db.fetch_count('resume_scrap', 'error')
    if job:
        js_p = db.fetch_count('job_scrap', 'pending')
        js_d = db.fetch_count('job_scrap', 'done')
        js_e = db.fetch_count('job_scrap', 'error')

    # HTML parse
    if resume:
        rp_p = db.fetch_count('resume_parse', 'pending')
        rp_d = db.fetch_count('resume_parse', 'done')
        rp_e = db.fetch_count('resume_parse', 'error')
    if job:
        jp_p = db.fetch_count('job_parse', 'pending')
        jp_d = db.fetch_count('job_parse', 'done')
        jp_e = db.fetch_count('job_parse', 'error')

    # Print Result
    if job:
        table_jobs = PrettyTable(['', 'Link Extraction', 'HTML Extraction', 'HTML Parsing'])
        table_jobs.add_row(["Pending", jq_p, js_p, jp_p])
        table_jobs.add_row(["Error", jq_e, js_e, jp_e])
        table_jobs.add_row(["Done", jq_d, js_d, jp_d])
    if resume:
        table_resume = PrettyTable(['', 'Link Extraction', 'HTML Extraction', 'HTML Parsing'])
        table_resume.add_row(["Pending", rq_p, rs_p, rp_p])
        table_resume.add_row(["Error", rq_e, rs_e, rp_e])
        table_resume.add_row(["Done", rq_d, rs_d, rp_d])

    if job:
        print "Jobs:"
        print table_jobs
        print
    if resume:
        print "Resumes:"
        print table_resume


if __name__ == '__main__':

    resume = settings.FOR_RESUME
    job = settings.FOR_JOB

    if resume or job:
        while (True):
            os.system('clear')
            fetch_status(job, resume)
            time.sleep(10)
