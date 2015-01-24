mangaUpdater
============

### Automatic manga downloader and updater. Use the updater with a crontab for better result.

1. #### What can it do ?

	* ##### Search a manga by name
		
		* mangaU -s [name] [--bestmatch]
		* mangaU --search [name] [--bestmatch]

	The name is optionnal. The next screen will ask it.
	
	

	* ##### Update current search database (could take time!)
		
		* mangaU -U
		* mangaU --updatelist

	* ##### Update mangas in the database. Only manga you set to "follow" will be updated. This will download any new chapters and update informations !
		
		* mangaU --update

	* ##### Show list actif list of manga
		
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

Clone the github repository or download the tarball. Then run
`python setup.py install`

3. #### Parameters

Setup your parameters in the parameters.py file. The default parameters are already ok.
If you use pushbullet, setup your device name and your api-key in order to enable notification by pushbullet when your manga database is updated.

4. #### Requirement

This script use the following library :

- colorama
- requests
- json
- sqlite3
