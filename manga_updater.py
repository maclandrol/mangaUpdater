"""
Copyright (C) 2014 Emmanuel Noutahi
Please don't change the original Copyright when you modify the program

"""

from urllib2 import  Request, urlopen
import sqlite3 as lite
import os.path, getopt, sys, json,smtplib
from pprint import pprint


api_base = "https://www.mangaeden.com/api/"
img_base = "http://cdn.mangaeden.com/mangasimg/"
base_dir = os.path.expanduser("~/Mangas/") #manga directory
data_dir = os.path.expanduser("~/.mangas/") #directory for private data
table ="myMangas" #manga table name
my_mail="emmanuel.noutahi@gmail.com" #mail to receive notification


def update_manga_list():
	'''update current manga_list and save to data_dir, this take some time'''
	d= os.path.dirname(data_dir)
	if not os.path.exists(d):
		os.makedirs(data_dir)

	jsonfile=data_dir+"manga_list.json"
	if not os.path.exists(jsonfile):
		manga_list= getJson(api_base+"list/0/")
		with open(data_dir+"manga_list.json", 'w+') as file:
			json.dump(manga_list, file)


def sendmail(update_infos,email=my_mail):
	'''send notification mail'''
	try:
		sender= 'manga_updater@fakemail.com'
		dest_list=[email]
		dest=", ".join(dest_list)
		text='This Mangas have been updated, please check them soon ! : \n\n'
		for info in update_infos:
			text+="Name: %s\tlast_chapter: %s\tpath: %s\n"%(info[0],info[1],info[2])
		message="From: %s\nTo: %s\nSubject: %s\n\n%s" %(sender, dest , "Manga Updates", text)
		server=smtplib.SMTP('gmail-smtp-in.l.google.com', 25)
		server.ehlo()
		server.starttls()
		server.sendmail(sender, dest, message)
		server.quit()
	except:
		print "Notification not send! You should use a gmail account to receive notification"


def pushbullet(apikey, device=None):pass


def update_manga(manga_id=None, get_current_chap=0, notify=None):
	'''Update the list of manga i'm following and download the latest release if possible.
	with get_current_chap,  get the current chapter and save to a directory named 'latest
	with notify, send notification using a function '''
	con= lite.connect(data_dir+"mangas.db")
	manga_updated=[]
	with con:
		cur=con.cursor()
		sql_req = "SELECT UniqId, Last_Chapter, Chap_Dir, Title FROM "+table+" WHERE Follow=%i"%True
		if manga_id:
			sql_req= sql_req+"and UniqId=%s"%manga_id;
		cur.execute(sql_req)
		manga_resp=cur.fetchall()
		for manga in manga_resp:
			manga_dir=manga[2]+"%i/"%(manga[1]+1)
			chapter_id= get_manga_chapter_id(manga[0], chapter=manga[1]+1)
			success=save_chapter_to(manga_dir, get_chapter_info(chapter_id))
			
			if(success):
				cur.execute("UPDATE "+table+" SET Last_Chapter=%i, Tot_Chapter=%i, Last_Chapter_Date=datetime('now') WHERE UniqId='%s'" %(manga[1]+1, manga[1]+1, manga[0]))
				manga_updated.append([manga[3], manga[1]+1, manga[2]])

			if(get_current_chap==1 and not os.path.exists(manga[2]+"%i/"%(manga[1]))):
				save_chapter_to(manga[2]+"%i/"%(manga[1]), get_chapter_info(get_manga_chapter_id(manga[0], chapter=manga[1])))

		con.commit()
	if(manga_updated and notify):
		notify(manga_updated)

def download_manga(manga_id, manga_base_dir, chap_start=1, chap_end=None):
	'''download manga with id 'manga_id' from chap_start to chap_end and save to manga_base_dir'''
	success=True
	while(success and ((chap_end and chap_start and chap_start<chap_end) or (not chap_end))):
		chapter_id= get_manga_chapter_id(manga_id, chapter=chap_start)
		
		if(not chap_start):
			chap_d="latest/"
		else:
			chap_d="%i/"%chap_start
			chap_start+=1;

		success=save_chapter_to(manga_base_dir+chap_d, get_chapter_info(chapter_id))


def get_manga_info(manga_id):
	'''return manga info in a tuple (for insertion in database)'''

	manga_json=getJson(api_base+"manga/"+manga_id)
	title= manga_json["title"]
	artist=manga_json["artist"]
	author= manga_json["author"]
	tot_chapter= manga_json["chapters_len"]
	last_chapter=0
	chapters= manga_json["chapters"]
	if(len(chapters)>0):
		last_chapter=chapters[0][0]
	image=img_base+manga_json["image"]
	last_update= manga_json["last_chapter_date"]
	years=0
	if(manga_json["released"]):
		years=manga_json["released"]
	summary= manga_json["description"]

	manga=(manga_id, title, author, artist, summary, int(years), image, '%i'%last_update, last_chapter, tot_chapter)
	return manga


def search_manga(manga_name, best_match=1):
	'''search manga  and return only best_match or all match'''
	matching_manga=[]
	max_hit_pos=-1
	max_hit=-1
	with open(data_dir+"manga_list.json") as json_data:
		manga_json=json.load(json_data)
		manga_list= manga_json["manga"]
		i=0;
		for manga in manga_list:
			if (manga_name.lower() in manga["a"].lower()) or  (manga_name.lower() in manga["t"].lower()):
				matching_manga.append(manga)
				if(manga["h"]>max_hit):
					max_hit_pos=i
					max_hit=manga["h"]
				i+=1

	if(max_hit>=0 and best_match): return [matching_manga[max_hit_pos]]
	return matching_manga


def add_manga(manga_info=None, manga_id=None):
	'''add_manga to database'''
	con= lite.connect(data_dir+"mangas.db")
	if manga_info is None and manga_id is not None:
		manga_info=get_manga_info(manga_id)

	chap_dir=base_dir+manga_info[1]+"/"
	if not os.path.exists(chap_dir):
		os.makedirs(chap_dir)
	with con:
		cur= con.cursor()
		if( not table_exists(table_name=table, cur=cur)):
			cur.execute("CREATE TABLE "+table+"(UniqId TEXT primary key not null, Title TEXT , Author TEXT, Artist TEXT, Summary TEXT, Years INT, Image TEXT, Last_Chapter_Date DATETIME, Last_Chapter INT, Tot_Chapter INT, Follow BOOLEAN, Chap_Dir TEXT)")
		cur.execute("INSERT OR IGNORE INTO "+table+" VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", manga_info+(True, chap_dir,))
		con.commit()
		print manga_info[1], "inserted at position:", cur.lastrowid



def get_manga_chapter_id(manga_id, chapter=None):
	'''Get manga chapter id '''
	manga_json= getJson(api_base+"manga/"+manga_id)
	chapter_id=None
	if(manga_json):
		chapters= manga_json["chapters"]
		if chapter is None:
			try:
				chapter=chapters[0][0]
			except:
				chapter=0
				print "Chapter not found!!! "

		for chapt in chapters:
			
			if chapter== chapt[0]:
				chapter_id=chapt[3]
				break;
	return chapter_id



def get_chapter_info(chapter_id):
	'''Get chapter informations (images) in json format'''
	chapter_json=None
	if(chapter_id is not None):
		chapter_json=getJson(api_base+"chapter/"+chapter_id)

	return chapter_json


def save_chapter_to(dir_name, chapter_json):
	'''Save the chapter into dir_name'''
	success=False
	if(chapter_json):
		if(dir_name is None):
			dir_name=""
		if not os.path.exists(dir_name):# and os.access(dir_name, os.W_OK):
			os.makedirs(dir_name)
		images= chapter_json["images"]
		for image in images:
			ext=image[1].split('.')[1]
			with open(dir_name+str(image[0])+"."+ext, "w+") as pic:
				pic.write(urlopen(img_base+image[1]).read())
			success=True
	return success


def delete_from_database(manga_id):
	'''delete manga from database'''
	con= lite.connect(data_dir+"mangas.db")
	with con:
		cur=con.cursor()
		cur.execute("DELETE FROM "+table+" WHERE UniqId=manga_id")
		con.commit()


def table_exists(table_name=None, cur=None ):
	'''check if table exists'''
	sql="SELECT * FROM sqlite_master WHERE name ='%s' and type='table'"%table_name 
	cur.execute(sql)
	response=cur.fetchall()
	return True if len(response)>0 else False


def unfollow_manga(manga_id):
	'''Do not update this manga anymore'''
	con=lite.connect(data_dir+"mangas.db")
	with con:
		cur=con.cursor();
		cur.execute("UPDATE "+table+"  SET Follow= %r WHERE UniqId=%s"%(False, manga_id));
		con.commit()


def getJson(link):
	'''get json from link'''
	headers = {"Accept": "application/json"}
	request = Request(link, headers=headers)
	response=urlopen(request).read()
	return json.loads(response)


def add_manga_list(my_list):
	'''add this list of manga to my database'''
	for manga_name in my_list:
		search_res= search_manga(manga_name, best_match=1)
		if(search_res):
			add_manga(manga_id=search_res[0]["i"])



if __name__ == '__main__':
	
	"""update my manga list, you can run this every weeks"""
	#update_manga_list()
	
	"""connect to database and drop table in order to create a new later"""
	#con=lite.connect(data_dir+"mangas.db")
	#with con:
	#	cur=con.cursor();
	#	cur.execute("DROP TABLE IF EXISTS "+table)
	#	con.commit()

	"""Add this list of manga into database, please don't discuss my manga taste"""
	#my_manga_list=['vinland saga', 'hunter x hunter', 'naruto', 'onepunch', 'one piece', 'bleach', 'ao no exorcist', 'd.gray', 'noblesse', 'feng shen ji','gamble fish', 'illegal rare', 'jojorion', 'the gamer', 'darwin', 'tower of god', 'katana', 'tokyo ghoul', 'shingeki no kyojin','iron knight', 'koe no katachi','horimiya','wallman', 'orange-takano','dragons rioting']
	#add_manga_list(my_manga_list)

	"""Update any manga in the current database and send me notification when done if new chapters are availables"""
	update_manga(get_current_chap=0, notify=sendmail)
