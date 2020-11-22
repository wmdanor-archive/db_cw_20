create type users_attributes_filter as
(
	username text,
	full_name_exclude_nulls boolean,
	full_name text,
	registration_from date,
	registration_to date,
	birth_exclude_nulls boolean,
	birth_from date,
	birth_to date,
	gender_exclude_nulls boolean,
	genders varchar(32) array,
	is_active boolean
); 

create type users_history_statistics_filter as
(
	listening_date_from date,
	listening_date_to date,
	times_listened_from integer,
	times_listened_to integer,
	compositions_list integer array,
	compositions_any boolean
);

create type users_rating_statistics_filter as
(
	rating_date_from date,
	rating_date_to date,
	times_rated_from integer,
	times_rated_to integer,
	average_rating_from numeric,
	average_rating_to numeric,
	rated_ids_list integer array,
	rated_ids_any boolean
);

create type users_saved_collections_statistics_filter as
(
	saved_number_from integer,
	saved_number_to integer,
	saved_ids_list integer array,
	saved_ids_any boolean
);