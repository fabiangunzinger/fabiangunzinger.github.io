---
title: "SQL"
subtitle: "Cheatsheet"
tags: [sql, cheatsheet]

date: 2021-02-12
featured: false
draft: true

reading_time: false
profile: false
commentable: true
summary: " "

---


## Querying data

```
SELECT col FROM table;
SELECT col1, col2 FROM table;
SELECT * FROM table LIMIT 10;
SELECT DISTINCT col_values FROM table;
```


## Counting

```
SELECT COUNT(*) FROM table;				# Count rows of table
SELECT COUNT(col) FROM table;			# Count non-missing values in col
SELECT COUNT(DISTINCT col) FROM table;	# Count distinct values in col
```


## Filtering

```
SELECT * FROM table WHERE col1 > 2010:	# Get rows for which col1 > 2010
SELECT COUNT(*) FROM table WHERE x < y	# Count number of rows for which x < y
SELECT * FROM table WHERE x > Y AND y < z
SELECT * FROM table WHERE x > Y OR y < z
SELECT * FROM table WHERE x BETWEEN a AND b 	# between a and b inclusive
SELECT * FROM table WHERE x IN (a, b, c)

SELECT title FROM films
WHERE (release_year = 1994 OR release_year = 1995)
AND (certification = 'PG' OR certification = 'R');
```


## Filter based on results from aggregate function

```
SELECT release_year
FROM films
GROUP BY release_year
HAVING COUNT(title) > 10;
```


## Missing values

```
SELECT COUNT(*)
FROM people
WHERE birthdate IS NULL;

SELECT name
FROM people
WHERE birthdate IS NOT NULL;
```


## Wildcards

```
SELECT name
FROM companies
WHERE name LIKE 'Data%';		# % matches zero, one, or many characters

SELECT name
FROM companies
WHERE name LIKE 'DataC_mp';		# _ matches exactly one character

SELECT name
FROM people
WHERE name NOT LIKE 'A%';
```


## Aggregate functions

```
SELECT AVG(budget)		# Also MAX, MIN, SUM,
FROM films;
```


## Aliasing

```
SELECT MAX(budget) AS max_budget,
       MAX(duration) AS max_duration
FROM films;
```


## Arithmetic

```
SELECT COUNT(deathdate) * 100.0 / COUNT(*) AS percentage_dead
FROM people
```


## Order by

```
SELECT title
FROM films
ORDER BY release_year;

SELECT title
FROM films
ORDER BY release_year DESC;
```


## Group by

```
SELECT sex, count(*)
FROM employees
GROUP BY sex;

SELECT release_year, MAX(budget)
FROM films
GROUP BY release_year;
```


## Building a database


## Create tables

```
CREATE TABLE professors (
 firstname text,
 lastname text
);
```


## Alter tables

```
ALTER TABLE table_name
ADD COLUMN column_name data_type;

ALTER TABLE table_name
DROP COLUMN column_name;

ALTER TABLE table_name
RENAME COLUMN old_name TO new_name;

DROP TABLE table_name
```


## Insert values

```
INSERT INTO transactions (transaction_date, amount, fee)
VALUES ('2018-09-24', 5454, '30');

SELECT transaction_date, amount + CAST(fee AS integer) AS net_amount
FROM transactions;
```


## Migrating data

```
INSERT INTO target_table
SELECT DISTINCT column_names
FROM source_table;
```


## Integrity constraints

1. Attribute constraints (data types)
2. Key constraints (primary keys)
3. Referential integrity constraints (enforced through foreign keys)


## Attribute constraints

```
ALTER TABLE professors
ALTER COLUMN firstname
TYPE varchar(16)
USING SUBSTRING(firstname FROM 1 FOR 16)

ALTER TABLE professors
ALTER COLUMN firstname
SET NOT NULL;

ALTER TABLE universities
ADD CONSTRAINT university_shortname_unq UNIQUE(university_shortname);
```


## Key constraints

- Superkey: each combination of attributes that identifies rows uniquely
- Candidate key: a superkey from which no column can be removed
- Primary key: one candidate key chosen to act as primary key
- Surrogate key: artificially created key (eg due to unsuitable candidate keys)
- Foreign keys: points to the primary key of another table

```
ALTER TABLE organizations
RENAME COLUMN organization TO id;
ALTER TABLE organizations
ADD CONSTRAINT organization_pk PRIMARY KEY (id);

ALTER TABLE affiliations
DROP CONSTRAINT affiliations_organizations_id_fkey;

ALTER TABLE professors
ADD COLUMN ID serial

UPDATE table_name
SET new_var = CONCAT(v1, v2);
```

Add a professor_id column that references id in professors table
```
ALTER TABLE affiliations
ADD COLUMN professor_id integer REFERENCES professors (id);
```

Rename the organization column to organization_id
```
ALTER TABLE affiliations
RENAME organization TO organization_id;
```

Add a foreign key on organization_id
```
ALTER TABLE affiliations
ADD CONSTRAINT affiliations_organization_fkey FOREIGN KEY (organization_id) REFERENCES organizations (id);
```

Update professor_id to professors.id where firstname, lastname correspond to rows in professors
```
UPDATE affiliations
SET professor_id = professors.id
FROM professors
WHERE affiliations.firstname = professors.firstname AND affiliations.lastname = professors.lastname;
```


## Referential integrity

```
CREATE TABLE a (
	id integer PRIMARY KEY,
	col_a, varchar(64),
	...,
	b_id integer REFERENCES b (id) VIOLATION SETTING)
```

Where violation setting is one of the following:

| Setting | Explanation |
| - | - |
| ON DELETE NO ACTION   | Deleting id in b that's referenced in a throws error |
| ON DELETE CASCADE     | Deleting id in b deletes references in all tables |
| RESTRICT              | Similar to no action |
| SET NULL              | Set referencing column to null |
| SET DEFAULT           | Set referencing column to default |

## Joins
```
SELECT table_a.column1, table_a.column2, table_b.column1, table_b.column2, ...
FROM table_a
JOIN table_b
ON table_a_foreign_key = table_b_primary_key
WHERE condition;
```
