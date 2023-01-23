create table events (
	e_id int primary key unique auto_increment,
    event_name varchar(255),
    start_d varchar(255),
    end_d varchar(255)
    );
    
create table movements (
	m_id int primary key unique auto_increment,
    mvmt_type int references mvmt_types (mt_id),
    event_id int references events (e_id),
    call_sign varchar(255),
    sup_cargo varchar(255),
    req_unit varchar(255),
    sup_unit varchar(255),
    orgin varchar(255),
    destination varchar(255),
    route varchar(255),
    status varchar(255),
    mhe_req boolean,
    start_dt varchar(255),
    end_dt varchar(255),
    remarks varchar(255),
    vics varchar(255),
    pax varchar(255)
    );
    
create table user_info (
	u_id int primary key unique auto_increment,
    u_name varchar(255),
    u_pass varchar(255),
    unit varchar(255)
    );
    
create table assets (
	serial_num varchar(255) primary key unique,
    mvmt_num int references movements(m_id),
    make varchar(255),
    model varchar(255),
    in_use boolean,
    start_t varchar(255),
    end_t varchar(255),
    deadlined boolean
    );

create table management (
	id int primary key unique auto_increment,
    mvmt_num int references movements(m_id),
    driver_name varchar(255),
    vc_name varchar(255),
    asset_id int references assets(serial_num),
    status varchar(255)
    );

create table drivers (
	d_id int primary key unique auto_increment,
    name varchar(255)
);

create table mvmt_types (
	mt_id int primary key unique auto_increment,
    mvmt_name varchar(255)
);

create table current_lto (
	id int primary key unique auto_increment,
    lto int
);