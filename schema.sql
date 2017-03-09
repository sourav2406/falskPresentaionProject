drop table if exists user_info;
create table user_info (
  id integer primary key autoincrement,
  name text not null,
  password text not null,
  email text,
  phone integer
);