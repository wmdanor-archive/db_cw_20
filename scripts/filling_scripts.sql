create or replace function toss_a_coin(true_result_possibility numeric)
returns boolean
as $$
begin
return random() <= true_result_possibility;
end;
$$ language plpgsql;


create or replace function select_random_artists(start_number integer, end_number integer)
returns table(
	name text,
	type_id smallint,
	gender_id smallint,
	begin_year smallint,
	begin_month smallint,
	begin_day smallint,
	end_year smallint,
	end_month smallint,
	end_day smallint,
	comment text
)
as $$
declare
temp_date date;
a_types smallint[];
a_genders smallint[];
begin_year smallint[];
begin_month smallint[];
begin_day smallint[];
end_year smallint[];
end_month smallint[];
end_day smallint[];
begin
for iter in start_number..end_number loop
if true then
	temp_date := (timestamp '1970-1-1' + random()*(timestamp '2000-1-1' - timestamp '1970-1-1'))::date;
	begin_year[iter] := date_part('year', temp_date);
	if toss_a_coin(0.9) then
		begin_month[iter] := date_part('month', temp_date);
		if toss_a_coin(0.9) then
			begin_day[iter] := date_part('day', temp_date);
		end if;
	end if;
end if;
if toss_a_coin(0.5) then
	temp_date := (timestamp '2015-1-1' + random()*(timestamp '2020-11-1' - timestamp '2015-1-1'))::date;
	end_year[iter] := date_part('year', temp_date);
	if toss_a_coin(0.9) then
		end_month[iter] := date_part('month', temp_date);
		if toss_a_coin(0.9) then
			end_day[iter] := date_part('day', temp_date);
		end if;
	end if;
end if;
a_types[iter] := floor(random()*(6) + 1)::smallint;
if a_types[iter] = 1 or a_types[iter] = 5 then
	a_genders[iter] = floor(random()*(3) + 1)::smallint;
end if;
end loop;
return query execute
	'SELECT ''artist ''||s.a, $1[s.a], $2[s.a], $3[s.a], $4[s.a], $5[s.a], $6[s.a], $7[s.a], $8[s.a],
	null from generate_series($9, $10) as s(a)'
	using a_types, a_genders, begin_year, begin_month, begin_day, end_year, end_month, end_day, start_number, end_number;
end;
$$ language plpgsql;


create or replace function select_random_compositions(start_number integer, end_number integer)
returns table(
	title text,
	artist_id integer,
	duration smallint,
	release_year smallint,
	release_month smallint,
	release_day smallint,
	lyrics text,
	path_to_file text
)
as $$
declare
artists_ids int[];
release_date date;
release_year smallint[];
release_month smallint[];
release_day smallint[];
begin
execute 'select array_agg(artist_id) from artists' into artists_ids;
for iter in start_number..end_number loop
if toss_a_coin(0.9) then
	release_date := (timestamp '2015-1-1' + random()*(timestamp '2020-11-1' - timestamp '2015-1-1'))::date;
	release_year[iter] := date_part('year', release_date);
	if toss_a_coin(0.9) then
		release_month[iter] := date_part('month', release_date);
		if toss_a_coin(0.9) then
			release_day[iter] := date_part('day', release_date);
		end if;
	end if;
end if;
end loop;
return query execute
	'SELECT ''composition ''||s.a, $1[floor(random()* array_length($1, 1) + 1)], floor(random()* (300-90 + 1) + 90)::smallint,
	$2[s.a], $3[s.a], $4[s.a], null, ''path ''||s.a from generate_series($5, $6) as s(a)'
	using artists_ids, release_year, release_month, release_day, start_number, end_number;
end;
$$ language plpgsql;



create or replace function select_random_history(start_number integer, end_number integer)
returns table(user_id integer, composition_id integer, listening_date date)
as $$
declare
users_ids integer[];
compositions_ids integer[];
begin
execute 'select array_agg(user_id) from users' into users_ids;
execute 'select array_agg(composition_id) from compositions' into compositions_ids;
return query execute
	'SELECT $3[floor(random()* array_length($3, 1) + 1)], $4[floor(random()* array_length($4, 1) + 1)],
	(date ''2020-11-1'' - ''4 years''::interval + justify_interval(''4 years''::interval/($2 - $1 + 1) * (s.a - $1 + 1)))::date
	from generate_series($1, $2) as s(a)'
	using start_number, end_number, users_ids, compositions_ids;
end;
$$ language plpgsql;



create or replace function select_random_comp_rating(start_number integer, end_number integer)
returns table(user_id integer, composition_id integer, rating_date date, satisfied boolean)
as $$
declare
users_ids integer[];
compositions_ids integer[];
begin
execute 'select array_agg(user_id) from users' into users_ids;
execute 'select array_agg(composition_id) from compositions' into compositions_ids;
return query execute
	'SELECT $3[floor(random()* array_length($3, 1) + 1)], $4[floor(random()* array_length($4, 1) + 1)],
	(date ''2020-11-1'' - ''4 years''::interval + justify_interval(''4 years''::interval/($2 - $1 + 1) * (s.a - $1 + 1)))::date,
	toss_a_coin(0.7)
	from generate_series($1, $2) as s(a)'
	using start_number, end_number, users_ids, compositions_ids;
end;
$$ language plpgsql;



create or replace function select_random_playlists(start_number integer, end_number integer)
returns table(title text, creator_id integer, privacy_id integer)
as $$
declare
users_ids integer[];
begin
execute 'select array_agg(user_id) from users' into users_ids;
return query execute
	'SELECT ''playlist ''||s.a, case when toss_a_coin(0.9) then
	$3[floor(random()* array_length($3, 1) + 1)] else null end,
	1 from generate_series($1, $2) as s(a)'
	using start_number, end_number, users_ids;
end;
$$ language plpgsql;



create or replace function select_random_playlists_filling(start_number integer, end_number integer)
returns table(playlist_id integer, composition_id integer)
as $$
declare
playlists_ids integer[];
compositions_ids integer[];
begin
execute 'select array_agg(playlist_id) from playlists' into playlists_ids;
execute 'select array_agg(composition_id) from compositions' into compositions_ids;
return query execute
	'SELECT $3[floor(random()* array_length($3, 1) + 1)], $4[floor(random()* array_length($4, 1) + 1)]
	from generate_series($1, $2) as s(a)'
	using start_number, end_number, playlists_ids, compositions_ids;
end;
$$ language plpgsql;

select * from select_random_playlists_filling(1, 100)