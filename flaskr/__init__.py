import os
from flask import Flask
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app,resources=r'/*')
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    if test_config is None:
        # load the instance config , if it exists ,when not testing
        app.config.from_pyfile('config.py',silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import client
    app.register_blueprint(client.bp)

    from . import car
    app.register_blueprint(car.bp)

    from . import staff
    app.register_blueprint(staff.bp)

    from . import order
    app.register_blueprint(order.bp)

    from . import project
    app.register_blueprint(project.bp)

    from . import dispatch
    app.register_blueprint(dispatch.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import material
    app.register_blueprint(material.bp)
    
    from . import repair_material
    app.register_blueprint(repair_material.bp)

    app.add_url_rule('/', endpoint='index')

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello,World!'


    return app
        