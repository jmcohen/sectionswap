from sectionswap.models import SwapRequest
from django.core.mail import send_mail

# Don't let a user submit identical have/want request

def process(input_req):
    input_req.save()
    cycle = input_req.find_cycle()
    if cycle != None:
        for req in cycle:
            email(req)
            req.delete()


def email(req):
    send_mail('Subject here', 'Here is the message.', 'from@example.com', ['to@example.com'], fail_silently=False)
