# flask 클래스를 import한다. / render_template를 추가로 import한다.
# url_for를 추가로 import한다.
import logging
import os

from email_validator import EmailNotValidError, validate_email
from flask import (Flask, current_app, flash, g, redirect, render_template,
                   request, url_for)
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message

# 여기에서 호출하면 오류가 된다.
# print(current_app)

# flask 클래스를 인스턴스화한다.
app = Flask(__name__)

# debug toolbar를 확인할수 있는 디버그 모드로 실행하려면 아래 코드 필요
# app.debug = True
# 해당 코드 대신 flask app 실행 시 flask --debug run 으로 실행하면 디버그 모드로 실행됨

# SECRET_KEY를 추가한다.
app.config["SECRET_KEY"] = "2AZSMss3p50PbcY2hBsJ"

# Mail 클래스의 config를 추가한다
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

# flask-mail 확장을 등록한다
mail = Mail(app)


# 로그 레벨을 설정한다.
app.logger.setLevel(logging.DEBUG)

# 로그를 출력하려면 다음과 같이 지정한다
# app.logger.critical("fatal error")
# app.logger.error("error")
# app.logger.warning("warning")
# app.logger.info("info")
# app.logger.debug("debug")

# 리다이랙트를 중단하지 않도록 한다
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# DebugToolbarExtension에 애플리케이션을 설정한다
# 디버그 툴바 확장 클래스 인스턴스(객체) 생성
toolbar = DebugToolbarExtension(app)

# 애플리케익션 컨텍스트를 취득하여 스택에 push한다.
ctx = app.app_context()
ctx.push()

# current_app에 접근할 수 있게 된다.
print(current_app.name)
# >> app.minimalapp.app

# 전역 임시 영역에 값을 설정한다.
g.connection = "connection"
print(g.connection)
# >> connection


# URL과 실행할 함수를 매핑한다.
@app.route("/")
def index():
    return "Hello, Flaskbook!"


@app.route("/hello/<name>",
           methods=["GET", "POST"],
           endpoint="hello-endpoint")
def hello(name):
    return f"Hello, {name}!"


# show_name 엔드포인트를 작성한다.
@app.route("/name/<name>")
def show_name(name):
    # 변수를 템플릿 엔진에게 건넨다
    return render_template("index.html", name=name)


@app.route("/contact")
def contact():
    return render_template("contact.html")


def send_email(to, subject, template, **kwargs):
    """메일을 송신하는 함수"""
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        # form 속성을 사용해서 폼의 값을 취득한다.
        # 입력받은 값을  python 변수로 받아온다.
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        # 입력 체크
        is_valid = True

        if not username:
            flash("사용자명은 필수입니다")
            is_valid = False

        if not email:
            flash("메일 주소는 필수입니다")
            is_valid = False

        # 이메일이 유효한지 체크
        try:
            # validate_email 함수가 실행되고 메일이 유효하지 않으면 except로 이동한다.
            validate_email(email)
        except EmailNotValidError:
            flash("메일 주소의 형식으로 입력해 주세요")
            is_valid = False

        if not description:
            flash("문의 내용은 필수 입니다")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        # 이메일을 보낸다(나중에 구현할 부분)
        send_email(
            email,
            "문의 감사합니다.",
            "contact_mail",
            username=username,
            description=description,
        )
        # 문의 완료 엔드포인트로 리다이렉트한다.
        flash("문의해 주셔서 감사합니다")
        return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")


with app.test_request_context("/users?updated=true"):
    # /
    print(url_for("index"))
    # /hello/world
    print(url_for("hello-endpoint", name="world!"))
    # /name/AK?page=1
    print(url_for("show_name", name="AK", page="!"))
    # true가 출력된다.
    print(request.args.get("updated"))
