do $$
declare
i int;
st date;
ed date;
begin

for i in 1..3500 loop

st := ('2000-1-1'::date + random() * '15 years'::interval)::date;
if toss_a_coin(0.1) then ed := ('2016-1-1'::date + random() * '4 years'::interval)::date;
else ed := null;
end if;

execute
'update artists set
begin_date_year = $2, begin_date_month = $3, begin_date_day = $4,
end_date_year = $5, end_date_month = $6, end_date_day = $7
where artist_id = $1 and type_id = 2'
using i, extract(year from st), extract(month from st), extract(day from st), 
	     extract(year from ed), extract(month from ed), extract(day from ed);

end loop;

end $$;

do $$
declare
i int;
st date;
ed date;
rvar real;
gen int;
begin

for i in 1..3500 loop

st := ('1970-1-1'::date + random() * '30 years'::interval)::date;
if toss_a_coin(0.1) then ed := ('2016-1-1'::date + random() * '4 years'::interval)::date;
else ed := null;
end if;

rvar := random();
if rvar <= 0.5 then gen := 1;
elsif rvar <= 0.995 then gen := 2;
else gen := 3;
end if;

execute
'update artists set
begin_date_year = $2, begin_date_month = $3, begin_date_day = $4,
end_date_year = $5, end_date_month = $6, end_date_day = $7, gender_id = $8
where artist_id = $1 and type_id = 1'
using i, extract(year from st), extract(month from st), extract(day from st), 
	     extract(year from ed), extract(month from ed), extract(day from ed),
		 gen;

end loop;

end $$;

select * from artists
where type_id = 1