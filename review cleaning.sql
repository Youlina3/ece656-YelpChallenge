delete review from review inner join 
     (select review.business_id 
     from review left join business on review.business_id = business.id where business.id is null) as table1
on review.business_id = table1.business_id;





delete review from review inner join 
     (select review.user_id 
     from review left join user on review.user_id = user.id where user.id is null) as table1
on review.user_id = table1.user_id;


