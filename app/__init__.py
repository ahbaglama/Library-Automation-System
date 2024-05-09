from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS


SWAGGER_URL="/swagger"
API_URL="/static/swagger.yaml"





def create_app():
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_pyfile('config.py')

    from .routes.users import routes_blueprint
    from .routes.main import home_blueprint


    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'Access API'
        }
    )

    @app.after_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    app.register_blueprint(home_blueprint)

    app.register_blueprint(routes_blueprint)

    return app