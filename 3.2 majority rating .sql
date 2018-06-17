drop view if exists avgstar_usernum;

create view avgstar_usernum as 
select average_stars, count(id) as usernum
from user
group by average_stars
order by average_stars desc;


DROP PROCEDURE IF EXISTS generate_series_base;
DELIMITER $$
CREATE PROCEDURE generate_series_base (IN n_first BIGINT, IN n_last BIGINT)
BEGIN
    -- Call generate_series_n_base stored procedure with "1" as "n_increment".
    CALL generate_series_n_base(n_first, n_last, 1);
END $$
DELIMITER ;

DROP PROCEDURE IF EXISTS generate_series_n_base;
DELIMITER $$
CREATE PROCEDURE generate_series_n_base (IN n_first BIGINT, IN n_last BIGINT, IN n_increment BIGINT)
BEGIN
    -- Create tmp table
    drop table if exists series_tmp;
    CREATE TABLE series_tmp (
        series bigint
    ) engine = memory;
    
    WHILE n_first <= n_last DO
        -- Insert in tmp table
        INSERT INTO series_tmp (series) VALUES (n_first);

        -- Increment value by one
        SET n_first = n_first + n_increment; 
    END WHILE;
END $$
DELIMITER ;

call generate_series_base(1,5);

select concat(g.series-1, '-',g.series) as avg_star, sum(usernum) as user_count
from avgstar_usernum as a, series_tmp as g
where a.average_stars <= g.series and a.average_stars > g.series-1
group by g.series
order by g.series;

