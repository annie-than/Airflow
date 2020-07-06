
CREATE TABLE IF NOT EXISTS public.staging_events(
artist VARCHAR(255) encode text255,
auth VARCHAR(255) encode text255,
firstname VARCHAR(100),
gender VARCHAR(10),
iteminsession INTEGER,
lastname VARCHAR(100),
length numeric,
level VARCHAR(50),
location VARCHAR(255) encode text255,
method VARCHAR(10),
page VARCHAR(50),
registration varchar(100),
sessionid INTEGER,
song VARCHAR(255),
status INTEGER,
ts BIGINT,
useragent VARCHAR(255) encode text255,
userid INTEGER
);


CREATE TABLE IF NOT EXISTS public.staging_songs(
num_songs int,
artist_id text,
artist_latitude numeric,
artist_longitude numeric,
artist_location text,
artist_name varchar(max),
song_id text,
title text,
duration numeric,
year int
);


CREATE TABLE IF NOT EXISTS public.songplays (
songplay_id INTEGER IDENTITY(0,1) PRIMARY KEY,
start_time BIGINT,
userid INTEGER,
level VARCHAR(50),
song_id text,
artist_id text,
sessionid INTEGER,
location VARCHAR(255),
useragent VARCHAR(255)
);


CREATE TABLE IF NOT EXISTS public.songs (
song_id text PRIMARY KEY,
title text,
artist_id text,
year INTEGER,
duration numeric
);


CREATE TABLE IF NOT EXISTS public.users (
user_id INTEGER PRIMARY KEY,
first_name VARCHAR(100),
last_name VARCHAR(100),
gender VARCHAR(10),
level VARCHAR(50)
);


CREATE TABLE IF NOT EXISTS public.artists (
artist_id text PRIMARY KEY,
name varchar(max),
location text,
latitude numeric,
longitude numeric
);


CREATE TABLE IF NOT EXISTS public.time (
start_time timestamp PRIMARY KEY,
hour varchar(25),
day smallint,
week smallint,
month integer,
year smallint,
weekday boolean
);



