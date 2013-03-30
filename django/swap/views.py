from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.db.models import Q
from swap.models import *
from django.core.mail import send_mail
import urllib2
import json
from process import process

CAS_URL = "https://fed.princeton.edu/cas/"
SERVICE = "http://localhost"

def index(request):
	return render_to_response("index.html")

def swapRequest(request):
	netid = request.GET['user']
	haveSectionNumber = request.GET['have']
	wantSectionNumbers = request.GET['want'].split(',')
	
	user, userCreated = User.objects.get_or_create(netid=netid)
	user.save()
	haveSection = Section.objects.get(number=haveSectionNumber)	
	for wantSectionNumber in wantSectionNumbers:
		wantSection = Section.objects.get(number=wantSectionNumber)
		swap, swapCreated = SwapRequest.objects.get_or_create(user=user, have=haveSection, want=wantSection)
		swap.save()
		status = process(swap)
		if not status:
			break
	return HttpResponse("All good!")

def testEmail(request):
	send_mail('test subject', 'test body', 'princetonsectionswap@gmail.com', ['ljmayer@princeton.edu'], fail_silently=False)
	return HttpResponse()

def courses(request):
# 	courseDicts = []
# 	for course in Course.objects.all().order_by('code'):
# 		sectionDicts = []
# 		sections = Section.objects.filter(course=course).filter(Q(name__startswith="P") | Q(name__startswith="C")).filter(isClosed=True).order_by('name')
# 		
# 		if len(sections) < 2:
# 			continue
# 		if len(sections.filter(name__startswith='C')) < 2 and len(sections.filter(name__startswith='P')) < 2:
# 			continue
# 		
# 		for section in sections:
# 			name = section.name + " (" + section.days + " " + section.time + ")"
# 			sectionDict = {'number' : section.number, 'name' : name}
# 			sectionDicts.append(sectionDict)
# 		code = course.code.split('/')[0].strip() # for demo purposes, keep only the first code synonym
# 		courseDict = {'code' : code, 'number' : course.number, 'sections' : sectionDicts}
# 		courseDicts.append(courseDict)
# 	coursesJson = json.dumps(courseDicts)
# 	return HttpResponse(coursesJson)
 	return render_to_response("courses.json")

# def index(request):
# 	C = casclient.CASClient()
# 	try:
#  		netid = C.Authenticate()
# 	except:
# 		tb = traceback.format_exc()
# 		return HttpResponse(tb)
# 	return HttpResponse(netid)
