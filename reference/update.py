import sectionswap.settings
from django.core.management import setup_environ
setup_environ(sectionswap.settings)

from swap.models import Course, Section, Entry
# import pounce.log as log
import urllib2
from bs4 import BeautifulSoup

def updateCourse(course):
# 	log.log("Updating %s" % str(course))
		
 	url = "https://registrar.princeton.edu/course-offerings/course_details.xml?courseid={}&term=1142".format(course.number)
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)
	
	rows = soup.find_all('tr')[1:]
	for row in rows:
			fields = row.find_all('td')
			
			classNumber = fields[0].get_text().strip()
			if not classNumber:
				continue
			print classNumber
				
			section, created = Section.objects.get_or_create(number=classNumber, course=course)
			section.name = fields[1].get_text().strip()
			section.time = fields[2].get_text().strip().replace("\n", "")
			section.days = fields[3].get_text().strip().replace("\n", "")
			raw = fields[5].get_text().replace("\n","").replace(" ","")
			sindex = raw.find("Enrolled:")
			eindex = raw.find("Limit:")
			section.enroll = int(raw[sindex+9:eindex])
			section.max = int(raw[eindex+6:] or 1000)
			
			isClosed = fields[6].get_text().strip() == "Closed"
			if not isClosed:
				print "Section %s is now open!" % str(classNumber)
# 				for subscription in Subscription.objects.filter(section=section, active=True):
# 					log.log("Sending subscription %s." % str(subscription))
# 					subscription.sendNotification()
# 					subscription.active = False
# 					subscription.save()
					
			section.isClosed = isClosed
			
			section.save()
				
def scrape():	
	# Gets the main page of all classes
	url = "https://registrar.princeton.edu/course-offerings/search_results.xml?submit=Search&term=1142"
	
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)

	# Iterates through all courses
	rows = soup.find_all('tr')[1:]
	for row in rows:
			fields = row.find_all('td')

			if (fields[10].get_text().strip() == "Cancelled"):
				continue

			courseNumber = fields[1].a['href'][28:34]
			section = fields[4].get_text().strip()
			enroll = int(fields[8].get_text().strip())
			closed = fields[10].get_text().strip() == "Closed"
						
			entry, created = Entry.objects.get_or_create(courseNumber=courseNumber, section=section)
 			if created or enroll != entry.totalEnroll or closed != entry.totalClosed:
				entry.totalEnroll = enroll
				entry.totalClosed = closed
				entry.save()

				course, created = Course.objects.get_or_create(number=courseNumber)
				course.code = ' / '.join([code.strip().replace("  ", " ") for code in fields[1].text.split('\n \n')])
				course.name = fields[2].text.strip()
				course.save()
 				updateCourse(course)
 	
# TODO: CACHING

#  	list = CoursesList.objects.all()[0]
#  	list.cache()
 	
# log.log('Running update.py')
#  
# if (len(CoursesList.objects.all()) == 0):
# 	CoursesList().save()

scrape()