mangaUpdater
============

### Automatic manga downloader and updater. Work better with a scheduler like crontab for manga updating.

1. #### Basics functions

	* ##### Search a manga by name (**search_manga**) 
		
		* Optional argument: best_match. If best_match is set to 1, only the manga with the best hit is returned (use it with popular manga)

	* ##### Get a manga info using a manga_id obtained with search manga (**get_manga_info**)
		
		* example: get_manga_info

	* ##### Update/Create if not exists my local manga list (**update_manga_list**). This could take some time!
		
		* Save manga_list to base_dir

	* ##### Get a chapter id for a manga (**get_manga_chapter_id**)
		
		* Required argument: manga_id
		* Optional argument: chapter. If chapter is set to None, the last chapter id is returned else, the id of the chapter is returned
		* Return chapter id or None

	* ##### Get chapter infos (**get_chapter_info**)
		
		* Required argument: chapter_id
		* Return a json object that contains chapter data (images)

	* ##### Save chapter to directory (**save_chapter_to**)

		* Required argument: dir_name (destination base directory)
		* Required argument: chapter_json (see **get_chapter_info**)

	* ##### Download manga chapter from chap_start to chap_end (**download_manga**)

		* Required argument: manga_id
		* Required argument: manga_base_dir
		* Optional argument: chap_start (set to 1 by default)
		* Optional argument: chap_end (set to None by default, chapters are then from chap_start to latest release)

2. #### Database related functions
	
	* ##### Add manga to my database for automatic update (**add_manga**)
		
		* Require manga_info and/or manga_id

	* ##### Add list of manga to database (**add_manga_list**)

		* Required argument: list of manga name. If the manga is found with **search_manga**, it'll be add to the database, else it'll be skipped

	* ##### Unfollow manga (**unfollow_manga**). By default, any mangas added to the database will be automatically updated when **update_manga** is called. Execute **unfollow_manga** to discard the manga.

		* Required argument: manga_id

	* ##### Update manga (**update_manga**). Automatically update any manga in the database, save the chapter to the corresponding manga directory ("*path_to_manga_dir/Manga_Title/Chapter_Num/*" and notify me if new releases are found!

		* Argument: manga_id (default value is None), if not None, only update selected manga
		* Argument: get_current_chap (default value is 0). If set to 1, retrieve current latest chapter and save to "*path_to_manga_dir/Manga_Title/latest*"
		* Argument: notify. Function for notification; By default sendmail!
