-- sqlite3 /tmp/tiny.db < schema.sql

DROP TABLE IF EXISTS `topic`;
CREATE TABLE `topic` (
  key_name string primary key,  
  uid string unique,

  created text,
  created_by text,
  name string,
  slug_name string,
  login_required integer,

  published integer,
  updated text,
  updated_by text,

  body text,
  category text not null,
  system text not null
);

DROP TABLE IF EXISTS `system`;
CREATE TABLE `system` (
  key_name string primary key,  
  uid string unique,

  created text,
  created_by text,
  name string,
  slug_name,
  login_required integer,

  published integer,
  updated text,
  updated_by text,

  description string,
  icon_url string
);

