#encoding=utf8
# with app.open_resource('schema.sql') as f:
#     contents = f.read()
#     do_something_with(contents)
#     http://dormousehole.readthedocs.org/en/latest/api.html#application-object

from scrapyc.server.flask.app import flask_app
from flask import render_template
from flask import request


def start_job(project_name,spider_name,task_name,params):
    scheduler = flask_app.config["scheduler_proxy"]
    ret,msg = scheduler.task_start(project_name,spider_name,task_name,params)
    return ret,msg


@flask_app.route('/')
def index():
    return render_template('index.html', flask_app=flask_app)

@flask_app.route('/task_start',methods=['POST', 'GET'])
def task_start():
    try:
        print request.form
        project_name = request.form["project_name"].strip()
        spider_name = request.form["spider_name"].strip()
        task_name = request.form["task_name"].strip()
        spider_params = request.form["spider_params"].strip()
        cron_type = request.form["cron_type"].strip()
        cron_minute = request.form["cron_minute"].strip()
        cron_hour = request.form["cron_hour"].strip()
        cron_day = request.form["cron_day"].strip()
        cron_month = request.form["cron_month"].strip()
        cron_week = request.form["cron_week"].strip()
        start_date = request.form["start_date"].strip()
        end_date = request.form["end_date"].strip()
        
    except  KeyError, e:
        return e
    params = {}
    for line in  spider_params.split():
        line = line.split("=",1)
        if len(line)  !=2 :
            continue
        params[line[0]] = line[1]

    if cron_type == "no":
        scheduler = flask_app.config["scheduler_proxy"]
        ret,msg = scheduler.task_start(project_name,spider_name,task_name,params)
        if ret == True:
            return "Success"
        else:
            return msg
    elif cron_type in ["interval","date","cron"]:
        apscheduler = flask_app.config["apscheduler"]
        job = apscheduler.add_job(
            func="scrapyc.server.flask.views:start_job",
            trigger=cron_type,
            kwargs={"project_name":project_name,'spider_name':spider_name,'task_name':task_name,'params':params},
            max_instances=1, replace_existing=True,
            month = cron_month,
            day = cron_day,
            week = cron_week,
            hour =cron_hour,
            minute = cron_minute,
            start_date=start_date,
            end_date =end_date,)
        if job:
            return 'success'
    else:
        return "unkown cron_type:%s"%cron_type
    return "failed"

    
@flask_app.route('/task_kill',methods=['POST', 'GET'])
def task_kill():
    task_id = request.args.get('task_id', '')
    if not task_id:
        return {}
    scheduler = flask_app.config["scheduler_proxy"]
    scheduler.task_kill(task_id)


@flask_app.route('/task_stop',methods=['POST', 'GET'])
def task_stop():
    task_id = request.args.get('task_id', '')
    if not task_id:
        return {}
    scheduler = flask_app.config["scheduler_proxy"]
    scheduler.task_stop(task_id)

@flask_app.route('/crontab')
def crontab():

        return render_template('crontab.html', flask_app=flask_app)

@flask_app.route('/new_task')
def new_task():
     return render_template('new_task.html', flask_app=flask_app)
