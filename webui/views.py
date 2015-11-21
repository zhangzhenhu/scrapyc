# encoding=utf8
# with app.open_resource('schema.sql') as f:
#     contents = f.read()
#     do_something_with(contents)
#     http://dormousehole.readthedocs.org/en/latest/api.html#application-object

from .app import flask_app
from flask import render_template, jsonify, abort
from flask import request
from datetime import datetime
from .utils import str2date, str2dict, str2int


def start_job(project_name, spider_name, task_name, params):
    scheduler = flask_app.config["scheduler_proxy"]
    ret, msg = scheduler.task_start(project_name, spider_name, task_name, params)
    return ret, msg


@flask_app.route('/')
def index():
    return render_template('index.html', flask_app=flask_app)


@flask_app.route('/run_list', methods=['POST', 'GET'])
def run_list():
    return render_template('_runlist.html', flask_app=flask_app)


@flask_app.route('/history/<int:pagenum>/<int:pagecount>', methods=['POST', 'GET'])
def history(pagenum, pagecount=10):
    return render_template('_history.html', flask_app=flask_app, pagenum=pagenum, pagecount=pagecount)


@flask_app.route('/history/all/<int:pagenum>', methods=['POST', 'GET'])
def history_all(pagenum=1):
    return render_template('history.html', flask_app=flask_app, pagenum=pagenum)


@flask_app.route('/project_list', methods=['POST', 'GET'])
def project_list():
    return render_template('_projectlist.html', flask_app=flask_app)


@flask_app.route('/task_start', methods=['POST', 'GET'])
def task_start():
    """
    启动一个任务
    Returns:

    """
    try:
        # 读取表单信息
        project_name = request.form["project_name"].strip()
        spider_name = request.form["spider_name"].strip()
        task_name = request.form["task_name"].strip()
        spider_config = str2dict(request.form["spider_config"].strip())
        scrapy_config = str2dict(request.form["scrapy_config"].strip())
        cron_type = request.form["cron_type"].strip()

    except KeyError, e:
        return jsonify(ok=False, msg=str(e))
    # crontab任务服务
    apscheduler = flask_app.config["apscheduler"]
    if cron_type == "no":
        # 不是ct任务
        scheduler = flask_app.config["scheduler_proxy"]
        ret, msg = scheduler.task_start(project_name, spider_name, task_name, scrapy_config, spider_config)

        return jsonify(ok=ret, msg="Success")

    elif cron_type == "interval":
        # 每个一定时间启动一次的类型
        cron_minute = str2int(request.form["cron_minute"], 0)
        cron_hour = str2int(request.form["cron_hour"], 0)
        cron_day = str2int(request.form["cron_day"], 0)
        cron_month = str2int(request.form["cron_month"], 0)
        cron_week = str2int(request.form["cron_week"], 0)
        start_date = str2date(request.form["start_date"].strip())
        end_date = str2date(request.form["end_date"].strip())
        job = apscheduler.add_job(
            name=task_name,
            func="scrapyc.server.flask.views:start_job",
            trigger=cron_type,
            kwargs={"project_name": project_name, 'spider_name': spider_name, 'task_name': task_name, 'params': params},
            max_instances=1, replace_existing=True,
            days=cron_day,
            weeks=cron_week,
            hours=cron_hour,
            minutes=cron_minute,
            start_date=start_date,
            end_date=end_date, )
    elif cron_type == "cron":
        # 类似unix下crontab定时任务的类型
        cron_minute = request.form["cron_minute"]
        cron_hour = request.form["cron_hour"]
        cron_day = request.form["cron_day"]
        cron_month = request.form["cron_month"]
        cron_week = request.form["cron_week"]
        start_date = str2date(request.form["start_date"].strip())
        end_date = str2date(request.form["end_date"].strip())

        job = apscheduler.add_job(
            name=task_name,
            func="scrapyc.server.flask.views:start_job",
            trigger=cron_type,
            kwargs={"project_name": project_name, 'spider_name': spider_name, 'task_name': task_name, 'params': params},
            max_instances=1, replace_existing=True,
            months=cron_month,
            days=cron_day,
            weeks=cron_week,
            hours=cron_hour,
            minutes=cron_minute,
            start_date=start_date,
            end_date=end_date, )
    elif cron_type == "date":
        # 定时未来某个时间点启动的类型
        start_date = str2date(request.form["start_date"].strip())
        job = apscheduler.add_job(
            name=task_name,
            func="scrapyc.server.flask.views:start_job",
            trigger=cron_type,
            kwargs={"project_name": project_name, 'spider_name': spider_name, 'task_name': task_name, 'params': params},
            max_instances=1, replace_existing=True,
            run_date=start_date)
    else:
        return jsonify(ok=False, msg="unkown cron_type:%s" % cron_type)

    if job:
        return jsonify(ok=True, msg='success')
    return jsonify(ok=False, msg="failed")


@flask_app.route('/task/kill', methods=['POST', 'GET'])
def task_kill():
    """
    强制杀死一个任务
    Returns:

    """
    task_id = request.args.get('task_id', '')
    if not task_id:
        return jsonify(ok=False, msg="no param:task_id")
    scheduler = flask_app.config["scheduler_proxy"]
    ret, msg = scheduler.task_kill(task_id)
    return jsonify(ok=ret, msg=msg)


@flask_app.route('/crontab')
def crontab():
    return render_template('crontab.html', flask_app=flask_app)


@flask_app.route('/new_task')
def new_task():
    return render_template('new_task.html', flask_app=flask_app)


@flask_app.route('/cronjob_modify')
def cronjob_modify():
    return jsonify()


@flask_app.route('/cronjob_pause', methods=['POST', 'GET'])
def cronjob_pause():
    job_id = request.args.get('job_id', '')
    if not job_id:
        return jsonify(ok=False, msg="no param:job_id")
    apscheduler = flask_app.config["apscheduler"]
    job = apscheduler.get_job(job_id)
    if not job:
        return jsonify(ok=False, msg="job not found.job_id:%s" % job_id)
    job.pause()
    return jsonify(ok=True, msg="success")


@flask_app.route('/cronjob_remove', methods=['POST', 'GET'])
def cronjob_remove():
    job_id = request.args.get('job_id', '')
    if not job_id:
        return jsonify(ok=False, msg="no param:job_id")
    apscheduler = flask_app.config["apscheduler"]
    job = apscheduler.get_job(job_id)
    if not job:
        return jsonify(ok=False, msg="job not found.job_id:%s" % job_id)
    job.remove()
    return jsonify(ok=True, msg="success")


@flask_app.route('/cronjob_removeall', methods=['POST', 'GET'])
def cronjob_removeall():
    """
    删除所有crontab任务
    Returns:

    """
    apscheduler = flask_app.config["apscheduler"]
    apscheduler.remove_all_jobs()
    return jsonify(ok=True, msg="success")


@flask_app.route('/task/stop/<task_id>', methods=['POST', 'GET'])
def task_stop(task_id):
    """
    停止一个任务
    Args:
        task_id:

    Returns:

    """
    task = flask_app.config["scheduler"].task_queue.get_task(task_id)
    if not task:
        # abort(404)
        return jsonify(ok=False, msg="no task:task_id")
    try:
        task.stop()
        # ws.cmd_stop(port=task.webservice_port,spider=task.spider)
        return jsonify(ok=True, msg="success")
    except Exception, e:
        # raise e
        return jsonify(ok=False, msg=str(e))


@flask_app.route('/task/log/<task_state>/<task_id>', methods=['POST', 'GET'])
def task_log(task_state, task_id):
    if task_state == "run":
        task = flask_app.config["scheduler"].task_queue.get_task(task_id)
        if not task:
            abort(404)
        return render_template('task_log_run.html', flask_app=flask_app, task=task, webservice=ws)
    elif task_state == "hist":
        task = flask_app.config["scheduler"].history_queue.get(task_id)
        if not task:
            abort(404)
        return render_template('task_log_hist.html', flask_app=flask_app, task=task, webservice=ws)

    abort(404)


@flask_app.route('/task/stats/<task_id>', methods=['POST', 'GET'])
def task_stats(task_id):
    task = flask_app.config["scheduler"].task_queue.get_task(task_id)
    if not task:
        abort(404)
    return render_template('_scrapy_stats.html', flask_app=flask_app, task=task, webservice=ws)
