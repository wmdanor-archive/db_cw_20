create or replace function make_tsvector(main text, secondary text)
returns tsvector
as $$
begin
return
(
	setweight(to_tsvector(main),'A') ||
    setweight(to_tsvector(secondary), 'B')
);
end;
$$ language plpgsql immutable;