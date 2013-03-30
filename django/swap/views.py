from django.http import HttpResponse
from django.shortcuts import render_to_response
# import casclient
import traceback

def index(request):
	return render_to_response("index.html")

# def index(request):
# 	C = casclient.CASClient()
# 	try:
#  		netid = C.Authenticate()
# 	except:
# 		tb = traceback.format_exc()
# 		return HttpResponse(tb)
# 	return HttpResponse(netid)