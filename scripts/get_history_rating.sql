-- orders
-- 1 - record_id
-- 2 - user_id
-- 3 - composition_id
-- 4 - listening_date
-- positive - asc
-- negative - desc
create or replace function get_history
(
	filters history_filter,
	user_listened_counter boolean,
	composition_listened_counter boolean,
	pagination pagination_filter,
	orders integer array default array[1]
)
returns table(
	record_id bigint,
	user_id integer,
	composition_id integer,
	listening_date date,
	times_user_listened bigint,
	times_composition_listened bigint
)
as $$
declare
window_query_1 text := 'null::bigint';
window_query_2 text := 'null::bigint';
orders_text text := '';
orders_types constant text array := array[
    'record_id',
    'user_id',
    'composition_id',
    'listening_date'
];
order_type integer;
begin

if user_listened_counter then
	window_query_1 := 'row_number() over (partition by user_id order by listening_date asc)';
end if;
if composition_listened_counter then
	window_query_2 := 'row_number() over (partition by composition_id order by listening_date asc)';
end if;

if array_length(orders, 1) = 0 then
	raise exception 'orders can not be empty';
end if;
foreach order_type in array orders
loop
	if order_type = 0 or abs(order_type) > 11 then
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
	'SELECT *, '|| window_query_1 ||', '|| window_query_2 ||'
   	FROM listening_history
	WHERE
	COALESCE(listening_date >= $1, true) AND
 	COALESCE(listening_date <= $2, true) AND
	COALESCE(user_id = ANY($3), true) AND
	COALESCE(composition_id = ANY($4), true)
	ORDER BY '|| orders_text ||'
	OFFSET $5 LIMIT $6'
	using
	filters.date_from, filters.date_to,
	filters.users_ids, filters.compositions_ids,
	pagination.offset_count, pagination.page_size;
end;
$$ language plpgsql called on null input;

select * from get_history(
	row(null, null, null, null),
	true,
	true,
	row(null, null),
	array[1, 4]
)


-- rated_types
-- 1 - compositions
-- 2 - albums
-- 3 - playlists
-- orders
-- 1 - rating_id
-- 2 - rated_id
-- 3 - user_id
-- 4 - satisfied
-- 5 - rating_date
-- positive - asc
-- negative - desc
create or replace function get_rating
(
	rated_type integer,
	filters rating_filter,
	rated_rating_counter boolean,
	user_rating_counter boolean,
	pagination pagination_filter,
	orders integer array default array[1]
)
returns table(
	record_id bigint,
	rated_id integer,
	user_id integer,
	satisfied boolean,
	rating_date date,
	times_rated_rated bigint,
	avg_rated_rating numeric,
	times_user_rated bigint,
	avg_user_rating numeric
	
)
as $$
declare
window_query_1 text := 'null::bigint, null::numeric';
window_query_2 text := 'null::bigint, null::numeric';
orders_text text := '';
orders_types text array := array[
    'rating_id',
    'rated_id',
    'user_id',
    'satisfied',
	'rating_date'
];
order_type integer;
rated_table_name text;
rated_id_name text;
begin

if rated_type = 1 then
	rated_table_name := 'compositions_rating';
	rated_id_name := 'composition_id';
elsif rated_type = 2 then
	rated_table_name := 'albums_rating';
	rated_id_name := 'album_id';
elsif rated_type = 3 then
	rated_table_name := 'playlists_rating';
	rated_id_name := 'playlist_id';
else raise exception 'invalid rated_type';
end if;
orders_types[2] := rated_id_name;
raise notice '%', orders_types;

if rated_rating_counter then
	window_query_1 := 'row_number() over (partition by '|| rated_id_name ||' order by rating_date asc), ' ||
	'(avg(satisfied::integer) over (partition by '|| rated_id_name ||' order by rating_date asc))*10';
end if;
if user_rating_counter then
	window_query_2 := 'row_number() over (partition by user_id order by rating_date asc), ' ||
	'(avg(satisfied::integer) over (partition by user_id order by rating_date asc))*10';
end if;

if array_length(orders, 1) = 0 then
	raise exception 'orders can not be empty';
end if;
foreach order_type in array orders
loop
	if order_type = 0 or abs(order_type) > 11 then
		raise exception 'invalid order type value %', order_type;
	end if;
	if order_type > 0 then
		orders_text := orders_text || orders_types[abs(order_type)] || ' ASC, ';
	else
		orders_text := orders_text || orders_types[abs(order_type)] || ' DESC, ';
	end if;
end loop;
orders_text := rtrim(orders_text, ', ');

raise notice '%', orders_text;

return query execute 
	'SELECT *, '|| window_query_1 ||', '|| window_query_2 ||'
   	FROM '|| rated_table_name ||'
	WHERE
	COALESCE(rating_date >= $1, true) AND
 	COALESCE(rating_date <= $2, true) AND
	COALESCE(user_id = ANY($3), true) AND
	COALESCE('|| rated_id_name ||' = ANY($4), true) AND
	COALESCE(satisfied = $5, true)
	ORDER BY '|| orders_text ||'
	OFFSET $6 LIMIT $7'
	using
	filters.date_from, filters.date_to,
	filters.users_ids, filters.rated_ids, filters.satisfied,
	pagination.offset_count, pagination.page_size;
end;
$$ language plpgsql called on null input;

select * from get_rating( 1,
	row(null, null, null, null, null),
	true,
	true,
	row(null, null),
	array[3, 5]
)



---------------------------------------------------------------------------------------------------------------

select
*,
row_number() over (partition by composition_id order by listening_date asc)
from listening_history

select
*,
row_number() over (partition by user_id order by listening_date asc) as c1,
row_number() over (partition by composition_id order by listening_date asc) as c2
from listening_history
order by composition_id, c2

select
*
from listening_history


select
*,
row_number() over w,
sum(satisfied::integer) over w,
round(avg(satisfied::integer) over w, 3)*10
from compositions_rating
window w as (partition by user_id order by rating_date asc)
order by user_id asc, rating_date desc

select
*,
row_number() over w,
sum(satisfied::integer) over w,
round(avg(satisfied::integer) over w, 3)*10
from compositions_rating
window w as (partition by user_id order by rating_date asc)
order by rating_date desc

create or replace function temp2
()
returns table(
	record_id bigint,
	user_id integer,
	composition_id integer,
	satisfied bool,
	rating_date date
)
as $$
begin
return query execute 'select * from compositions_rating';
end;
$$ language plpgsql;


select temp2()

select * from (
	select
	*,
	row_number() over w,
	sum(satisfied::integer) over w,
	round(avg(satisfied::integer) over w, 3)*10
	from compositions_rating
	window w as (partition by user_id order by rating_date asc)
) s
ORDER BY rating_date DESC


select
*,
count(compositions_rating) over (partition by composition_id order by rating_date asc),
round(avg(satisfied::integer*10) over (partition by composition_id order by rating_date asc), 1)
from compositions_rating

select
*
from compositions_rating