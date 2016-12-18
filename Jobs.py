from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request

from SQL_init import create_post_table
from SQL_init import seed_post_table
from SQL_init import test_post_table
import psycopg2 as dbApi
from flask import current_app as app
from unicodedata import category

from flask_login import current_user
from flask_login.utils import login_required

jobs = Blueprint('jobs', __name__)

@jobs.route("/jobs")
@login_required
def main():
    return render_template("/jobs/jobs.html", jobs=list_all_jobs())


@jobs.route("/add-new-job", methods=['GET', 'POST'])
@login_required
def get_new_job():
    if request.method == "GET":
        return render_template("jobs/add-new-job.html")
    else:
        title = request.form.get('job_title')
        description = request.form.get('description')
        location = request.form.get('location')
        salary = request.form.get('salary')
        is_remote = request.form.get('is_remote')
        create_new_job(title, description, location, salary, is_remote)
        return redirect('/jobs')
    
def create_new_job(job_title, description, location, salary, is_remote):
    with dbApi.connect(app.config['dsn']) as connection:
        if is_remote == "None":
            is_remote = False
        else:
            is_remote = True

        query = """INSERT INTO JOB_OFFERS (user_id, job_title, description, location, salary, is_remote)
VALUES (%s, '%s', '%s', '%s', %d, %s);""" % (
        current_user.id, job_title, description, location, int(salary), is_remote)

        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        return True
    
    
def list_all_jobs():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT JOB_OFFERS.id,
        us.name, job_title, description, location, salary,
        is_remote
        from JOB_OFFERS JOIN USERS as us
        ON us.id = JOB_OFFERS.user_id
        ORDER BY salary;"""
        cursor.execute(query)
        connection.commit()
        return cursor
def select_job(id):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT job_title, description, location, salary,
        is_remote
        from JOB_OFFERS where id=%s""" % id
        cursor.execute(query)
        connection.commit()
        return cursor
def delete_offer(id):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """DELETE FROM JOB_OFFERS
        WHERE id = %s;""" % id
        cursor.execute(query)
        connection.commit()
        return True
    
@jobs.route("/delete-job/<job_id>")
def delete_job_from_list(job_id):
    delete_offer(job_id)
    return redirect('/jobs')

@jobs.route("/update-job/<job_id>", methods=['GET', 'POST'])
def update_job_list(job_id):
    if request.method == "GET":
        object = select_job(job_id).fetchone()
        if object:
            job_title = object[0]
            description = object[1]
            location = object[2]
            salary = object[3]
            is_remote = object[4]
            return render_template("jobs/update-job.html",
                                   object=object, job_title=job_title, description=description, location=location, salary=salary, is_remote=is_remote)
        else:
            return redirect('/jobs')
    else:
            job_title = request.form.get('job_title')
            description = request.form.get('description')
            location = request.form.get('location')
            salary = request.form.get('salary')
            is_remote = request.form.get('is_remote')
            update_job(job_id, job_title, description, location, salary, is_remote);
    return redirect('/jobs')


def update_job(job_id, job_title, description, location, salary, is_remote):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        if is_remote == "on":
            is_remote = True
        else:
            is_remote = False

        query = """UPDATE JOB_OFFERS SET
        job_title='%s',
        description='%s',
        location='%s',
        salary=%d,
        is_remote=%s
        WHERE id = %s;""" % (job_title, description, location, int(salary), is_remote, job_id)
        cursor.execute(query)
        connection.commit()

        return True
    
