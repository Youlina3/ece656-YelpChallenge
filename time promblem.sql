delete from elite_years
where year < 2004 || year > 2018; 

delete from review
where date < '2004-09-30' || date > '2018-04-30';

delete from tip
where date < '2004-09-30' || date > '2018-04-30';

delete from user
where yelping_since < '2004-09-30' || yelping_since > '2018-04-30';



