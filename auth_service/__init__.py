from flask import Flask
from .auth import *
from .db import *
import os


def create_app():
    app = Flask(__name__)

    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'auth.sqlite'),
    )


    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    init_app(app)

    app.register_blueprint(bp)
    return app


#if __name__ == '__main__':
#    main()
