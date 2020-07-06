class SqlQueries:

    songplay_table_insert = ("""       
        SELECT events.ts, events.userid, events.level,  songs.song_id, songs.artist_id, events.sessionid, events.location, events.useragent
        FROM staging_events as events
        JOIN staging_songs as songs ON (events.artist=songs.artist_name)
                                    AND (events.song=songs.title)
                                    AND (events.length = songs.duration)
                                    WHERE events.page='NextSong';
        """)

    
    user_table_insert = ("""        
        SELECT userid, firstname, lastname, gender, level
        FROM staging_events
        WHERE staging_events.userid is not NULL
        """)
    

    song_table_insert = ("""       
        SELECT song_id, title, artist_id, year, duration
        FROM staging_songs;
        """)

    artist_table_insert = ("""
        SELECT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
        FROM staging_songs;
        """)

    
    time_table_insert = ("""
        SELECT 
        atime.start_time, 
        EXTRACT(HOUR from atime.start_time), 
        EXTRACT(DAY from atime.start_time),
        EXTRACT(WEEK from atime.start_time),
        EXTRACT(MONTH from atime.start_time),
        EXTRACT(YEAR from atime.start_time),
        EXTRACT(DOW from atime.start_time)
        FROM (SELECT TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS start_time FROM staging_events) as atime;
        """)