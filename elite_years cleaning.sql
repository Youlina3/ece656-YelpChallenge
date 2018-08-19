delete elite_years from elite_years inner join
    (select e.user_id
    from elite_years e left join user u on e.user_id = u.id where u.id is null) as table1
on elite_years.user_id = table1.user_id;
    
