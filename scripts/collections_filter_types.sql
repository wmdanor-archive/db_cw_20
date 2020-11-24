create type collections_compositions_statistics_filter as
(
	compositions_number_from integer,
	compositions_number_to integer,
	compositions_list integer array,
	compositions_any boolean
);

create type collections_users_statistics_filter as
(
	users_number_from integer,
	users_number_to integer,
	users_list integer array,
	users_any boolean
);

create type albums_attributes_filter as
(
	title text,
	release_date_exclude_nulls boolean,
	release_date_from date,
	release_date_to date
);

create type playlists_attributes_filter as
(
	title text,
	creators_ids_exclude_nulls boolean,
	creators_ids integer array,
	privacies varchar(16) array
);