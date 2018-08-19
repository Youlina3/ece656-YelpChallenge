delete user from user inner join 
    (select tmp.user_id from user u inner join
       (select user_id, count(*) total from review group by user_id) as tmp
on u.id = tmp.user_id where tmp.total > u.review_count) as table1
on user.id = table1.user_id;


