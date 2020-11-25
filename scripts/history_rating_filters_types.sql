create type history_filter as
(
	users_ids integer array,
	compositions_ids integer array,
	date_from date,
	date_to date
);

create type rating_filter as
(
	users_ids integer array,
	rated_ids integer array,
	satisfied boolean,
	date_from date,
	date_to date
);