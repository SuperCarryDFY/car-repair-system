
import traceback
from json import dumps
from flask import (
    Blueprint, url_for, make_response,request
)

from flaskr.db import get_db

bp = Blueprint('client', __name__, url_prefix='/client')


@bp.route('/register', methods=('POST','GET'))
def register():
    if request.method == 'POST':
        db = get_db()
        error = None
        # 获取表单数据
        client_name = request.form['name']
        client_cha = request.form['type']
        discount = request.form['discount']
        contact_man = request.form['contact_man']
        contact_number = request.form['contact_number']
        # 生成客户编号
        num = db.prepare("select count(*) from car_sys.client")
        num = str(num()[0][0])
        num = (4-len(num))*'0'+num
        client_number = 'GS'+num
        try:
            db.execute(
                "INSERT INTO car_sys.client (client_number, client_name, client_cha, discount, contact_man, contact_number) VALUES('{}','{}','{}','{}','{}','{}')".format(
                    client_number, client_name, client_cha, discount, contact_man, contact_number)
            )
        except Exception as e:
            error = traceback.format_exc()
            traceback.print_exc()
            response = make_response(dumps(error), 404)

        else:
            response = make_response(
                dumps('register {} successfully'.format(client_name)), 200)

        return response
    else:
        return 'good'