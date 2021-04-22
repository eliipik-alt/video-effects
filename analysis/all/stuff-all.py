import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime
import re

df = pd.read_csv('allbugs.csv')

time_to_resolve_list = []
time_from_video_resolve_list = []
product_list = []
component_list = []
platform_list = []
os_list = []
priority_list = []
severity_list = []
status_list = []
assignee_list = []
reporter_list = []
flags_list = []
version_list = []
qa_contact_list = []
duplicates_list = []
classification_list = []
is_confirmed_list = []
cc_list = []
votes_list = []
comment_count_list = []
is_creator_accessible_list = []
is_open_list = []
year_list = []
id_list = []

Bug_ID = df['0']

for id in Bug_ID:
	try:
		print(id)    
		id = int(id)    
		URL = "https://bugzilla.mozilla.org/rest/bug/" + format(id)
		page = requests.get(URL)
		x = page.json()
		bugs = x["bugs"]

		temp = bugs[0]["creation_time"]
		match = re.search(r'\d{4}-\d{2}-\d{2}', temp)
		time = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
		year = time.strftime('%Y')
	# 	print(year)    
		year_list.append(year)
	    
		opened = datetime.datetime.strptime(temp,"%Y-%m-%dT%H:%M:%SZ")

		temp = bugs[0]["cf_last_resolved"]
		if(temp):
			closed = datetime.datetime.strptime(temp,"%Y-%m-%dT%H:%M:%SZ")

			time_to_resolve = closed - opened
			print(time_to_resolve.days)

			time_to_resolve_list.append(time_to_resolve.days)
	        
		else:
			time_to_resolve_list.append(-1)      


		product = bugs[0]["product"]

		component = bugs[0]["component"]

		platform = bugs[0]["platform"]

		os = bugs[0]["op_sys"]

		priority = bugs[0]["priority"]

		severity = bugs[0]["severity"]
		
		status = bugs[0]["status"]

		resolution = bugs[0]["resolution"]

		assignee = bugs[0]["assigned_to"]
		
		reporter = bugs[0]["creator"]

		flags = bugs[0]["flags"]
		version = bugs[0]["version"]
		qa_contact = bugs[0]["qa_contact"]
		duplicates = bugs[0]["duplicates"]
		classification = bugs[0]["classification"]
		is_confirmed = bugs[0]["is_confirmed"]
		cc = bugs[0]["cc"]
		votes = bugs[0]["votes"]
		comment_count = bugs[0]["comment_count"]
		is_creator_accessible = bugs[0]["is_creator_accessible"]
		is_open = bugs[0]["is_open"]

		id_list.append(id)
		product_list.append(product)
		component_list.append(component)
		platform_list.append(platform)
		os_list.append(os)
		priority_list.append(priority)
		severity_list.append(severity)
		status_list.append(status)
		assignee_list.append(assignee)
		reporter_list.append(reporter)
		flags_list.append(flags)
		version_list.append(version)
		qa_contact_list.append(qa_contact)
		duplicates_list.append(len(duplicates))
		classification_list.append(classification)
		is_confirmed_list.append(is_confirmed)
		cc_list.append(len(cc))
		votes_list.append(votes)
		comment_count_list.append(comment_count)
		is_creator_accessible_list.append(is_creator_accessible)
		is_open_list.append(is_open)

	except:
		pass

	# print(product,
	# 	component,
	# 	platform,
	# 	os,
	# 	priority,
	# 	severity,
	# 	status,
	# 	assignee,
	# 	reporter,
	# 	flags,
	# 	version,
	# 	qa_contact,
	# 	duplicates,
	# 	classification,
	# 	is_confirmed,
	# 	cc,
	# 	votes,
	# 	comment_count,
	# 	is_creator_accessible,
	# 	is_open)


df = pd.DataFrame({
    'year': year_list,
    'bug_id': id_list,
    'time_to_resolve': time_to_resolve_list,
    'time_from_video_to_resolve': time_from_video_resolve_list,
    'product': product_list,
    'component': component_list,
    'platform': platform_list,
    'os': os_list,
    'priority': priority,
    'severity': severity,
    'status': status_list,
    'assignee': assignee_list,
    'reporter': reporter_list,
    'flags': flags_list,
	'version': version_list,
	'qa_contact': qa_contact_list,
	'no_of_duplicates': duplicates_list,
	'classification': classification_list,
	'is_confirmed': is_confirmed_list,
	'no_of_cc': cc_list,
	'votes': votes_list,
	'comment_count': comment_count_list,
	'is_creator_accessible': is_creator_accessible_list,
	'is_open': is_open_list
})

df.to_csv("test.csv")

