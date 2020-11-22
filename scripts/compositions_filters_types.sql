create type compositions_attributes_filter as
(
	title_lyrics text,
	artists_ids_exclude_nulls boolean,
    artists_ids integer array,
    duration_from smallint,
	duration_to smallint,
	release_date_exclude_nulls boolean,
    release_from date,
	release_to date,
    search_lyrics boolean -- fulltext
);

create type compositions_history_statistics_filter as
(
	listening_date_from date,
	listening_date_to date,
	times_listened_from integer,
	times_listened_to integer,
	users_ids_list integer array,
	users_ids_any boolean
);

create type compositions_rating_statistics_filter as
(
	rating_date_from date,
	rating_date_to date,
	times_rated_from integer,
	times_rated_to integer,
	average_rating_from numeric,
	average_rating_to numeric,
	users_ids_list integer array,
	users_ids_any boolean
);

create type compositions_collections_statistics_filter as
(
	number_belongs_from integer,
	number_belongs_to integer,
	collections_list integer array,
	collections_any boolean
);