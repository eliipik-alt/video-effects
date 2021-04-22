import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime
import re
import os
from csv import writer



def find_author(link):

	try:

		x = "https://bugzilla.mozilla.org" + format(link)
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
					return 'developer'
					
				else:
					return 'end-user'
					
	except:
		return 'error'
		pass






def append_list_as_row(file_name, list_of_elem):

	if os.path.exists(file_name):
		append_write = 'a' 
	else:
		append_write = 'w' 


    # Open file in append mode
	with open(file_name, append_write, newline='') as write_obj:

        # Create a writer object from csv module
		csv_writer = writer(write_obj)

        # Add contents of list as last row in the csv file
		csv_writer.writerow(list_of_elem)


        
f = open("submitter-error.txt", "w")
f.write("errors: ")
f.close()

df = pd.read_csv('videos-ids.csv')



id_list = df['bug_id']

string = "Attached video"

for id in id_list:

    try:
	    row_contents = []
	    id = int(id)
	    print(id)
	    row_contents.append(id)

	    URL = "https://bugzilla.mozilla.org/show_bug.cgi?id=" + format(id)
	    page = requests.get(URL)
	    # print(page)
	    soup = BeautifulSoup(page.content, 'html.parser')
	    list_change = soup.find_all(class_="change-set")

	    for alist in list_change:	
	        temp = alist.find(class_="attachment") 
	        if(temp):
		        if(any(substring in temp.get_text() for substring in string)):
		            # print('video')
		            comment = alist.find(class_="comment") 
		            author = comment.find(class_="change-author")
		            # print(author)
		            a = author.find('a', href=True)
		            # print(a['href'])
		            role = author.find(class_="user-role")
		            if (role):
		            	# print(role.get_text())
		            	row_contents.append(role.get_text())
		            else:
		            	row_contents.append('no-role')


		            row_contents.append(find_author(a['href']))

		            # comment_num = comment.find(class_="change-name")
		            # row_contents.append(comment_num.get_text())

		
	    append_list_as_row('stuff-submitter.csv', row_contents)

    except Exception as e:
        print(str(e))        
        print('error with id: ', id)
        f = open("submitter-error.txt", "a+")
        f.write("\n")
        f.write(format(id))
        f.write('\n')
        f.write(str(e))
        f.close()
        pass





