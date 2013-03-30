from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db.models import Q
from swap.models import *
# import casclient
import traceback
import json

def index(request):
	return render_to_response("index.html")

def swapRequest(request):
	have = request.GET['have']
	want = request.GET['want']
	return HttpResponse(want)
	
def courses(request):
	courseDicts = []
	for course in Course.objects.all():
		sectionDicts = []
		sections = Section.objects.filter(course=course).filter(Q(name__startswith="P") | Q(name__startswith="C")).order_by('name')
		
		if len(sections) < 2:
			continue
		if len(sections.filter(name__startswith='L')) < 2 and len(sections.filter(name__startswith='P')) < 2:
			continue
		
		for section in sections:
			name = section.name + " (" + section.days + " " + section.time + ")"
			sectionDict = {'number' : section.number, 'name' : name}
			sectionDicts.append(sectionDict)
		courseDict = {'code' : course.code, 'number' : course.number, 'sections' : sectionDicts}
		courseDicts.append(courseDict)
	coursesJson = json.dumps(courseDicts)
	return HttpResponse(coursesJson)

# def index(request):
# 	C = casclient.CASClient()
# 	try:
#  		netid = C.Authenticate()
# 	except:
# 		tb = traceback.format_exc()
# 		return HttpResponse(tb)
# 	return HttpResponse(netid)