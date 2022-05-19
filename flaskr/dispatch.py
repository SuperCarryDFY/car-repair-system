import traceback
from json import dumps
from flask import (
    Blueprint, make_response, request
)

from flaskr.db import get_db

bp = Blueprint('dispatch', __name__, url_prefix='/dispatch')


@bp.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'POST':
        db = get_db()
        error = None
        # 获取表单数据
        repair_number = request.form['repair_number']
        repair_project = request.form['repair_project']
        hours = request.form['hours']
        repair_man_number = request.form['repair_man_number']

        try:
            db.execute(
                "INSERT INTO car_sys.repair_dispatch (repair_number, repair_project, hours, repair_man_number) VALUES('{}','{}','{}','{}')".format(
                    repair_number, repair_project, hours, repair_man_number)
            )
        except Exception as e:
            error = traceback.format_exc()
            traceback.print_exc()
            response = make_response(dumps(error), 404)
        else:
            response = make_response(
                dumps('create dispatch successfully'), 200)
        return response

    else:
        return '/dispatch/register'


@bp.route('/search', methods=('POST','GET'))
def search():
    if request.method == 'POST':
        db = get_db()
        error = None
        repair_number = request.form['repair_number']
        repair_man_number = request.form['repair_man_number']
        try:
            if not repair_number and not repair_man_number:
                rows = db.prepare("select * from car_sys.repair_dispatch")
            elif not repair_number:
                rows = db.prepare("select * from car_sys.repair_dispatch where repair_man_number='{}'".format(repair_man_number))
            elif not repair_man_number:
                rows = db.prepare("select * from car_sys.repair_dispatch where repair_number='{}'".format(repair_number))
            else:
                rows = db.prepare("select * from car_sys.repair_dispatch where repair_number='{}' and repair_man_number='{}'".format(repair_number,repair_man_number))
        except Exception as e:
            error = traceback.format_exc()
            response = make_response(dumps(error), 404) 
        else:
            res = []
            info = rows()
            for row in info:
                dic = {}
                dic['repair_number'] = row[0]
                dic['repair_project'] = row[1]
                dic['hours'] = row[2]
                dic['repair_man_number'] = row[3]
                res.append(dic)
            response = make_response(dumps(res),200)
        return response
    else:
        return 'dispatch/search'
