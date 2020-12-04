create or replace function get_albums_compositions_statistics
(albums_ids integer array, filters collections_compositions_statistics_filter)
returns table(album_id integer, compositions_number bigint)
as $$
declare
any_or_all char(2) := '&&';
begin
if not filters.compositions_any then any_or_all = '@>';
end if;
return query execute
	'SELECT albums.album_id, COUNT(album_comp_links)
	FROM albums LEFT JOIN album_comp_links ON albums.album_id = album_comp_links.album_id AND
	COALESCE(albums.album_id = ANY($4), true)
	GROUP BY albums.album_id
	HAVING (
		COALESCE(COUNT(album_comp_links) >= $1, true) AND
		COALESCE(COUNT(album_comp_links) <= $2, true) AND
		COALESCE(ARRAY_AGG(DISTINCT composition_id) ' || any_or_all || ' $3, true)
	)
	ORDER BY album_id'
	using filters.compositions_number_from, filters.compositions_number_to, filters.compositions_list, albums_ids;
end;
$$ language plpgsql called on null input;



create or replace function get_albums_rating_statistics
(albums_ids integer array, filters entity_rating_statistics_filter)
returns table(album_id integer, times_rated bigint, avg_rating numeric)
as $$
declare
any_or_all char(2) := '&&';
begin
if not filters.users_ids_any then any_or_all = '@>';
end if;
return query execute
	'SELECT albums.album_id, COUNT(albums_rating), AVG(satisfied::integer) * 10
	FROM albums LEFT JOIN albums_rating ON albums.album_id = albums_rating.album_id AND
	COALESCE(albums.album_id = ANY($8), true) AND
	COALESCE(rating_date >= $1, true) AND
	COALESCE(rating_date <= $2, true)
	GROUP BY compositions.composition_id
   	HAVING (
		COALESCE(COUNT(albums_rating) >= $3, true) AND
		COALESCE(COUNT(albums_rating) <= $4, true) AND
		COALESCE(AVG(satisfied::integer) * 10 >= $5, true) AND
		COALESCE(AVG(satisfied::integer) * 10 <= $6, true) AND
		COALESCE(ARRAY_AGG(DISTINCT user_id) ' || any_or_all || ' $7, true)
	)
	ORDER BY album_id'
	using filters.rating_date_from, filters.rating_date_to, filters.times_rated_from,
	filters.times_rated_to, filters.average_rating_from, filters.average_rating_to,
	filters.users_ids_list, albums_ids;
end;
$$ language plpgsql called on null input;



create or replace function get_albums_users_statistics
(albums_ids integer array, filters collections_users_statistics_filter)
returns table(album_id integer, users_saved_number bigint)
as $$
declare
any_or_all char(2) := '&&';
begin
if not filters.users_any then any_or_all = '@>';
end if;
return query execute
	'SELECT albums.album_id, COUNT(user_saved_albums)
	FROM albums LEFT JOIN user_saved_albums ON albums.album_id = user_saved_albums.album_id
	AND COALESCE(albums.album_id = ANY($4), true)
	GROUP BY albums.album_id
	HAVING (
		COALESCE(COUNT(user_saved_albums) >= $1, true) AND
		COALESCE(COUNT(user_saved_albums) <= $2, true) AND
		COALESCE(ARRAY_AGG(DISTINCT user_id) ' || any_or_all || ' $3, true)
	)
	ORDER BY album_id'
	using filters.users_number_from, filters.users_number_to, filters.users_list, albums_ids;
end;
$$ language plpgsql called on null input;



-- orders
-- 1 - album_id
-- 2 - title
-- 3 - release_date
-- 4 - compositions_number
-- 5 - times_rated
-- 6 - average_rating
-- 7 - users_saved_number
-- positive - asc
-- negative - desc
create or replace function get_albums
(
	albums_ids integer array,
	attribute_filter albums_attributes_filter,
	compositions_toggle boolean,
	compositions_filter collections_compositions_statistics_filter,
	rating_toggle boolean,
	rating_filter entity_rating_statistics_filter,
	users_toggle boolean,
	users_filter collections_users_statistics_filter,
	pagination pagination_filter,
	orders integer array default array[1]
)
returns table
(
	albums_id integer,
    title character varying(256),
    release_year smallint,
    release_month smallint,
    release_day smallint,
	compositions_number bigint,
	times_rated bigint,
	average_rating real,
	users_saved_number bigint
)
as $$
declare
comp_join text := '(select null::int, null::bigint as compositions_number) comp on true';
rate_join text := '(select null::int, null::bigint as times_rated, null::numeric as avg_rating) rate on true';
users_join text := '(select null::int, null::bigint as users_saved_number) users on true';
release_search_mode text := ' OR release_year IS NULL';
orders_text text := '';
orders_types constant text array := array[
    'album_id',
    'title',
    'array[coalesce(release_year, 0), coalesce(release_month, 0), coalesce(release_day, 0)]',
    'comp.compositions_number',
    'rate.times_rated',
    'average_rating',
    'users.users_saved_number'
];
order_type integer;
begin

if attribute_filter.release_date_exclude_nulls then
release_search_mode := ' AND release_year IS NOT NULL';
end if;

if compositions_toggle then
comp_join := 'get_albums_compositions_statistics($7, $4) AS comp ON albums.album_id = comp.album_id';
end if;
if rating_toggle then
rate_join := 'get_albums_rating_statistics($7, $5) AS rate ON albums.album_id = rate.album_id';
end if;
if users_toggle then
users_join := 'get_albums_users_statistics($7, $6) AS users ON albums.album_id = users.album_id';
end if;

if array_length(orders, 1) = 0 then
	raise exception 'orders can not be empty';
end if;
foreach order_type in array orders
loop
	if order_type = 0 or abs(order_type) > 10 then
		raise exception 'invalid order type value %', order_type;
	end if;
	if order_type > 0 then
		orders_text := orders_text || orders_types[abs(order_type)] || ' ASC, ';
	else
		orders_text := orders_text || orders_types[abs(order_type)] || ' DESC, ';
	end if;
end loop;
orders_text := rtrim(orders_text, ', ');

return query execute
	'SELECT albums.album_id, albums.title, albums.release_year, albums.release_month, albums.release_day,
	comp.compositions_number, rate.times_rated, round(rate.avg_rating, 2)::real as average_rating, users.users_saved_number
	FROM albums
	INNER JOIN ' || comp_join || '
	INNER JOIN ' || rate_join || '
	INNER JOIN ' || users_join || '
	WHERE
	COALESCE(albums.album_id = ANY($7), true) AND
	COALESCE(albums.title LIKE ''%%''||$1||''%%'', true) AND
	COALESCE(compare_dates(release_year, release_month, release_day, $2) <= 0'|| release_search_mode ||', true) AND
	COALESCE(compare_dates(release_year, release_month, release_day, $3) >= 0'|| release_search_mode ||', true)
	ORDER BY '|| orders_text ||'
	OFFSET $8 LIMIT $9'
	using attribute_filter.title, attribute_filter.release_date_from, attribute_filter.release_date_to,
	compositions_filter, rating_filter, users_filter, albums_ids,
	pagination.offset_count, pagination.page_size;
end;
$$ language plpgsql called on null input;



select * from get_albums( null,
	row(null, false, null, null),
	true,
	row(null, null, null, null),
	true,
	row(null, null, null, null, null, null, null, null), 
	true,
	row(null, null, null, null),
	row(null, null),
	array[1, 2, 3, 4, 5, 6, 7]
)