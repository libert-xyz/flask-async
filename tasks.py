from celery import Celery
import time
app = Celery('tasks', broker='amqp://172.17.0.2//',backend='redis://172.17.0.3')

@app.task
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
