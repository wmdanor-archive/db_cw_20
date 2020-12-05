select count(*) from (

select users.user_id, record_id, username, registration_date, listening_date from users
inner join listening_history on users.user_id = listening_history.user_id
--where users.username = 'username 1000'

) q