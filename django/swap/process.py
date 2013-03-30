from swap.models import SwapRequest
from django.core.mail import send_mail

# Don't let a user submit identical have/want request

def process(input_req):
    input_req.save()
    cycle = input_req.find_cycle()
    if cycle != None:
        netids = []
        for req in cycle:
            netids.append(req.user.netid)
        for req in cycle:
            email(req, netids)
            delete_all(req)
        return netids
    return None

def delete_all(input_req):
    for req in input_req.section.had_by_set.all():
        if req.user == input_req.user:
            req.delete()

def email(req, netids):
    email_body = 'Users involved in swap:\n'
    for netid in netids:
        email_body += netid + '\n'
    send_mail('Successful swap into' + unicode(req.want), email_body, 'from email', [req.user.netid + '@princeton.edu'], fail_silently=False)
