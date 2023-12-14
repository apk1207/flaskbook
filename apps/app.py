from flask import Flask

# create_app 함수 생성
def create_app():

    # 플라스크(클래스)의 인스턴스(객체) 생성
    app = Flask(__name__)

    # from 폴더위치 import views as 별칭 선언
    from apps.curd import views as crud_views


    # register_blueprint
    app.register_blueprint(crud_views.curd, url_prefix="/crud")

    return app
