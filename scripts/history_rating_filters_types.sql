create type history_filter
(
	users_ids integer array,
	compositions_ids integer array,
	date_from date,
	date_to date
);