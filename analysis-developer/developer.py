import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime
import re



def is_dev(user_id_list):

	authors = 0
	developers = 0
	users_list = []

	# try:
	for id in user_id_list:
	
		x = "https://bugzilla.mozilla.org/user_profile?user_id=" + str(id)
		page = requests.get(x)
		soup = BeautifulSoup(page.content, 'html.parser')

		stat = soup.find_all('tr')
		num = 0
		for i in stat:
			x = i.get_text()
			x = x.replace('\n','')
			if ("Patches submitted" in x):
				num = int(re.search(r'\d+', x).group())
				if(num>0):
					developers +=1
					users_list.append('developer')
				else:
					authors +=1
					users_list.append('non-developer')
	# except:
	# 	pass


	return users_list, developers, authors




df = pd.read_csv('stuff-video-part1.csv')

# year,bug_id,time_to_resolve,time_from_video_to_resolve,product,component,platform,os,priority,severity,status,
# assignee,reporter,flags,version,qa_contact,no_of_duplicates,classification,is_confirmed,no_of_cc,votes,
# comment_count,is_creator_accessible,is_open


		

user_id_list = [] 
year_list = [] 
bug_id_list = [] 

reporter_list = df[['year', 'bug_id', 'reporter']]


for index, row in reporter_list.iterrows():
	# print(row['year'], row['bug_id'])

	try:
		reporter = row['reporter']
		URL = "https://bugzilla.mozilla.org/rest/user?names=" + reporter
		page = requests.get(URL)
		# print(page)
		x = page.json()
		bugs = x["users"]

		user_id = bugs[0]["id"]
		# print(user_id)
		user_id_list.append(user_id)	

		year_list.append(row['year']) 
		bug_id_list.append(row['bug_id'])	

	except:
		pass

df = pd.DataFrame(
	{'year': year_list,
     'bug_id': bug_id_list,
     'user_id': user_id_list
    })

df.to_csv("user-video-part1.csv")

users_list, developers, authors = is_dev(user_id_list)


f = open("result.txt", "w")
f.write("Reporters: ")
f.write(format(authors))
f.write("\nDevelopers: ")
f.write(format(developers))
f.close()
print(developers, authors)


df1 = pd.DataFrame(
	{'year': year_list,
     'bug_id': bug_id_list,
     'user_id': user_id_list,
     'developer/non-developer': users_list
    })

# df['developer/non-developer'] = pd.Series(users_list, index=df.index)
df1.to_csv("user-video-part1.csv")



