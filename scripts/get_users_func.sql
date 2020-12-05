create or replace function get_users_history_statistics
(users_ids integer array, filters users_history_statistics_filter)
returns table(user_id integer, times_listened bigint)
as $$
declare
any_or_all char(2) := '&&';
begin
if not filters.compositions_any then any_or_all = '@>';
end if;
return query execute 
	'SELECT users.user_id, COUNT(listening_history)
   	FROM users LEFT JOIN listening_history ON users.user_id = listening_history.user_id AND
	COALESCE(users.user_id = ANY($6), true) AND
	COALESCE(listening_date >= $1, true) AND
 	COALESCE(listening_date <= $2, true)
   	GROUP BY users.user_id
   	HAVING (
		COALESCE(COUNT(listening_history) >= $3, true) AND
		COALESCE(COUNT(listening_history) <= $4, true) AND
		COALESCE(ARRAY_AGG(DISTINCT composition_id) ' || any_or_all || ' $5, true)
	)
	ORDER BY users.user_id'
	using
	filters.listening_date_from, filters.listening_date_to, filters.times_listened_from,
	filters.times_listened_to, filters.compositions_list, users_ids;
end;
$$ language plpgsql called on null input;



create or replace function get_users_compositions_rating_statistics
(users_ids integer array, filters users_rating_statistics_filter)
returns table(user_id integer, times_rated bigint, avg_rating numeric)
as $$
declare
any_or_all char(2) := '&&';
begin
if not filters.rated_ids_any then any_or_all = '@>';
end if;
return query execute
	'SELECT users.user_id, COUNT(compositions_rating), AVG(satisfied::integer) * 10
	FROM users LEFT JOIN compositions_rating ON users.user_id = compositions_rating.user_id AND
	COALESCE(users.user_id = ANY($8), true) AND
	COALESCE(rating_date >= $1, true) AND
	COALESCE(rating_date <= $2, true)
	GROUP BY users.user_id
   	HAVING (
		COALESCE(COUNT(compositions_rating) >= $3, true) AND
		COALESCE(COUNT(compositions_rating) <= $4, true) AND
		COALESCE(AVG(satisfied::integer) * 10 >= $5, true) AND
		COALESCE(AVG(satisfied::integer) * 10 <= $6, true) AND
		COALESCE(ARRAY_AGG(DISTINCT composition_id) ' || any_or_all || ' $7, true)
	)
	ORDER BY user_id'
	using filters.rating_date_from, filters.rating_date_to, filters.times_rated_from,
	filters.times_rated_to, filters.average_rating_from, filters.average_rating_to,
	filters.rated_ids_list, users_ids;
end;
$$ language plpgsql called on null input;



create or replace function get_users_albums_rating_statistics
(users_ids integer array, filters users_rating_statistics_filter)
returns table(user_id integer, times_rated bigint, avg_rating numeric)
as $$
declare
any_or_all char(2) := '&&';
begin
if not filters.rated_ids_any then any_or_all = '@>';
end if;
return query execute
	'SELECT users.user_id, COUNT(albums_rating), AVG(satisfied::integer) * 10
	FROM users LEFT JOIN albums_rating ON users.user_id = albums_rating.user_id AND
	COALESCE(users.user_id = ANY($8), true) AND
	COALESCE(rating_date >= $1, true) AND
	COALESCE(rating_date <= $2, true)
	GROUP BY users.user_id
   	HAVING (
		COALESCE(COUNT(albums_rating) >= $3, true) AND
		COALESCE(COUNT(albums_rating) <= $4, true) AND
		COALESCE(AVG(satisfied::integer) * 10 >= $5, true) AND
		COALESCE(AVG(satisfied::integer) * 10 <= $6, true) AND
		COALESCE(ARRAY_AGG(DISTINCT album_id) ' || any_or_all || ' $7, true)
	)
	ORDER BY user_id'
	using filters.rating_date_from, filters.rating_date_to, filters.times_rated_from,
	filters.times_rated_to, filters.average_rating_from, filters.average_rating_to,
	filters.rated_ids_list, users_ids;
end;
$$ language plpgsql called on null input;



create or replace function get_users_playlists_rating_statistics
(users_ids integer array, filters users_rating_statistics_filter)
returns table(user_id integer, times_rated bigint, avg_rating numeric)
as $$
declare
any_or_all char(2) := '&&';
begin
if not filters.rated_ids_any then any_or_all = '@>';
end if;
return query execute
	'SELECT users.user_id, COUNT(playlists_rating), AVG(satisfied::integer) * 10
	FROM users LEFT JOIN playlists_rating ON users.user_id = playlists_rating.user_id AND
	COALESCE(users.user_id = ANY($8), true) AND
	COALESCE(rating_date >= $1, true) AND
	COALESCE(rating_date <= $2, true)
	GROUP BY users.user_id
   	HAVING (
		COALESCE(COUNT(playlists_rating) >= $3, true) AND
		COALESCE(COUNT(playlists_rating) <= $4, true) AND
		COALESCE(AVG(satisfied::integer) * 10 >= $5, true) AND
		COALESCE(AVG(satisfied::integer) * 10 <= $6, true) AND
		COALESCE(ARRAY_AGG(DISTINCT playlist_id) ' || any_or_all || ' $7, true)
	)
	ORDER BY user_id'
	using filters.rating_date_from, filters.rating_date_to, filters.times_rated_from,
	filters.times_rated_to, filters.average_rating_from, filters.average_rating_to,
	filters.rated_ids_list, users_ids;
end;
$$ language plpgsql called on null input;



create or replace function get_users_saved_albums_statistics
(users_ids integer array, filters users_saved_collections_statistics_filter)
returns table(user_id integer, saved_number bigint)
as $$
declare
any_or_all char(2) := '&&';
begin
if not filters.saved_ids_any then any_or_all = '@>';
end if;
return query execute
	'SELECT users.user_id, COUNT(user_saved_albums)
	FROM users LEFT JOIN user_saved_albums ON users.user_id = user_saved_albums.user_id
	AND COALESCE(users.user_id = ANY($4), true)
	GROUP BY users.user_id
	HAVING (
		COALESCE(COUNT(user_saved_albums) >= $1, true) AND
		COALESCE(COUNT(user_saved_albums) <= $2, true) AND
		COALESCE(ARRAY_AGG(DISTINCT album_id) ' || any_or_all || ' $3, true)
	)
	ORDER BY user_id'
	using filters.saved_number_from, filters.saved_number_to, filters.saved_ids_list, users_ids;
end;
$$ language plpgsql called on null input;



create or replace function get_users_saved_playlists_statistics
(users_ids integer array, filters users_saved_collections_statistics_filter)
returns table(user_id integer, saved_number bigint)
as $$
declare
any_or_all char(2) := '&&';
begin
if not filters.saved_ids_any then any_or_all = '@>';
end if;
return query execute
	'SELECT users.user_id, COUNT(user_saved_plists)
	FROM users LEFT JOIN user_saved_plists ON users.user_id = user_saved_plists.user_id
	AND COALESCE(users.user_id = ANY($4), true)
	GROUP BY users.user_id
	HAVING (
		COALESCE(COUNT(user_saved_plists) >= $1, true) AND
		COALESCE(COUNT(user_saved_plists) <= $2, true) AND
		COALESCE(ARRAY_AGG(DISTINCT playlist_id) ' || any_or_all || ' $3, true)
	)
	ORDER BY user_id'
	using filters.saved_number_from, filters.saved_number_to, filters.saved_ids_list, users_ids;
end;
$$ language plpgsql called on null input;


-- orders
-- 1 - user_id
-- 2 - username
-- 3 - registration_date
-- 4 - is_active
-- 5 - full_name
-- 6 - birth_date
-- 7 - gender
-- 8 - times_listened
-- 9 - times_compositions_rated
-- 10 - compositions_average_rating
-- 11 - times_albums_rated
-- 12 - albums_average_rating
-- 13 - times_playlists_rated
-- 14 - playlists_average_rating
-- 15 - albums_saved_number
-- 16 - playlists_saved_number
-- positive - asc
-- negative - desc
create or replace function get_users
(
	users_ids integer array,
	attribute_filter users_attributes_filter,
	history_toggle boolean,
	history_filters users_history_statistics_filter,
	compositions_rating_toggle boolean,
	compositions_rating_filter users_rating_statistics_filter,
	albums_rating_toggle boolean,
	albums_rating_filter users_rating_statistics_filter,
	playlists_rating_toggle boolean,
	playlists_rating_filter users_rating_statistics_filter,
	saved_albums_toggle boolean,
	saved_albums_filter users_saved_collections_statistics_filter,
	saved_playlists_toggle boolean,
	saved_playlists_filter users_saved_collections_statistics_filter,
	pagination pagination_filter,
	orders integer array default array[1]
)
returns table
(
	user_id integer,
    username character varying(16),
    password_hash character varying(64),
    registration_date date,
    is_active boolean,
    full_name character varying(256),
    birth_date date,
    gender character varying(32),
	times_listened bigint,
	times_compositions_rated bigint,
	compositions_average_rating real,
	times_albums_rated bigint,
	albums_average_rating real,
	times_playlists_rated bigint,
	playlists_average_rating real,
	albums_saved_number bigint,
	playlists_saved_number bigint
)
as $$
declare
hist_join text := '(select null::int, null::bigint as times_listened) comp_hist on true';
comp_rate_join text := '(select null::int, null::bigint as times_rated, null::numeric as avg_rating) comp_rate on true';
album_rate_join text := '(select null::int, null::bigint as times_rated, null::numeric as avg_rating) album_rate on true';
plist_rate_join text := '(select null::int, null::bigint as times_rated, null::numeric as avg_rating) plist_rate on true';
saved_albums_join text := '(select null::int, null::bigint as saved_number) album_saved on true';
saved_plists_join text := '(select null::int, null::bigint as saved_number) plist_saved on true';
full_name_search_mode text := ' OR full_name IS NULL';
birth_search_mode text := ' OR birth_date IS NULL';
genders_search_mode text := ' OR users.gender_id IS NULL';
orders_text text := '';
orders_types constant text array := array[
	'user_id',
    'username',
    'registration_date',
    'is_active',
    'full_name',
    'birth_date',
    'genders.name',
    'comp_hist.times_listened',
    'comp_rate.times_rated',
    'compositions_average_rating',
    'album_rate.times_rated',
    'albums_average_rating',
    'plist_rate.times_rated',
    'playlists_average_rating',
    'album_saved.saved_number',
    'plist_saved.saved_number'
];
order_type integer;
genders_ids integer array := null;
gender_temp varchar(32);
begin
if history_toggle then
hist_join := 'get_users_history_statistics($15, $9) AS comp_hist ON users.user_id = comp_hist.user_id';
end if;
if compositions_rating_toggle then
comp_rate_join := 'get_users_compositions_rating_statistics($15, $10) AS comp_rate ON users.user_id = comp_rate.user_id';
end if;
if albums_rating_toggle then
album_rate_join := 'get_users_albums_rating_statistics($15, $12) AS album_rate ON users.user_id = album_rate.user_id';
end if;
if playlists_rating_toggle then
plist_rate_join := 'get_users_playlists_rating_statistics($15, $11) AS plist_rate ON users.user_id = plist_rate.user_id';
end if;
if saved_albums_toggle then
saved_albums_join := 'get_users_saved_albums_statistics($15, $13) AS album_saved ON users.user_id = album_saved.user_id';
end if;
if saved_playlists_toggle then
saved_plists_join := 'get_users_saved_playlists_statistics($15, $14) AS plist_saved ON users.user_id = plist_saved.user_id';
end if;

if attribute_filter.full_name_exclude_nulls then
full_name_search_mode := ' AND full_name IS NOT NULL';
end if;
if attribute_filter.birth_exclude_nulls then
birth_search_mode := ' AND birth_date IS NOT NULL';
end if;
if attribute_filter.gender_exclude_nulls then
genders_search_mode := ' AND users.gender_id IS NOT NULL';
end if;

if array_length(orders, 1) = 0 then
	raise exception 'orders can not be empty';
end if;
foreach order_type in array orders
loop
	if order_type = 0 or abs(order_type) > 16 then
		raise exception 'invalid order type value %', order_type;
	end if;
	if order_type > 0 then
		orders_text := orders_text || orders_types[abs(order_type)] || ' ASC, ';
	else
		orders_text := orders_text || orders_types[abs(order_type)] || ' DESC, ';
	end if;
end loop;
orders_text := rtrim(orders_text, ', ');

if attribute_filter.genders is not null and array_length(attribute_filter.genders, 1) != 0 then
	--genders_ids := array[];
	foreach gender_temp in array attribute_filter.genders
	loop
		if gender_temp = 'male' then genders_ids := genders_ids || 1;
		elsif gender_temp = 'female' then genders_ids := genders_ids || 2;
		elsif gender_temp = 'other' then genders_ids := genders_ids || 3;
		else raise exception 'Invalid gender - %',  gender_temp;
		end if;
	end loop;
end if;

return query execute
	'SELECT users.user_id, users.username, users.password_hash,
	users.registration_date, users.is_active, users.full_name,
	users.birth_date, genders.name,
	comp_hist.times_listened, comp_rate.times_rated, round(comp_rate.avg_rating, 2)::real as compositions_average_rating,
	album_rate.times_rated, round(album_rate.avg_rating, 2)::real as albums_average_rating,
	plist_rate.times_rated, round(plist_rate.avg_rating, 2)::real as playlists_average_rating,
	album_saved.saved_number, plist_saved.saved_number
	FROM users
	LEFT JOIN genders ON users.gender_id = genders.gender_id
	INNER JOIN ' || hist_join || '
	INNER JOIN ' || comp_rate_join || '
	INNER JOIN ' || album_rate_join || '
	INNER JOIN ' || plist_rate_join || '
	INNER JOIN ' || saved_albums_join || '
	INNER JOIN ' || saved_plists_join || '
	WHERE
	COALESCE(users.user_id = ANY($15), true) AND
	COALESCE(username LIKE ''%%''||$1||''%%'', true) AND
	COALESCE(full_name LIKE ''%%''||$2||''%%'''|| full_name_search_mode ||', true) AND
	COALESCE(registration_date >= $3, true) AND
	COALESCE(registration_date <= $4, true) AND
	COALESCE(birth_date >= $5'|| birth_search_mode ||', true) AND
	COALESCE(birth_date <= $6'|| birth_search_mode ||', true) AND
	COALESCE(users.gender_id = ANY($7)'|| genders_search_mode ||', true) AND
	COALESCE(is_active = $8, true)
	ORDER BY '|| orders_text ||'
	OFFSET $16 LIMIT $17'
	using attribute_filter.username, attribute_filter.full_name,
	attribute_filter.registration_from, attribute_filter.registration_to,
	attribute_filter.birth_from, attribute_filter.birth_to,
	genders_ids, attribute_filter.is_active,
	history_filters, compositions_rating_filter,
	albums_rating_filter, playlists_rating_filter,
	saved_albums_filter, saved_playlists_filter,
	users_ids, pagination.offset_count, pagination.page_size;
end;
$$ language plpgsql called on null input;

select * from get_users( null,
	row(null, false, null, null, null, false, null, null, false, null, null),
	true,
	row(null, null, null, null, null, null),
	true,
	row(null, null, null, null, null, null, null, null),
	true,
	row(null, null, null, null, null, null, null, null),
	true,
	row(null, null, null, null, null, null, null, null),
	true,
	row(null, null, null, null),
	true,
	row(null, null, null, null),
	row(null, null),
	--array[7, -3, 9]
	array[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
);