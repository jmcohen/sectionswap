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
    email_body = """
    	<p><b>Hey, there!</b></p>
    	<p>We've identified a potential swap for %s from %s into %s.</p>
    	<p>You'll swap with the following people:</p>
    	<p>%s</p>
    	<p>Cheers!</p>
    	<p>The Section Swap Team</p>
    	""" % (str(req.have.course), str(req.have.name), str(req.want.name), "</p><p>".join(netids))

    send_mail('Successful swap into ' + str(req.want), email_body, 'Section Swap<princetonsectionswap@gmail.com>', [req.user.netid + '@princeton.edu'], fail_silently=False)
    