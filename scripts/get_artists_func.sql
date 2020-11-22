create or replace function get_artists_history_statistics
(artists_ids integer array, filters compositions_history_statistics_filter)
returns table(artist_id integer, times_listened bigint)
as $$
declare
any_or_all char(2) := '&&';
begin
if not filters.users_ids_any then any_or_all = '@>';
end if;
return query execute 
	'SELECT compositions.artist_id, COUNT(listening_history)
   	FROM compositions LEFT JOIN listening_history ON compositions.composition_id = listening_history.composition_id AND
	COALESCE(compositions.artist_id = ANY($6), true) AND
	COALESCE(listening_date >= $1, true) AND
 	COALESCE(listening_date <= $2, true)
   	GROUP BY compositions.artist_id
   	HAVING (
		COALESCE(COUNT(listening_history) >= $3, true) AND
		COALESCE(COUNT(listening_history) <= $4, true) AND
		COALESCE(ARRAY_AGG(DISTINCT user_id) ' || any_or_all || ' $5, true)
	)
	ORDER BY artist_id'
	using
	filters.listening_date_from, filters.listening_date_to, filters.times_listened_from,
	filters.times_listened_to, filters.users_ids_list, artists_ids;
end;
$$ language plpgsql called on null input;



create or replace function get_artists_rating_statistics
(artists_ids integer array, filters compositions_rating_statistics_filter)
returns table(artist_id integer, times_rated bigint, avg_rating numeric)
as $$
declare
any_or_all char(2) := '&&';
begin
if not filters.users_ids_any then any_or_all = '@>';
end if;
return query execute
	'SELECT compositions.artist_id, COUNT(compositions_rating), AVG(satisfied::integer) * 10
	FROM compositions LEFT JOIN compositions_rating ON compositions.composition_id = compositions_rating.composition_id AND
	COALESCE(compositions.artist_id = ANY($8), true) AND
	COALESCE(rating_date >= $1, true) AND
	COALESCE(rating_date <= $2, true)
	GROUP BY compositions.artist_id
   	HAVING (
		COALESCE(COUNT(compositions_rating) >= $3, true) AND
		COALESCE(COUNT(compositions_rating) <= $4, true) AND
		COALESCE(AVG(satisfied::integer) * 10 >= $5, true) AND
		COALESCE(AVG(satisfied::integer) * 10 <= $6, true) AND
		COALESCE(ARRAY_AGG(DISTINCT user_id) ' || any_or_all || ' $7, true)
	)
	ORDER BY artist_id'
	using filters.rating_date_from, filters.rating_date_to, filters.times_rated_from,
	filters.times_rated_to, filters.average_rating_from, filters.average_rating_to,
	filters.users_ids_list, artists_ids;
end;
$$ language plpgsql called on null input;



create or replace function get_artists_playlists_statistics
(artists_ids integer array, filters compositions_collections_statistics_filter)
returns table(artist_id integer, belongs_number bigint)
as $$
declare
any_or_all char(2) := '&&';
begin
if not filters.collections_any then any_or_all = '@>';
end if;
return query execute
	'SELECT compositions.artist_id, COUNT(DISTINCT plist_comp_links.playlist_id)
	FROM compositions LEFT JOIN plist_comp_links ON compositions.composition_id = plist_comp_links.composition_id AND
	COALESCE(compositions.artist_id = ANY($4), true)
	GROUP BY compositions.artist_id
	HAVING (
		COALESCE(COUNT(distinct plist_comp_links.playlist_id) >= $1, true) AND
		COALESCE(COUNT(distinct plist_comp_links.playlist_id) <= $2, true) AND
		COALESCE(ARRAY_AGG(DISTINCT playlist_id) ' || any_or_all || ' $3, true)
	)
	ORDER BY artist_id'
	using filters.number_belongs_from, filters.number_belongs_to, filters.collections_list, artists_ids;
end;
$$ language plpgsql called on null input;



create or replace function get_artists_albums_statistics
(artists_ids integer array, filters compositions_collections_statistics_filter)
returns table(artist_id integer, belongs_number bigint)
as $$
declare
any_or_all char(2) := '&&';
begin
if not filters.collections_any then any_or_all = '@>';
end if;
return query execute
	'SELECT compositions.artist_id, COUNT(DISTINCT album_comp_links.album_id)
	FROM compositions LEFT JOIN album_comp_links ON compositions.composition_id = album_comp_links.composition_id AND
	COALESCE(compositions.artist_id = ANY($4), true)
	GROUP BY compositions.artist_id
	HAVING (
		COALESCE(COUNT(distinct album_comp_links.album_id) >= $1, true) AND
		COALESCE(COUNT(distinct album_comp_links.album_id) <= $2, true) AND
		COALESCE(ARRAY_AGG(DISTINCT album_id) ' || any_or_all || ' $3, true)
	)
	ORDER BY artist_id'
	using filters.number_belongs_from, filters.number_belongs_to, filters.collections_list, artists_ids;
end;
$$ language plpgsql called on null input;



create or replace function get_artists -- modify for times listened
(
	artists_ids integer array,
	attribute_filter artists_attributes_filter,
	history_toggle boolean,
	history_filters compositions_history_statistics_filter,
	rating_toggle boolean,
	rating_filter compositions_rating_statistics_filter,
	playlists_toggle boolean,
	playlists_filter compositions_collections_statistics_filter,
	albums_toggle boolean, 
	albums_filter compositions_collections_statistics_filter
)
returns table
(
    artist_id integer,
    name text,
    type character varying(16),
    gender character varying(32),
    begin_date_year smallint,
    begin_date_month smallint,
    begin_date_day smallint,
    end_date_year smallint,
    end_date_month smallint,
    end_date_day smallint,
    comment text,
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
ftq_name text := 'artists.name::text';
ftq_comment text := 'artists.comment';
ftq_where text := 'COALESCE(artists.name LIKE ''%%''||$1||''%%'', true)';
ftq_rank text := 'artist_id ASC';
begin

if attribute_filter.begin_date_from is not null or attribute_filter.begin_date_to is not null or 
attribute_filter.end_date_from is not null or attribute_filter.end_date_to is not null or 
attribute_filter.genders is not null then raise exception 'Not implemented';
end if;
if attribute_filter.search_comments and attribute_filter.name_comment is not null then
ftq_name := 'ts_headline(artists.name, plainto_tsquery($1))';
ftq_comment := 'ts_headline(artists.comment, plainto_tsquery($1))';
ftq_where := 'make_tsvector(artists.name, artists.comment) @@ plainto_tsquery($1)';
ftq_rank := 'ts_rank(make_tsvector(artists.name, artists.comment), plainto_tsquery($1)) DESC';
end if;

if history_toggle then
hist_join := 'get_artists_history_statistics($12, $8) AS hist ON artists.artist_id = hist.artist_id';
end if;
if rating_toggle then
rate_join := 'get_artists_rating_statistics($12, $9) AS rate ON artists.artist_id = rate.artist_id';
end if;
if playlists_toggle then
plist_join := 'get_artists_playlists_statistics($12, $10) AS plist_belong ON artists.artist_id = plist_belong.artist_id';
end if;
if albums_toggle then
album_join := 'get_artists_albums_statistics($12, $11) AS album_belong ON artists.artist_id = album_belong.artist_id';
end if;
return query execute
	'SELECT artists.artist_id, '|| ftq_name ||', artist_types.name,
	genders.name, artists.begin_date_year, artists.begin_date_month,
	artists.begin_date_day, artists.end_date_year, artists.end_date_month,
	artists.end_date_day, '|| ftq_comment ||',
	hist.times_listened, rate.times_rated, round(rate.avg_rating, 2)::real,
	plist_belong.belongs_number, album_belong.belongs_number
	FROM artists
	LEFT JOIN artist_types ON artists.type_id = artist_types.type_id
	LEFT JOIN genders ON artists.gender_id = artists.gender_id
	INNER JOIN ' || hist_join || '
	INNER JOIN ' || rate_join || '
	INNER JOIN ' || plist_join || '
	INNER JOIN ' || album_join || '
	WHERE
	COALESCE(artists.artist_id = ANY($12), true) AND
	'|| ftq_where ||' AND
	COALESCE(artist_types.name = ANY($2), true)
	ORDER BY ' || ftq_rank
	using attribute_filter.name_comment, attribute_filter.types, attribute_filter.genders,
	attribute_filter.begin_date_from, attribute_filter.begin_date_to,
	attribute_filter.end_date_from, attribute_filter.end_date_to,
	history_filters, rating_filter, playlists_filter, albums_filter, artists_ids;
end;
$$ language plpgsql called on null input;

/*
	COALESCE(genders.name = ANY($3)'|| genders_search_mode ||', true) AND
	COALESCE(compare_dates(begin_date_year, begin_date_month, begin_date_day, $4) <= 0'|| begin_date_mode ||', true) AND
	COALESCE(compare_dates(begin_date_year, begin_date_month, begin_date_day, $5) >= 0'|| begin_date_mode ||', true) AND
	COALESCE(compare_dates(end_date_year, end_date_month, end_date_day, $6) <= 0'|| end_date_mode ||', true) AND
	COALESCE(compare_dates(end_date_year, end_date_month, end_date_day, $7) >= 0'|| end_date_mode ||', true)
	needs complex analysis
*/

select * from get_artists( null,
	row(null, null, null, null, null, null, null, true),
	true,
	row(null, null, null, null, null, null),
	true,
	row(null, null, null, null, null, null, null, null), 
	true,
	row(null, null, null, null),
	true,
	row(null, null, null, null)
)