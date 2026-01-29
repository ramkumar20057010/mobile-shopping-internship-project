create database mob;
use mob;
create table users(
	u_id int primary key auto_increment,
    user_name varchar(255),
    age int,
    mob_no long,
    email varchar(255) unique,
    pass varchar(255),
    created_at timestamp default current_timestamp
    
);
alter table users auto_increment=20301;
insert into users(user_name,age,mob_no,email,pass) 
values("admin","20","4561212882","admin123@gmail.com","admin123");

create table products(
	p_id int primary key auto_increment,
    mob_name varchar(255),
    mob_model varchar(255),
    no_items int ,
    price long,
    image_path varchar(255),
    pmode enum('visible','hide') default 'visible'
	);
alter table products auto_increment=40001;

create table transactions(
	t_id int primary key auto_increment,
    p_items int ,
    total_amount long ,
    tu_id int,
    tp_id int,
    p_status enum('cart','purchased') default 'cart',
    foreign key(tu_id) references users(u_id),
    foreign key(tp_id) references products(p_id),
    p_date timestamp default current_timestamp
	);

alter table transactions auto_increment=60001;

SELECT * FROM users;

SELECT * FROM products;

SELECT * FROM transactions;

 SELECT  p.mob_model, p.price, p.image_path,
    t.p_items, t.total_amount,t.p_status, t.t_id,t.tu_id,t.tp_id
    FROM transactions t JOIN users u on t.tu_id=u.u_id JOIN products p on 
    t.tp_id=p.p_id WHERE t.tu_id='20301';
    
 SELECT  p.mob_model, p.price, p.image_path,
    t.p_items, t.total_amount,t.p_status
    FROM transactions t JOIN users u on t.tu_id=u.u_id JOIN products p on 
    t.tp_id=p.p_id WHERE t.tu_id='20301' ;
    
