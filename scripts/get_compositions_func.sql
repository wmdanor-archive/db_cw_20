create or replace function get_compositions_history_statistics
(compositions_ids integer array, filters compositions_history_statistics_filter)
returns table(composition_id integer, times_listened bigint)
as $$
declare
any_or_all char(2) := '&&';
begin
if not filters.users_ids_any then any_or_all = '@>';
end if;
return query execute 
	'SELECT compositions.composition_id, COUNT(listening_history)
   	FROM compositions LEFT JOIN listening_history ON compositions.composition_id = listening_history.composition_id AND
	COALESCE(compositions.composition_id = ANY($6), true) AND
	COALESCE(listening_date >= $1, true) AND
 	COALESCE(listening_date <= $2, true)
   	GROUP BY compositions.composition_id
   	HAVING (
		COALESCE(COUNT(listening_history) >= $3, true) AND
		COALESCE(COUNT(listening_history) <= $4, true) AND
		COALESCE(ARRAY_AGG(DISTINCT user_id) ' || any_or_all || ' $5, true)
	)
	ORDER BY composition_id'
	using
	filters.listening_date_from, filters.listening_date_to, filters.times_listened_from,
	filters.times_listened_to, filters.users_ids_list, compositions_ids;
end;
$$ language plpgsql called on null input;



create or replace function get_compositions_rating_statistics
(compositions_ids integer array, filters compositions_rating_statistics_filter)
returns table(composition_id integer, times_rated bigint, avg_rating numeric)
as $$
declare
any_or_all char(2) := '&&';
begin
if not filters.users_ids_any then any_or_all = '@>';
end if;
return query execute
	'SELECT compositions.composition_id, COUNT(compositions_rating), AVG(satisfied::integer) * 10
	FROM compositions LEFT JOIN compositions_rating ON compositions.composition_id = compositions_rating.composition_id AND
	COALESCE(compositions.composition_id = ANY($8), true) AND
	COALESCE(rating_date >= $1, true) AND
	COALESCE(rating_date <= $2, true)
	GROUP BY compositions.composition_id
   	HAVING (
		COALESCE(COUNT(compositions_rating) >= $3, true) AND
		COALESCE(COUNT(compositions_rating) <= $4, true) AND
		COALESCE(AVG(satisfied::integer) * 10 >= $5, true) AND
		COALESCE(AVG(satisfied::integer) * 10 <= $6, true) AND
		COALESCE(ARRAY_AGG(DISTINCT user_id) ' || any_or_all || ' $7, true)
	)
	ORDER BY composition_id'
	using filters.rating_date_from, filters.rating_date_to, filters.times_rated_from,
	filters.times_rated_to, filters.average_rating_from, filters.average_rating_to,
	filters.users_ids_list, compositions_ids;
end;
$$ language plpgsql called on null input;



create or replace function get_compositions_playlists_statistics
(compositions_ids integer array, filters compositions_collections_statistics_filter)
returns table(composition_id integer, belongs_number bigint)
as $$
declare
any_or_all char(2) := '&&';
begin
if not filters.collections_any then any_or_all = '@>';
end if;
return query execute
	'SELECT compositions.composition_id, COUNT(plist_comp_links)
	FROM compositions LEFT JOIN plist_comp_links ON compositions.composition_id = plist_comp_links.composition_id AND
	COALESCE(compositions.composition_id = ANY($4), true)
	GROUP BY compositions.composition_id
	HAVING (
		COALESCE(COUNT(plist_comp_links) >= $1, true) AND
		COALESCE(COUNT(plist_comp_links) <= $2, true) AND
		COALESCE(ARRAY_AGG(DISTINCT playlist_id) ' || any_or_all || ' $3, true)
	)
	ORDER BY composition_id'
	using filters.number_belongs_from, filters.number_belongs_to, filters.collections_list, compositions_ids;
end;
$$ language plpgsql called on null input;



create or replace function get_compositions_albums_statistics
(compositions_ids integer array, filters compositions_collections_statistics_filter)
returns table(composition_id integer, belongs_number bigint)
as $$
declare
any_or_all char(2) := '&&';
begin
if not filters.collections_any then any_or_all = '@>';
end if;
return query execute
	'SELECT compositions.composition_id, COUNT(album_comp_links)
	FROM compositions LEFT JOIN album_comp_links ON compositions.composition_id = album_comp_links.composition_id AND
	COALESCE(compositions.composition_id = ANY($4), true)
	GROUP BY compositions.composition_id
	HAVING (
		COALESCE(COUNT(album_comp_links) >= $1, true) AND
		COALESCE(COUNT(album_comp_links) <= $2, true) AND
		COALESCE(ARRAY_AGG(DISTINCT album_id) ' || any_or_all || ' $3, true)
	)
	ORDER BY composition_id'
	using filters.number_belongs_from, filters.number_belongs_to, filters.collections_list, compositions_ids;
end;
$$ language plpgsql called on null input;


-- orders
-- 1 - composition_id
-- 2 - title
-- 3 - artist_id
-- 4 - duration
-- 5 - release_date
-- 6 - times_listened
-- 7 - times_rated
-- 8 - average_rating
-- 9 - playlists_belong_number
-- 10 - albums_belong_number
-- positive - asc
-- negative - desc
create or replace function get_compositions
(
	compositions_ids integer array,
	attribute_filter compositions_attributes_filter,
	history_toggle boolean,
	history_filters compositions_history_statistics_filter,
	rating_toggle boolean,
	rating_filter compositions_rating_statistics_filter,
	playlists_toggle boolean,
	playlists_filter compositions_collections_statistics_filter,
	albums_toggle boolean,
	albums_filter compositions_collections_statistics_filter,
	pagination pagination_filter,
	orders integer array default array[1]
)
returns table
(
	composition_id integer,
    title character varying(64),
    artist_id integer,
    duration smallint,
    release_year smallint,
    release_month smallint,
    release_day smallint,
    lyrics text,
	path_to_file text,
	fulltext_highlight text,
	times_listened bigint,
	times_rated bigint,
	average_rating real,
	playlists_belong_number bigint,
	albums_belong_number bigint
)
as $$
declare
hist_join text := '(select null::int, null::bigint as times_listened) hist on true';
rate_join text := '(select null::int, null::bigint as times_rated, null::numeric as avg_rating) rate on true';
plist_join text := '(select null::int, null::bigint as belongs_number) plist_belong on true';
album_join text := '(select null::int, null::bigint as belongs_number) album_belong on true';
artists_search_mode text := ' OR artist_id IS NULL';
release_search_mode text := ' OR release_year IS NULL';
ftq_head text := 'null::text';
ftq_where text := 'COALESCE(compositions.title LIKE ''%%''||$1||''%%'', true)';
ftq_rank text := '';
orders_text text := '';
orders_types constant text array := array[
    'composition_id',
    'title',
    'artist_id',
    'duration',
    'release_date',
    'times_listened',
    'times_rated',
    'average_rating',
    'playlists_belong_number',
    'albums_belong_number'
];
order_type integer;
begin
if attribute_filter.search_lyrics and attribute_filter.title_lyrics is not null then
ftq_head := 'ts_headline(compositions.title ||''\n''|| compositions.lyrics, plainto_tsquery($1))';
ftq_where := 'compositions.search_tsv @@ plainto_tsquery($1)';
ftq_rank := 'ts_rank(compositions.search_tsv), plainto_tsquery($1)) DESC, ';
end if;

if attribute_filter.artists_ids_exclude_nulls then
artists_search_mode := ' AND artist_id IS NOT NULL';
end if;
if attribute_filter.release_date_exclude_nulls then
release_search_mode := ' AND release_year IS NOT NULL';
end if;

if history_toggle then
hist_join := 'get_compositions_history_statistics($11, $7) AS hist ON compositions.composition_id = hist.composition_id';
end if;
if rating_toggle then
rate_join := 'get_compositions_rating_statistics($11, $8) AS rate ON compositions.composition_id = rate.composition_id';
end if;
if playlists_toggle then
plist_join := 'get_compositions_playlists_statistics($11, $9) AS plist_belong ON compositions.composition_id = plist_belong.composition_id';
end if;
if albums_toggle then
album_join := 'get_compositions_albums_statistics($11, $10) AS album_belong ON compositions.composition_id = album_belong.composition_id';
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
	'SELECT compositions.composition_id, compositions.title, compositions.artist_id,
	compositions.duration, compositions.release_year, compositions.release_month,
	compositions.release_day, compositions.lyrics, compositions.path_to_file, '|| ftq_head ||',
	hist.times_listened, rate.times_rated, round(rate.avg_rating, 2)::real, 
	plist_belong.belongs_number, album_belong.belongs_number
	FROM compositions
	INNER JOIN ' || hist_join || '
	INNER JOIN ' || rate_join || '
	INNER JOIN ' || plist_join || '
	INNER JOIN ' || album_join || '
	WHERE
	COALESCE(compositions.composition_id = ANY($11), true) AND
	'|| ftq_where ||' AND
	COALESCE(artist_id = ANY($2)'|| artists_search_mode ||', true) AND
	COALESCE(duration >= $3, true) AND
	COALESCE(duration <= $4, true) AND
	COALESCE(compare_dates(release_year, release_month, release_day, $5) <= 0'|| release_search_mode ||', true) AND
	COALESCE(compare_dates(release_year, release_month, release_day, $6) >= 0'|| release_search_mode ||', true)
	ORDER BY '|| ftq_rank || orders_text ||'
	OFFSET $12 LIMIT $13'
	using attribute_filter.title_lyrics, attribute_filter.artists_ids, attribute_filter.duration_from,
	attribute_filter.duration_to, attribute_filter.release_from, attribute_filter.release_to,
	history_filters, rating_filter, playlists_filter, albums_filter, compositions_ids,
	pagination.offset_count, pagination.page_size;
end;
$$ language plpgsql called on null input;

select * from get_compositions( null,
	row(null, false, null, null, null, false, null, null, null),
	true,
	row(null, null, null, null, null, null),
	true,
	row(null, null, null, null, null, null, null, null), 
	true,
	row(null, null, null, null),
	true,
	row(null, null, null, null),
	row(null, null)
)