create or replace function get_history
(filters history_filter)
returns table(
	record_id bigint,
	user_id integer,
	composition_id integer,
	listening_date date
)
as $$
begin
return query execute 
	'SELECT listening_history.*
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

select
*,
row_number() over (partition by composition_id order by listening_date asc),
count(listening_history) over (partition by composition_id order by listening_date asc)
from listening_history

select
*,
count(listening_history) over (partition by composition_id order by listening_date desc) -
count(listening_history) over (partition by composition_id order by listening_date asc) as user_listened
from listening_history

select
*
from listening_history

with tt as (
select
*,
row_number() over (partition by user_id order by rating_date asc),
count(compositions_rating) over (partition by user_id order by rating_date asc),
sum(satisfied::integer) over (partition by user_id order by rating_date asc),
round(avg(satisfied::integer*10) over (partition by user_id order by rating_date asc), 1)
from compositions_rating
)
select * from tt
where user_id =

select
*,
count(compositions_rating) over (partition by composition_id order by rating_date asc),
round(avg(satisfied::integer*10) over (partition by composition_id order by rating_date asc), 1)
from compositions_rating

select
*
from compositions_rating