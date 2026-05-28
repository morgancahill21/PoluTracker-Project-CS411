# Detailed Feature Requirements

## Transaction

We have 2 versions, one that's used in our app.py file and another thats the same thing but in SQL.
``` python

db.start_transaction(isolation_level="REPEATABLE READ")

cursor.execute(
    """
    SELECT
      s.state_name,
      COUNT(DISTINCT m.monitor_id) AS total_monitors
    FROM
      state s
      JOIN location l ON s.state_code = l.state_code
      JOIN monitor m ON l.location_id = m.location_id
    WHERE
      s.state_code = %s
    GROUP BY
      s.state_name
    """,
    (state_code,),
)

cursor.execute(
    """
    SELECT
      d.race,
      COUNT(*) AS death_count
    FROM
      death d
    WHERE
      d.state_code = %s
    GROUP BY
      d.race
    ORDER BY
      death_count DESC
    """,
    (state_code,),
)

db.commit()


```

``` sql

BEGIN TRANSACTION;

SELECT
  s.state_name,
  COUNT(DISTINCT m.monitor_id) AS total_monitors
FROM
  state s
  JOIN location l ON s.state_code = l.state_code
  JOIN monitor m ON l.location_id = m.location_id
WHERE
  s.state_code = 'IL'
GROUP BY
  s.state_name;

SELECT
  d.race,
  COUNT(*) AS death_count
FROM
  death d
WHERE
  d.state_code = 'IL'
GROUP BY
  d.race
ORDER BY
  death_count DESC;

COMMIT;

```

## Stored Procedure

``` sql

DELIMITER //

CREATE PROCEDURE GetStatePollutionSummary(IN p_state_code CHAR(2))
BEGIN
    IF p_state_code IS NOT NULL THEN
        
        SELECT 
            'MONITORING' AS record_type,
            s.state_name,
            COUNT(DISTINCT m.monitor_id) AS total_monitors,
            COUNT(DISTINCT l.location_id) AS total_locations,
            
            (
                SELECT pt.pollutant_name
                FROM monitor m1
                JOIN location l1 USING (location_id)
                JOIN pollutant p1 ON m1.pollutant_id = p1.pollutant_id
                JOIN pollutant_type pt ON p1.pollutant_type_id = pt.pollutant_type_id
                WHERE l1.state_code = p_state_code
                GROUP BY pt.pollutant_name
                ORDER BY COUNT(*) DESC
                LIMIT 1
            ) AS mode_pollutant,
            NULL AS mode_race,
            NULL AS mode_gender,
            NULL AS total_deaths
        FROM state s
        JOIN location l ON s.state_code = l.state_code
        JOIN monitor m ON l.location_id = m.location_id
        WHERE s.state_code = p_state_code
        GROUP BY s.state_name
        UNION ALL
        
        SELECT
            'DEATHS' AS record_type,
            s.state_name,
            NULL AS total_monitors,
            NULL AS total_locations,
            NULL AS mode_pollutant,
            
            (
                SELECT d.race
                FROM death d
                JOIN location l USING (county_code)
                WHERE l.state_code = p_state_code
                GROUP BY d.race
                ORDER BY COUNT(*) DESC
                LIMIT 1
            ) AS mode_race,
            
            (
                SELECT d.gender
                FROM death d
                JOIN location l USING (county_code)
                WHERE l.state_code = p_state_code
                GROUP BY d.gender
                ORDER BY COUNT(*) DESC
                LIMIT 1
            ) AS mode_gender,
            
            (
                SELECT COUNT(*)
                FROM death d
                JOIN location l USING (county_code)
                WHERE l.state_code = p_state_code
            ) AS total_deaths
        FROM state s
        WHERE s.state_code = p_state_code;
    END IF;
END //


DELIMITER ;


```

## Trigger

``` sql

DELIMITER //
CREATE TRIGGER after_user_insert
AFTER INSERT ON user
FOR EACH ROW
BEGIN
    IF NEW.first_name IS NOT NULL THEN
        INSERT INTO user_audit (user_id, first_name, last_name)
        VALUES (NEW.user_id, NEW.first_name, NEW.last_name);
    END IF;
END //
DELIMITER ;

```

## Constraints

All of our tables use primary and foreign key constraints. The pollutant table below demonstrates these constraints on both the primary and foreign keys. The other constraints can be found in the Stage 3 document, which shows the code used to create all tables used.

``` sql
CREATE TABLE pollutant (
    pollutant_id INT NOT NULL,
    full_name VARCHAR(255) DEFAULT NULL,
    units_measured VARCHAR(255) DEFAULT NULL,
    pollutant_type_id INT DEFAULT NULL,
    PRIMARY KEY (pollutant_id),
    CONSTRAINT pollutant_ibfk_1 FOREIGN KEY (pollutant_type_id) REFERENCES pollutant_type(pollutant_type_id)
);
```








