WITH 
comp_hist AS 
( 
	SELECT users.user_id AS user_id, COUNT(listening_history) as times_listened 
   FROM users LEFT JOIN listening_history ON users.user_id = listening_history.user_id AND
	(listening_date >= %(comp_hist_dfom)s OR %(comp_hist_dfom)s IS NULL) AND 
 	(listening_date <= %(comp_hist_dto)s OR %(comp_hist_dto)s IS NULL) 
	WHERE 
	%(comp_hist_toggle)s  
   GROUP BY users.user_id 
   HAVING ( 
	    CASE 
		WHEN %(comp_hist_clist_any)s AND %(comp_hist_clist)s IS NOT NULL THEN 
			ARRAY_AGG(DISTINCT composition_id) && %(comp_hist_clist)s 
		WHEN %(comp_hist_clist_any)s THEN
           COALESCE(ARRAY_AGG(DISTINCT composition_id) && %(comp_hist_clist)s, true)
		WHEN NOT %(comp_hist_clist_any)s AND %(comp_hist_clist)s IS NOT NULL THEN 
			ARRAY_AGG(DISTINCT composition_id) @> %(comp_hist_clist)s 
		ELSE true 
		END AND 
		(COUNT(listening_history) >= %(comp_hist_nfrom)s OR %(comp_hist_nfrom)s IS NULL) AND 
		(COUNT(listening_history) <= %(comp_hist_nto)s OR %(comp_hist_nto)s IS NULL) 
	) 
)
comp_rate AS 
(
	SELECT users.user_id AS user_id, COUNT(compositions_rating) as times_rated, AVG(satisfied::integer) * 10 AS avg_rating
	FROM users LEFT JOIN compositions_rating ON users.user_id = compositions_rating.user_id 
	WHERE 
	%(comp_rate_toggle)s AND 
	(rating_date >= %(comp_rate_dfrom)s OR %(comp_rate_dfrom)s IS NULL) AND 
	(rating_date <= %(comp_rate_dto)s OR %(comp_rate_dto)s IS NULL) 
	GROUP BY users.user_id 
   HAVING (
		CASE 
		WHEN %(comp_rate_rlist_any)s AND %(comp_rate_rlist)s IS NOT NULL THEN 
			ARRAY_AGG(DISTINCT composition_id) && %(comp_rate_rlist)s 
		WHEN NOT %(comp_rate_rlist_any)s AND %(comp_rate_rlist)s IS NOT NULL THEN 
			ARRAY_AGG(DISTINCT composition_id) @> %(comp_rate_rlist)s 
		ELSE true 
		END AND 
		(COUNT(compositions_rating) >= %(comp_rate_nfrom)s OR %(comp_rate_nfrom)s IS NULL) AND 
		(COUNT(compositions_rating) <= %(comp_rate_nto)s OR %(comp_rate_nto)s IS NULL) AND 
		(AVG(satisfied::integer) * 10 >= %(comp_rate_vfrom)s OR %(comp_rate_vfrom)s IS NULL) AND 
		(AVG(satisfied::integer) * 10 <= %(comp_rate_vto)s OR %(comp_rate_vto)s IS NULL) 
	) 
), 
plist_rate AS 
(
	SELECT users.user_id AS user_id, COUNT(playlists_rating) as times_rated, AVG(satisfied::integer) * 10 AS avg_rating 
	FROM users LEFT JOIN playlists_rating ON users.user_id = playlists_rating.user_id 
	WHERE 
	%(plist_rate_toggle)s AND 
	(rating_date >= %(plist_rate_dfrom)s OR %(plist_rate_dfrom)s IS NULL) AND 
	(rating_date <= %(plist_rate_dto)s OR %(plist_rate_dto)s IS NULL) 
	GROUP BY users.user_id 
   HAVING (
		CASE 
		WHEN %(plist_rate_rlist_any)s AND %(plist_rate_rlist)s IS NOT NULL THEN 
			ARRAY_AGG(DISTINCT playlist_id) && %(plist_rate_rlist)s 
		WHEN NOT %(plist_rate_rlist_any)s AND %(plist_rate_rlist)s IS NOT NULL THEN 
			ARRAY_AGG(DISTINCT playlist_id) @> %(plist_rate_rlist)s 
		ELSE true 
		END AND 
		(COUNT(playlists_rating) >= %(plist_rate_nfrom)s OR %(plist_rate_nfrom)s IS NULL) AND 
		(COUNT(playlists_rating) <= %(plist_rate_nto)s OR %(plist_rate_nto)s IS NULL) AND 
		(AVG(satisfied::integer) * 10 >= %(plist_rate_vfrom)s OR %(plist_rate_vfrom)s IS NULL) AND 
		(AVG(satisfied::integer) * 10 <= %(plist_rate_vto)s OR %(plist_rate_vto)s IS NULL) 
	) 
), 
album_rate AS 
(
	SELECT users.user_id AS user_id, COUNT(albums_rating) as times_rated, AVG(satisfied::integer) * 10 AS avg_rating 
	FROM users LEFT JOIN albums_rating ON users.user_id = albums_rating.user_id 
	WHERE 
	%(album_rate_toggle)s AND 
	(rating_date >= %(album_rate_dfrom)s OR %(album_rate_dfrom)s IS NULL) AND 
	(rating_date <= %(album_rate_dto)s OR %(album_rate_dto)s IS NULL) 
	GROUP BY users.user_id 
   HAVING (
		CASE 
		WHEN %(album_rate_rlist_any)s AND %(album_rate_rlist)s IS NOT NULL THEN 
			ARRAY_AGG(DISTINCT album_id) && %(album_rate_rlist)s 
		WHEN NOT %(album_rate_rlist_any)s AND %(album_rate_rlist)s IS NOT NULL THEN 
			ARRAY_AGG(DISTINCT album_id) @> %(album_rate_rlist)s 
		ELSE true 
		END AND 
		(COUNT(albums_rating) >= %(album_rate_nfrom)s OR %(album_rate_nfrom)s IS NULL) AND 
		(COUNT(albums_rating) <= %(album_rate_nto)s OR %(album_rate_nto)s IS NULL) AND 
		(AVG(satisfied::integer) * 10 >= %(album_rate_vfrom)s OR %(album_rate_vfrom)s IS NULL) AND 
		(AVG(satisfied::integer) * 10 <= %(album_rate_vto)s OR %(album_rate_vto)s IS NULL) 
	) 
), 
plist_saved AS 
(
	SELECT users.user_id AS user_id, COUNT(user_saved_plists) as saved_number 
	FROM users LEFT JOIN user_saved_plists ON users.user_id = user_saved_plists.user_id 
	WHERE 
	%(plist_saved_toggle)s 
	GROUP BY users.user_id 
	HAVING (
		(COUNT(user_saved_plists) >= %(plist_saved_nfrom)s OR %(plist_saved_nfrom)s IS NULL) AND 
		(COUNT(user_saved_plists) <= %(plist_saved_nto)s OR %(plist_saved_nto)s IS NULL) AND 
		CASE 
		WHEN %(plist_saved_slist_any)s AND %(plist_saved_slist)s IS NOT NULL THEN 
			ARRAY_AGG(DISTINCT playlist_id) && %(plist_saved_slist)s 
		WHEN NOT %(plist_saved_slist_any)s AND %(plist_saved_slist)s IS NOT NULL THEN 
			ARRAY_AGG(DISTINCT playlist_id) @> %(plist_saved_slist)s 
		ELSE true 
		END
	)
), 
album_saved AS 
(
	SELECT users.user_id AS user_id, COUNT(user_saved_albums) as saved_number 
	FROM users LEFT JOIN user_saved_albums ON users.user_id = user_saved_albums.user_id 
	WHERE 
	%(album_saved_toggle)s 
	GROUP BY users.user_id 
	HAVING (
		(COUNT(user_saved_albums) >= %(album_saved_nfrom)s OR %(album_saved_nfrom)s IS NULL) AND 
		(COUNT(user_saved_albums) <= %(album_saved_nto)s OR %(album_saved_nto)s IS NULL) AND 
		CASE 
		WHEN %(album_saved_slist_any)s AND %(album_saved_slist)s IS NOT NULL THEN 
			ARRAY_AGG(DISTINCT album_id) && %(album_saved_slist)s 
		WHEN NOT %(album_saved_slist_any)s AND %(album_saved_slist)s IS NOT NULL THEN 
			ARRAY_AGG(DISTINCT album_id) @> %(album_saved_slist)s 
		ELSE true 
		END
	)
)

SELECT users.*, 
	comp_hist.times_listened, 
	comp_rate.times_rated AS times_compositions_rated, 
	round(comp_rate.avg_rating, 2)::real AS compositions_average_rating, 
	plist_rate.times_rated AS times_playlists_rated, 
	round(plist_rate.avg_rating, 2)::real AS playlists_average_rating, 
	album_rate.times_rated AS times_albums_rated, 
	round(album_rate.avg_rating, 2)::real AS albums_average_rating, 
	plist_saved.saved_number as playlists_saved_number, 
	album_saved.saved_number as albums_saved_number 
FROM users 
LEFT JOIN comp_hist ON users.user_id = comp_hist.user_id 
LEFT JOIN comp_rate ON users.user_id = comp_rate.user_id 
LEFT JOIN plist_rate ON users.user_id = plist_rate.user_id 
LEFT JOIN album_rate ON users.user_id = album_rate.user_id 
LEFT JOIN plist_saved ON users.user_id = plist_saved.user_id 
LEFT JOIN album_saved ON users.user_id = album_saved.user_id 
WHERE 
(username LIKE \'%%\'||%(username)s||\'%%\' OR %(username)s IS NULL) AND 
(full_name LIKE \'%%\'||%(full_name)s||\'%%\' OR %(full_name)s IS NULL) AND 
(registration_date >= %(reg_from)s::date OR %(reg_from)s IS NULL) AND 
(registration_date <= %(reg_to)s::date OR %(reg_to)s IS NULL) AND 
(birth_date >= %(birth_from)s::date OR %(birth_from)s IS NULL) AND 
(birth_date <= %(birth_to)s::date OR %(birth_to)s IS NULL) AND 
(gender_id = ANY(%(genders)s) OR %(genders)s IS NULL) AND 
(is_active = %(is_active)s OR %(is_active)s IS NULL) AND 
( NOT %(comp_hist_toggle)s OR EXISTS ( 
	SELECT user_id FROM comp_hist 
 	WHERE users.user_id = comp_hist.user_id 
	) 
) AND 
( NOT %(comp_rate_toggle)s OR EXISTS ( 
	SELECT user_id FROM comp_rate 
	WHERE users.user_id = comp_rate.user_id 
	) 
) AND
( NOT %(plist_rate_toggle)s OR EXISTS ( 
	SELECT user_id FROM plist_rate 
 	WHERE users.user_id = plist_rate.user_id 
	) 
) AND 
( NOT %(album_rate_toggle)s OR EXISTS ( 
	SELECT user_id FROM album_rate 
 	WHERE users.user_id = album_rate.user_id 
	) 
) AND 
( NOT %(plist_saved_toggle)s OR EXISTS (
	SELECT user_id FROM plist_saved 
 	WHERE users.user_id = plist_saved.user_id 
	)
) AND 
( NOT %(album_saved_toggle)s OR EXISTS (
	SELECT user_id FROM album_saved 
 	WHERE users.user_id = album_saved.user_id 
	)
)
ORDER BY user_id ASC