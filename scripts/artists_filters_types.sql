create type artists_attributes_filter as
(
    name_comment text,
    types varchar(16) array,
    genders varchar(32) array,
	begin_date_from date,
	begin_date_to date,
	end_date_from date,
    end_date_to date,
    search_comments boolean -- fulltext
);