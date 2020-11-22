create index artist_types_idx on artists using btree (type_id);
create index artist_gender_idx on artists using btree (gender_id);
create index artist_comment_idx on artists using gin (search_tsv);
create index composition_tsv_idx on compositions using gin (search_tsv);
create index playlist_type_idx on playlists using btree (privacy_id);
create index user_gender_idx on users using btree (gender_id);


drop index artist_types_idx;
drop index artist_gender_idx;
drop index artist_comment_idx;
drop index composition_tsv_idx;
drop index playlist_type_idx;
drop index user_gender_idx;

-- trash

insert into artists(name, type_id, gender_id, begin_date_year, begin_date_month, begin_date_day,
				   end_date_year, end_date_month, end_date_day, comment)
select * from select_random_artists(900001, 1000000)


select * from artists -- 1
where gender_id = any(array[1, 2])

select * from artists
where gender_id = 1

select * from artists
where type_id = any(array[1, 5]) -- 2
and gender_id = any(array[1, 2]) -- 3

select * from artists
where type_id = 1

select count(*) from artists

select type_id, count(*) from artists
group by type_id

select type_id, count(*) from artists
where gender_id is not null
group by type_id

select * from artists
order by type_id


select * from compositions

select compositions.* from compositions
where search_tsv @@ plainto_tsquery('everybody')
order by ts_rank(search_tsv, plainto_tsquery('everybody')) DESC

select compositions.*, ts_headline(title || '\n' || lyrics, plainto_tsquery('far never')) from compositions
where search_tsv @@ plainto_tsquery('far never')
order by ts_rank(search_tsv, plainto_tsquery('far never')) DESC

select compositions.*, ts_headline(title || '\n' || lyrics, plainto_tsquery('everybody right body first')) from compositions
where search_tsv @@ plainto_tsquery('everybody right body first')
order by ts_rank(search_tsv, plainto_tsquery('everybody right body first')) DESC

select word, ndoc from ts_stat('select search_tsv from compositions')
order by ndoc desc

update compositions set search_tsv = make_tsvector(compositions.title, compositions.lyrics)