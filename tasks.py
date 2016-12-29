from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_celery import make_celery
import time
import pdfkit


#DATABASE
app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)

class User(db.Model):
    username = db.Column(db.String(50),primary_key=True)
    email = db.Column(db.String(50))


#CELERY
app.config['CELERY_BROKER_URL'] = 'amqp://172.17.0.2//'
#app.config['CELERY_BACKEND'] = 'redis://172.17.0.3'

celery = make_celery(app)

@app.route('/process/<int:num>',methods=['GET'])
def process(num):
    prime.delay(num)

    return 'Async Task'

@celery.task(name='tasks.prime')
def prime(num):
    time.sleep(10)
    if num % 2 == 0 or num < 2:
        return False
    elif num ==2 or num ==3:
        return True

    for i in range(3,int(num**0.5)+1,2): #only odd numbers
        if num % i == 0:
            return False
    return True

if __name__ == '__main__':
    app.run(debug=True)
