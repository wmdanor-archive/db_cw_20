create or replace function calculate_rating_weight(rating numeric, n bigint)
returns numeric
as $$
declare 
positive numeric := round((rating / 10) * n);
negative numeric := n - positive;
begin
if rating is null then return 0;
end if;

return ((positive + 1.9208) / (positive + negative) - 1.96 * SQRT((positive * negative) / (positive + negative) + 0.9604) / (positive + negative)) / (1 + 3.8416 / (positive + negative));
end;
$$ language plpgsql called on null input;