from flask import render_template, request

from sweater import db, app
from sweater.parser import get_links, get_job


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/job_search', methods=['POST', 'GET'])
def job_search():
    job = request.form.get('job')
    region = request.form.get('region')
    skills = request.form.get('skills')
    work_exp = request.form.get('work exp')
    busyness = request.form.get('busyness')
    chart = request.form.get('chart')

    if request.method == "POST":
        count = 0
        for a in get_links(job):
            count += 1
            if 'https://hh.ru/vacancy/' in a:
                jobs = get_job(a)
                if region in jobs['address'] and skills in jobs['skills'] \
                        and work_exp in jobs['work experience']  and (busyness in jobs['chart'] or chart in jobs['chart']):
                    if count == 10:
                        break
                return render_template('job_search.html', jobs=jobs, count=count)



    return render_template('job_search.html')

@app.route('/job_seeker_search')
def job_seeker_search():
    return render_template('job_seeker_search.html')