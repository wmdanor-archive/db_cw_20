insert into users (username, password_hash, registration_date, is_active, full_name, birth_date, gender_id)
select 'username '||s.a, 'password hash '||s.a, 
(date '2020-1-1' - '4 years'::interval + justify_interval('4 years'::interval/(3500 - 1 + 1) * s.a))::date,
toss_a_coin(0.95), case when toss_a_coin(0.6) then 'full name '||s.a else null::text end,
case when toss_a_coin(0.4) then (timestamp '1970-1-1' + random()*(timestamp '2004-1-1' - timestamp '1970-1-1'))::date
else null::date end, case when toss_a_coin(0.5) then floor(random()*(3) + 1)::smallint else null::smallint end
from generate_series(1, 3500) as s(a)