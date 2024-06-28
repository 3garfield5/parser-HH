from flask import render_template, request

from sweater import db, app
from sweater.parser import get_links, get_job
from sweater.models import Vacancy


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/job_search', methods=['POST', 'GET'])
def job_search():
    job = request.form.get('job')

    if request.method == "POST":
        one = request.form.get('1')
        two = request.form.get('2')
        region = request.form.get('region')
        skills = request.form.get('skills')
        work_exp = request.form.get('work exp')
        busyness = request.form.get('busyness')
        chart = request.form.get('chart')

        data = []
        count = 0
        for a in get_links(job): # получение ссылок на вакансии hh
            count += 1
            jobs = get_job(a) # получение данных с самих ссылок
            for key, value in jobs.items(): # обработка данных: перевод из словаря в список
                temp = [key, value]
                data.append(temp)

            if count == 5: # ограничение на количество вакансий, из-за долгой прогрузки
                break
        len_jobs = len(data)

        #добавление данных в бд
        for i in range(0, len_jobs, 6):
            name = data[i][1]

            salary = data[i+1][1]

            work_experience = data[i+2][1]

            charts = data[i+3][1]

            ski = data[i+4][1]

            address = data[i+5][1]

            vac = Vacancy(name=name, salary=salary, work_experience=work_experience, chart=charts, skills=ski, address=address)
            db.session.add(vac)
            db.session.commit()


        if one is None and two is not None: #разделение по нажатиям кнопок, чтобы не срабатывали функции, которые должны выполняться при нажатии на другую кнопку
            db_region = db.session.query(Vacancy)
            id = list(map(lambda x: x.id, db_region))
            region_list = list(map(lambda x: x.address, db_region))

            db_skills = db.session.query(Vacancy)
            skills_list = list(map(lambda x: x.skills, db_skills))

            db_work_exp = db.session.query(Vacancy)
            experience_list = list(map(lambda x: x.work_experience, db_work_exp))

            db_chart = db.session.query(Vacancy)
            chart_list = list(map(lambda x: x.chart, db_chart))
            # создаем списки, где лежат данные из БД, чтобы их отфильтровать

            # фильтр
            work_experience_f = []
            id_del = [] # создаем список, где будут лежать айдишки вакансий, которые нужно убрать при фильтрации
            for i in range(len(id)):
                if region != '': # проверка ну пустоту
                    if region != region_list[i]:
                        id_del.append(i+1)

                if skills != '': # проверка ну пустоту
                    if skills not in skills_list[i]:
                        id_del.append(i + 1)

                if work_exp != '': # проверка ну пустоту
                    if '–' in experience_list[i]:
                        for j in range(int(experience_list[i][0]), int(experience_list[i][2])):
                            work_experience_f.append(j)
                        if int(work_exp) not in work_experience_f:
                            id_del.append(i + 1)

                if chart != '': # проверка ну пустоту
                    chart_list[i] = list(chart_list[i].split(', '))
                    if (busyness not in chart_list[i][0]) or (chart not in chart_list[i][1]):
                        id_del.append(i + 1)
            id_del = set(id_del) # делаем из списка множество

            # удаляем ненужные вакансии
            for i in id_del:
                del_res = db.session.query(Vacancy).filter(Vacancy.id == i).first()
                db.session.delete(del_res)
                db.session.commit()

            # получаем из БД оставшиеся вакансии, чтобы вывести их на страницу
            db_data_filt = db.session.query(Vacancy)

            id = list(map(lambda x: x.id, db_data_filt))
            name_list = list(map(lambda x: x.name, db_data_filt))
            salary_list = list(map(lambda x: x.salary, db_data_filt))
            region_list = list(map(lambda x: x.address, db_data_filt))
            skills_list = list(map(lambda x: x.skills, db_data_filt))
            experience_list = list(map(lambda x: x.work_experience, db_data_filt))
            chart_list = list(map(lambda x: x.chart, db_data_filt))



            return render_template('job_search.html', name_list=name_list, salary_list=salary_list, region_list=region_list, \
                                   skills_list=skills_list, experience_list=experience_list, chart_list=chart_list, id=len(id), one=one, two=two)
        return render_template('job_search.html', data=data, count=count, len_jobs=len_jobs, one=one, two=two)

    db.drop_all() # очистка БД
    db.create_all() # создание новой таблицы БД
    return render_template('job_search.html')

@app.route('/job_seeker_search')
def job_seeker_search():
    return render_template('job_seeker_search.html')