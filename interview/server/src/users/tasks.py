import requests
from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

@shared_task(name='sendsms')
def send_sms(mobile_number, code):
    # url = "http://api.smsapp.ir/v2/sms/send/simple"
    # payload = {'message' : code , 'sender' :'10000000002562' ,'receptor' : mobile_number}
    # headers = {'apikey': "9888",}
    # requests.post(url,data=payload,headers=headers)
    logger.info(f"{code} is sent to {mobile_number}")