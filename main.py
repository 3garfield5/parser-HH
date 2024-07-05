from sweater import app, db

with app.app_context():
    db.drop_all()  # очистка БД
    db.create_all()  # создание новой таблицы БД

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)