import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime
import re
import os
from csv import writer



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


        
f = open("comments-error.txt", "w")
f.write("errors: ")
f.close()

df = pd.read_csv('stuff-all-video.csv')



reporter_list = df[['year', 'bug_id', 'comment_count']]

string = "Attached video"

for index, row in reporter_list.iterrows():

    try:
	    row_contents = []
	    id = int(row['bug_id'])
	    print(id)
	    row_contents.append(id)
	    row_contents.append(row['year'])

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

		            comment_num = comment.find(class_="change-name")
		            txt = comment_num.get_text()
		            print(txt)
		            num = 0

		            fnd = re.findall(r'\d+', txt)
		            num_list = list(map(int, fnd))
		            if(num_list):
			            num = num_list[0]
			            print(num)

		            row_contents.append(num)
		            after = row['comment_count'] - 1 - num
		            print(after)
		            row_contents.append(after)

		
	    append_list_as_row('stuff-comments-ba.csv', row_contents)

    except Exception as e:
        print(str(e))        
        print('error with id: ', id)
        f = open("comments-error.txt", "a+")
        f.write("\n")
        f.write(format(id))
        f.write('\n')
        f.write(str(e))
        f.close()
        pass





