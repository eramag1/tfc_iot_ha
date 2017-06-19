from flask import Flask
from flask import request, render_template
from fiware.orion.ngsiv2_client import NGSIv2Client

from multiprocessing.pool import ThreadPool

import time
from random import randint

app = Flask(__name__)

client = NGSIv2Client()
num_jobs = 10
chunk_size = 1
num_workers = 2


def manage_exception(ex):
    message = "Error {0}".format(ex)
    print(message)
    template = "error.html"
    return render_template(template, message=message)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/list_entities', methods=['GET'])
def list_entities():
    try:
        entity_list = client.get_entities()
        template = "list_entities.html"
        return render_template(template, entity_list=entity_list)
    except Exception as ex:
        return manage_exception(ex)


@app.route('/create_entity', methods=['GET', 'POST'])
def create_entity():
    if request.method == 'GET':
        return render_template("create_entity.html")

    id = request.form['id']
    type = request.form['type']
    temperature = request.form['temperature']
    pressure = request.form['pressure']
    try:
        entity = client.create_entity(id=id, type=type, temperature=temperature, pressure=pressure)
        template = "show_entity.html"
        return render_template(template, entity=entity)
    except Exception as ex:
        return manage_exception(ex)


@app.route('/show_entity', methods=['GET', 'POST'])
def show_entity():

    id = request.args.get('id')

    try:
        entity = client.get_entity(id)
        template = "show_entity.html"
        return render_template(template, entity=entity)
    except Exception as ex:
        return manage_exception(ex)


@app.route('/update_entity', methods=['GET', 'POST'])
def update_entity():

    id = request.form['id']
    temperature = request.form['temperature']
    pressure = request.form['pressure']
    try:
        entity = client.set_entity_attrs(id, temperature, pressure)
        template = "entity_updated.html"
        return render_template(template, entity=entity)
    except Exception as ex:
        return manage_exception(ex)


@app.route('/delete_entity', methods=['POST'])
def delete_entity():
    if request.method == 'GET':
        return render_template("delete_entity.html")

    id = request.form['id']
    try:
        template = "entity_deleted.html"
        entity = None
        return render_template(template, entity=entity)
    except Exception as ex:
        return manage_exception(ex)


def multi_update_account(arg):
    """
    :param arg: tuple data to convert in arguments
    :param kwarg: dict data to convert in arguments
    :return: tuples (account_id, result update)
    """
    client.set_source_ip(arg[1])
    return arg[0], arg[1], client.set_entity_attrs(arg[0], arg[2], arg[3])


def get_entities_as_job_args(uuid, req_size, diff_ips, temperature, pressure):
    """
    :param uuid: UUID of the device
    :param req_size: Number of update requests
    :param diff_ips: Source IPs used in update requests
    :return: tuples (uuid, temperature, pressure)
    """
    job_args = []
    num_jobs = int(req_size)
    source_ip = "10.0.0.{0}"

    while num_jobs > 0:
        for i in range(int(diff_ips)):
            tupla = (uuid, source_ip.format(i), temperature, pressure)
            job_args.append(tupla)
        num_jobs -= chunk_size
    return job_args


@app.route('/send_bulk_request', methods=['GET', 'POST'])
def send_bulk_request():

    if request.method == 'GET':
        return render_template("send_bulk_request.html")

    uuid = request.form['uuid']
    req_size = request.form['req_size']
    diff_ips = request.form['diff_ips']
    temperature = request.form['temperature']
    pressure = request.form['pressure']

    pool = ThreadPool(processes=num_workers)
    job_args = get_entities_as_job_args(uuid, req_size, diff_ips, temperature, pressure)
    start = time.time()
    result = pool.map(multi_update_account, job_args)  # job_args = [(uuid, source_ip, 20, 20), (uuid, source_ip, 20, 20) ...]
    # result [(id,ip,update_result) ,()...,()]
    end = time.time()
    print "Updated " + str(num_jobs) + " Accounts (" + str(num_workers) + " process workers) TIME: " + str(end - start)

    print "RESULT" + str(result)

    return render_template('bulk_updated.html', result=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
