create or replace function compare_dates -- -1 -> 1 > 2 | 0 -> 1 => 2 | 1 < 2
(year_1 smallint, month_1 smallint, day_1 smallint, date_2 date)
returns smallint
as $$
declare
year_2 smallint := null;
month_2 smallint := null;
day_2 smallint := null;
b1 boolean := year_1 is null;
b2 boolean := month_1 is null;
b3 boolean := day_1 is null;
date_1 date := null;
begin
if date_2 is null then return null; end if;
year_2 := date_part('year', date_2);
month_2 := date_part('month', date_2);
day_2 := date_part('day', date_2);
if b1 and b2 and b3 then return null;
elsif not b1 and b2 and b3 then
	case
	when year_1 > year_2 then return -1;
	when year_1 < year_2 then return 1;
	else return 0;
	end case;
elsif not b1 and not b2 and b3 then
	case
	when year_1 > year_2 then return -1;
	when year_1 < year_2 then return 1;
	else case
		when month_1 > month_2 then return -1;
		when month_1 < month_2 then return 1;
		else return 0;
		end case;
	end case;
elsif not b1 and not b2 and not b3 then
	date_1 := make_date(year_1, month_1, day_1);
	case
	when date_1 > year_2 then return -1;
	when date_1 < year_2 then return 1;
	else return 0;
	end case;
else raise exception 'Invalid date 1';
end if;
end;
$$ language plpgsql called on null input;