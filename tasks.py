from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_celery import make_celery
from flask_mail import Mail,Message
import os
import pdfkit

app =Flask(__name__)

#DATABASE
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
class User(db.Model):
    username = db.Column(db.String(50),primary_key=True)
    email = db.Column(db.String(50))


#CELERY
app.config['CELERY_BROKER_URL'] = 'amqp://172.17.0.2//'
celery = make_celery(app)

# MAIL
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'flask@example.com'

mail = Mail(app)


@app.route('/<user>/<location>')
def send_pdf(user,location):
    send.delay(user,location)
    return 'Generatd pdf and sent'

@celery.task(name='tasks.send')
def send(user,location):
    user = User.query.filter_by(username=user).one()
    rendered = render_template('pdf_template.html',user=user,location=location)
    pdf = pdfkit.from_string(rendered,False)

    msg = Message('Hello from Flask',recipients=[user.email])
    msg.attach('result.pdf', 'application/pdf',pdf)
    msg.body = 'This is a test email sent from a background Celery task.'
    mail.send(msg)


# @app.route('/process/<int:num>',methods=['GET'])
# def process(num):
#     prime.delay(num)
#
#     return 'Async Task'
#
# @celery.task(name='tasks.prime')
# def prime(num):
#     time.sleep(10)
#     if num % 2 == 0 or num < 2:
#         return False
#     elif num ==2 or num ==3:
#         return True
#
#     for i in range(3,int(num**0.5)+1,2): #only odd numbers
#         if num % i == 0:
#             return False
#     return True

if __name__ == '__main__':
    app.run(debug=True)
