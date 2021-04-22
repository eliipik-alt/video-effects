import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime
import re


def time_video(soup):

	attachment = soup.find(class_="attach-time activity-ref")

	time = datetime.datetime.strptime(attachment.span['title'],"%Y-%m-%d %H:%M %Z")
	# print(time)
	# video_time_list.append(time)
	return time


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



f = open("time_to_resolve-errors.txt", "w")
f.write("errors: ")
f.close()

df = pd.read_csv('videos_all.csv')

id_list = []
year_list = []
time_to_resolve_list = []
time_to_resolve_video_list = []
# video_time_list = []
initially_submitted_list = []


Bug_ID = df['Bug_ID']

for id in Bug_ID:
	try:
		row_contents = []
		id = int(id)
		print(id)
		# id_list.append(id)
		row_contents.append(id)

		URL = "https://bugzilla.mozilla.org/show_bug.cgi?id=" + format(id)
		page = requests.get(URL)
		soup = BeautifulSoup(page.content, 'html.parser')

		video_time = time_video(soup)
		row_contents.append(video_time)

		labels = soup.find_all(class_="bug-time-label")

		for bug_time in labels:
			if "Opened" in bug_time.get_text():
				opened = datetime.datetime.strptime(bug_time.span['title'],"%Y-%m-%d %H:%M %Z")
				# print('opened:', opened)
				row_contents.append(opened)

				year = opened.year
				# year_list.append(year)
				row_contents.append(year)


				if (video_time == opened):
					# initially_submitted_list.append('yes')
					row_contents.append('yes')
				else:
					# initially_submitted_list.append('no')
					row_contents.append('no')
				continue

			if "Closed" in bug_time.get_text():
				if (datetime.datetime.strptime(bug_time.span['title'],"%Y-%m-%d %H:%M %Z")):
					closed = datetime.datetime.strptime(bug_time.span['title'],"%Y-%m-%d %H:%M %Z")
				
					time_to_resolve = closed - opened
					# time_to_resolve_list.append(time_to_resolve.days)
					row_contents.append(time_to_resolve.days)

					time_to_resolve_video = closed - video_time
					# time_to_resolve_video_list.append(time_to_resolve_video.days)
					row_contents.append(time_to_resolve_video.days)
				else:
					row_contents..append(-2)
					row_contents..append(-2)

			else:
				row_contents..append(-1)
				row_contents..append(-1)

		# row_contents.append(id)
		# row_contents.append(link)

		append_list_as_row('time_to_resolve_all.csv', row_contents)

	except:
		print('error with id: ', id)
		f = open("time_to_resolve-errors.txt", "a+")
		f.write("\n")
		f.write(format(id))
		f.close()
		pass


# print(len(time_to_resolve_list),len(time_to_resolve_video_list),
# len(initially_submitted_list))

# df = pd.DataFrame({
#     'bug_id': id_list,
#     'year': year_list,
# 	# 'video_submitted_at': video_time_list,
# 	'time_to_resolve': time_to_resolve_list,
# 	'time_to_resolve_from_video_submitted': time_to_resolve_video_list,
# 	'initially_submitted': initially_submitted_list
# })

# df.to_csv("time_to_resolve_all.csv")

