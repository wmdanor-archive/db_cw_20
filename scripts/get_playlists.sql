create or replace function get_playlists_compositions_statistics
(playlists_ids integer array, filters collections_compositions_statistics_filter)
returns table(playlist_id integer, compositions_number bigint)
as $$
declare
any_or_all char(2) := '&&';
begin
if not filters.compositions_any then any_or_all = '@>';
end if;
return query execute
	'SELECT playlists.playlist_id, COUNT(plist_comp_links)
	FROM playlists LEFT JOIN plist_comp_links ON playlists.playlist_id = plist_comp_links.playlist_id AND
	COALESCE(playlists.playlist_id = ANY($4), true)
	GROUP BY playlists.playlist_id
	HAVING (
		COALESCE(COUNT(plist_comp_links) >= $1, true) AND
		COALESCE(COUNT(plist_comp_links) <= $2, true) AND
		COALESCE(ARRAY_AGG(DISTINCT composition_id) ' || any_or_all || ' $3, true)
	)
	ORDER BY playlist_id'
	using filters.compositions_number_from, filters.compositions_number_to, filters.compositions_list, playlists_ids;
end;
$$ language plpgsql called on null input;



create or replace function get_playlists_rating_statistics
(playlists_ids integer array, filters entity_rating_statistics_filter)
returns table(playlist_id integer, times_rated bigint, avg_rating numeric)
as $$
declare
any_or_all char(2) := '&&';
begin
if not filters.users_ids_any then any_or_all = '@>';
end if;
return query execute
	'SELECT playlists.playlist_id, COUNT(playlists_rating), AVG(satisfied::integer) * 10
	FROM playlists LEFT JOIN playlists_rating ON playlists.playlist_id = playlists_rating.playlist_id AND
	COALESCE(playlists.playlist_id = ANY($8), true) AND
	COALESCE(rating_date >= $1, true) AND
	COALESCE(rating_date <= $2, true)
	GROUP BY compositions.composition_id
   	HAVING (
		COALESCE(COUNT(playlists_rating) >= $3, true) AND
		COALESCE(COUNT(playlists_rating) <= $4, true) AND
		COALESCE(AVG(satisfied::integer) * 10 >= $5, true) AND
		COALESCE(AVG(satisfied::integer) * 10 <= $6, true) AND
		COALESCE(ARRAY_AGG(DISTINCT user_id) ' || any_or_all || ' $7, true)
	)
	ORDER BY playlist_id'
	using filters.rating_date_from, filters.rating_date_to, filters.times_rated_from,
	filters.times_rated_to, filters.average_rating_from, filters.average_rating_to,
	filters.users_ids_list, playlists_ids;
end;
$$ language plpgsql called on null input;



create or replace function get_playlists_users_statistics
(playlists_ids integer array, filters collections_users_statistics_filter)
returns table(playlist_id integer, users_saved_number bigint)
as $$
declare
any_or_all char(2) := '&&';
begin
if not filters.users_any then any_or_all = '@>';
end if;
return query execute
	'SELECT playlists.playlist_id, COUNT(user_saved_plists)
	FROM playlists LEFT JOIN user_saved_plists ON playlists.playlist_id = user_saved_plists.playlist_id
	AND COALESCE(playlists.playlist_id = ANY($4), true)
	GROUP BY playlists.playlist_id
	HAVING (
		COALESCE(COUNT(user_saved_plists) >= $1) AND
		COALESCE(COUNT(user_saved_plists) <= $2) AND
		COALESCE(ARRAY_AGG(DISTINCT user_id) ' || any_or_all || ' $3, true)
	)
	ORDER BY playlist_id'
	using filters.users_number_from, filters.users_number_to, filters.users_list, playlists_ids;
end;
$$ language plpgsql called on null input;



-- orders
-- 1 - playlist_id
-- 2 - title
-- 3 - creator_id
-- 4 - privacy_id
-- 5 - compositions_number
-- 6 - times_rated
-- 7 - average_rating
-- 8 - users_saved_number
-- positive - asc
-- negative - desc
create or replace function get_playlists
(
	playlists_ids integer array,
	attribute_filter playlists_attributes_filter,
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
	playlist_id integer,
    title character varying(32),
    creator_id integer,
	privacy character varying(16),
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
creator_search_mode text := ' OR creator_id IS NULL';
orders_text text := '';
orders_types constant text array := array[
    'playlist_id',
    'title',
    'creator_id',
	'privacy_id',
    'compositions_number',
    'times_rated',
    'average_rating',
    'users_saved_number'
];
order_type integer;
privacies_ids smallint array := null;
privacy_temp varchar(16);
begin

if attribute_filter.creators_ids_exclude_nulls then
creator_search_mode := ' AND creator_id IS NOT NULL';
end if;

if compositions_toggle then
comp_join := 'get_playlists_compositions_statistics($7, $4) AS comp ON playlists.playlist_id = comp.playlist_id';
end if;
if rating_toggle then
rate_join := 'get_playlists_rating_statistics($7, $5) AS rate ON playlists.playlist_id = rate.playlist_id';
end if;
if users_toggle then
users_join := 'get_playlists_users_statistics($7, $6) AS users ON playlists.playlist_id = users.playlist_id';
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

if attribute_filter.privacies is not null and array_length(attribute_filter.privacies, 1) != 0 then
	privacies_ids := array[];
	foreach privacy_temp in array attribute_filter.privacies
	loop
		if privacy_temp = 'public' then privacies_ids := privacies_ids || 1;
		elsif privacy_temp = 'unlisted' then privacies_ids := privacies_ids || 2;
		elsif privacy_temp = 'private' then privacies_ids := privacies_ids || 3;
		else raise exception 'Invalid privacy type - %',  privacy_temp;
		end if;
	end loop;
end if;

return query execute
	'SELECT playlists.playlist_id, playlists.title, playlists.creator_id, playlists_privacy.privacy_type,
	comp.compositions_number, rate.times_rated, round(rate.avg_rating, 2)::real, users.users_saved_number
	FROM playlists
	LEFT JOIN playlists_privacy ON playlists.privacy_id = playlists_privacy.privacy_id
	INNER JOIN ' || comp_join || '
	INNER JOIN ' || rate_join || '
	INNER JOIN ' || users_join || '
	WHERE
	COALESCE(playlists.playlist_id = ANY($7), true) AND
	COALESCE(playlists.title LIKE ''%%''||$1||''%%'', true) AND
	COALESCE(creator_id = ANY($2)'|| creator_search_mode ||', true) AND
	COALESCE(playlists.privacy_id = ANY($3), true)
	ORDER BY '|| orders_text ||'
	OFFSET $8 LIMIT $9'
	using attribute_filter.title, attribute_filter.creators_ids, privacies_ids,
	compositions_filter, rating_filter, users_filter, playlists_ids,
	pagination.offset_count, pagination.page_size;
end;
$$ language plpgsql called on null input;



select * from get_playlists( null,
	row(null, false, null, null),
	true,
	row(null, null, null, null),
	true,
	row(null, null, null, null, null, null, null, null), 
	true,
	row(null, null, null, null),
	row(null, null)
)