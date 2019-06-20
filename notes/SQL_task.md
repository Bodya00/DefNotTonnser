Part 1 Databases
## Test db
For this task I want to create database for testing my queries:
	`create database bike_service;`

####Creating tables
I assumed the following types and length
I assume real database(from defnottonnser) is set up correctly and I my field lengths are OK.
Same for not null constraints.

Scooters:
```postgresql
create table scooters (
    id serial primary key,
    name varchar(200),
    city varchar(100),
    model varchar(300),
    battery_capacity real
    );
```

Customers:
```postgresql
	create table customers (
		id serial primary key,
		name varchar(200),
		platform_token varchar(100)
		);
-- I used length 100 cause there could be more platforms in this table(at least in the future)
```
Rental reservations:
```postgresql
create table rental_reservations(
	scooter_id integer references scooters(id),
	customer_id integer references customers(id),
	start_datetime timestamp with time zone,
	end_datetime timestamp with time zone
	);
  -- time zone will be usefull if our service is working in more than one time zone
  -- there is no separate id column in the description for this table
  -- we can't make primary key from scooter_id in combination with customer_id because one user can obviously use one bike multiple times
	-- if I could change schema, I would add simpel id primary key for this table to identify reservations(IMO it is case similiar to sort of transactions table)
```
####Setting up some test data
Scooters
```postgresql
insert into scooters (name, city, model, battery_capacity)
values ('scooter1', 'city1', 'model1', 100),
	('scooter2', 'city1', 'model2', 150),
	('scooter3', 'Copenhagen', 'model1', 100),
	('scooter4', 'Copenhagen', 'model2', 150),
	('scooter5', 'city3', 'model2', 150);
```
Customers
```postgresql
insert into customers (name,platform_token)
values ('android_customer1', repeat('t', 12)),
	('android_customer2', repeat('t', 12)),
	('android_customer3', repeat('t', 12)),
	('iphone_customer1', repeat('t', 30)),
	('iphone_customer2', repeat('t', 30)),
	('iphone_customer3', repeat('t', 30));
```
Rental reservations
```postgresql
insert into rental_reservations (scooter_id, customer_id, start_datetime, end_datetime)
values (1,1, '2019-01-01 07:00', '2019-01-01 12:00'),
	(1,1,'2019-07-08 12:00', '2019-07-08 17:00' ),
	(2,1, '2019-01-03 07:00', '2019-01-03 12:00'),
	(1,2, '2019-07-07 07:00', '2019-07-08 12:00'),
	(3,2, '2019-07-10 07:00', '2019-07-10 12:00'),
	(2,3, '2019-07-14 07:00', '2019-07-15 00:00'),
	(2,3, '2019-07-07 07:00', '2019-07-16 12:00'),
	(5,4, '2019-07-15 00:00', '2019-07-15 12:00'),
	(5,5, '2019-01-02 07:00', '2019-01-02 12:00');
```
####Queries:
First:
```postgresql
select scooters.name, model, battery_capacity, start_datetime, end_datetime
from scooters
inner join rental_reservations on scooters.id = rental_reservations.scooter_id
	and (start_datetime <= '2019-07-15 00:00' and end_datetime >='2019-07-08 12:00')
inner join customers on rental_reservations.customer_id = customers.id and length(platform_token) = 12
where city = 'Copenhagen'
```

my result:

|  name  |  model  |  battery_capacity  |
|---|---|---|
|  scooter3  |  model1  |  100  |
notes:

I used filtering on join because we dont need rest of rows and in larger tables we can decrease execution time.

Second:
```postgresql
select scooters.id, customers.id
from scooters
cross join customers
    except (select scooter_id, customer_id from rental_reservations)
```
my result:

23 rows from example database

notes:

Getting all possible combinations of scooters_id and customers_id and then getting the difference with the combinations from rental reservations.

Third:
```postgresql
select length(platform_token), percentile_cont(0.5) within group (order by end_datetime - start_datetime)
from rental_reservations
left join customers c2 on rental_reservations.customer_id = c2.id
group by length(platform_token)
```
my result:

|length|percentile_cont|
| --- | --- |
|12|0 years 0 mons 0 days 5 hours 0 mins 0.00 secs|
|30|0 years 0 mons 0 days 8 hours 30 mins 0.00 secs|


notes:

Because the median type(numerical or discrete) is not specified I am going to assume it is numerical.

