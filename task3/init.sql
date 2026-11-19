-- Runs once, when the database volume is first created.
create table products (
    name varchar(20) primary key,
    price integer not null,
    quantity integer not null
);
