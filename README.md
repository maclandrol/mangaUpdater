mangaUpdater
============

### Automatic manga downloader and updater. Use the updater with a crontab for better result.

1. #### What can it do ?

  * ##### Search a manga by name
     * mangaU -s [name] [--bestmatch]
     * mangaU --search [name] [--bestmatch]

     The name is optionnal. The next screen will ask it if you didn't set it.
	
     ![screenshot 1](https://raw.githubusercontent.com/maclandrol/mangaUpdater/master/tests/screenshots/Screenshot%20from%202015-01-24%2003:15:03.png)
	
     In the following example. we search "naruto"
	
     ![screenshot 1](https://raw.githubusercontent.com/maclandrol/mangaUpdater/master/tests/screenshots/Screenshot%20from%202015-01-24%2003:15:16.png)
	
     
     Got 3 results, Your screen should display the title and the popularity (*hits*) of those results. Result with higher hits are the bestmatch (you're likely searching for those).
	
     ![screenshot 1](https://raw.githubusercontent.com/maclandrol/mangaUpdater/master/tests/screenshots/Screenshot%20from%202015-01-24%2003:15:31.png)
	
     When you choose your result, another screen with infos and options will be displayed according to the status of the manga (if it's in your database or not ...)
	
     Common options are :
       + **Download** will binge download a manga. (You will specify start and end)
       + **Save** will save the manga to your database and update new chapter when update is called 
       + **Follow** by default any new added manga is set to follow.  
       + **Unfollow** if you unfollow a manga, it will be kept in your database but won't be updated. 
       + **Update** update only this manga (not the entire database). 
       + **Delete** delete this crap from my database. 
       + **Location** answer to "where the fuck are you saving my downloads ?" 
       + **reddit-RT** Not implemented 
       + **New Search** Perform a new search 

	
  * ##### Update current search database (could take time!)
    * mangaU -U
    * mangaU --updatelist

  * ##### Update mangas in the database. Only manga you set to "follow" will be updated. This will download any new chapters and update informations !
    * mangaU --update
    
    You can add this in your crontab file to update your manga every 12h for example. Notification on any new update will be sent by pushbullet if you enable it (I'm not sure if the notification by simple mail is working, I got a network error while testing it, so let me know).

  * ##### Show list of active manga
    * mangaU --show
    * mangaU --t
    
    This show the mangas in your database and their status.

  * ##### Drop everything
    * mangaU --droptable
    * mangaU -d

    Drop every mangas in the database. If you call `mangaU -t` you shouldn't see anything.

  * ##### Batch add of manga by title
    * mangaU --add filename
    * mangaU -a filename

    Search and add manga from filename into your database (one manga title per line). The bestmatch will be used. When there is no match, the manga will be skipped.

2. #### Installation
    
  Clone the github repository or download the tarball. Then run `python setup.py install`.

3. #### Parameters

  Setup your parameters in the _**parameters.py**_ file. The default parameters are already ok and it's really straight forward.
  If you use pushbullet, setup your device name and your api-key in order to enable notification by pushbullet when your manga database is updated.


4. #### Requirement

  This script use the following library :
    - colorama
    - requests
    - json
    - sqlite3
