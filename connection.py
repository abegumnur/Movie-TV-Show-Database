import mysql.connector

def initialize_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="begum57",
    )

    cursor = mydb.cursor()
    create_database(cursor)
    create_table(cursor, mydb)

    return mydb, cursor

def create_database(cursor):
    cursor.execute("SHOW DATABASES")
    temp = cursor.fetchall()
    databases = [item[0] for item in temp]
    if "tv_show_movie_db" not in databases:
        cursor.execute("CREATE DATABASE tv_show_movie_db")

    cursor.execute("USE tv_show_movie_db")
    print("DATABASE CONNECTED")

def create_table(cursor, conn):
    print("TABLE CONTROL")
    cursor.execute("SHOW TABLES")
    temp = cursor.fetchall()
    tables = [item[0].lower() for item in temp]  # Ensure case-insensitive comparison

    if "user" not in tables:
        cursor.execute("""CREATE TABLE User(
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50),
            password VARCHAR(50),
            email VARCHAR(100),
            role VARCHAR(20)
        )""")
        conn.commit()

    if "cast" not in tables:
        cursor.execute("""CREATE TABLE Cast(
            cast_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100),
            role VARCHAR(100)
        )""")
        conn.commit()

    if "crew" not in tables:
        cursor.execute("""CREATE TABLE Crew(
            crew_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100),
            role VARCHAR(100)
        )""")
        conn.commit()

    if "movie" not in tables:
        cursor.execute("""CREATE TABLE Movie(
            movie_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            description TEXT,
            release_date DATE,
            genre VARCHAR(50),
            rating FLOAT,
            director_id INT,
            FOREIGN KEY (director_id) REFERENCES Director(director_id)
        )""")
        conn.commit()

    if "tv_show" not in tables:
        cursor.execute("""CREATE TABLE TV_Show(
            show_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            description TEXT,
            release_date DATE,
            genre VARCHAR(50),
            rating FLOAT,
            director_id INT,
            FOREIGN KEY (director_id) REFERENCES Director(director_id)
        )""")
        conn.commit()

    if "review" not in tables:
        cursor.execute("""CREATE TABLE Review(
            review_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            show_id INT,
            movie_id INT,
            rating FLOAT,
            review_text VARCHAR(255),
            review_date DATE,
            FOREIGN KEY (user_id) REFERENCES User(user_id),
            FOREIGN KEY (show_id) REFERENCES TV_Show(show_id),
            FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
        )""")
        conn.commit()

    if "watchlist" not in tables:
        cursor.execute("""CREATE TABLE Watchlist(
            watchlist_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            name VARCHAR(100),
            FOREIGN KEY (user_id) REFERENCES User(user_id)
        )""")
        conn.commit()

    if "watchlist_item" not in tables:
        cursor.execute("""CREATE TABLE Watchlist_Item(
            watchlist_item_id INT AUTO_INCREMENT PRIMARY KEY,
            watchlist_id INT,
            show_id INT,
            movie_id INT,
            FOREIGN KEY (watchlist_id) REFERENCES Watchlist(watchlist_id),
            FOREIGN KEY (show_id) REFERENCES TV_Show(show_id),
            FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
        )""")
        conn.commit()

    if "recommendation" not in tables:
        cursor.execute("""CREATE TABLE Recommendation(
            recommendation_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            show_id INT,
            movie_id INT,
            FOREIGN KEY (user_id) REFERENCES User(user_id),
            FOREIGN KEY (show_id) REFERENCES TV_Show(show_id),
            FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
        )""")
        conn.commit()

    if "critic" not in tables:
        cursor.execute("""CREATE TABLE Critic(
            critic_id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT,
            publication VARCHAR(100),
            review_count INT,
            average_rating FLOAT,
            FOREIGN KEY (user_id) REFERENCES User(user_id)
        )""")
        conn.commit()


    if "director" not in tables:
        cursor.execute("""CREATE TABLE Director(
            director_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100)
        )""")
        conn.commit()

    if "user_change_log" not in tables:
        cursor.execute("""CREATE TABLE User_Change_Log(
            log_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            old_username VARCHAR(50),
            new_username VARCHAR(50),
            change_date DATETIME,
            FOREIGN KEY (user_id) REFERENCES User(user_id)
        )""")
        conn.commit()

    # Adding foreign keys
    alter_review_table_query = """
    ALTER TABLE Review
    ADD CONSTRAINT fk_review_user FOREIGN KEY (user_id) REFERENCES User(user_id),
    ADD CONSTRAINT fk_review_show FOREIGN KEY (show_id) REFERENCES TV_Show(show_id),
    ADD CONSTRAINT fk_review_movie FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
    """
    cursor.execute("SHOW CREATE TABLE Review")
    review_table_definition = cursor.fetchone()[1]
    if "fk_review_user" not in review_table_definition:
        cursor.execute(alter_review_table_query)

    # Add the stored procedures, triggers, and views
    create_procedures(cursor, conn)
    create_triggers(cursor, conn)
    create_views(cursor, conn)
    add_views(cursor, conn)
    add_procedures(cursor, conn)

    print("TABLES AND CONSTRAINTS CREATED")

def create_procedures(cursor, conn):
    cursor.execute("SHOW PROCEDURE STATUS WHERE Db = 'tv_show_movie_db'")
    procedures = [item[1] for item in cursor.fetchall()]

    if "AddDirector" not in procedures:
        cursor.execute("""CREATE PROCEDURE AddDirector(IN director_name VARCHAR(100))
                        BEGIN
                            INSERT INTO Director(name) VALUES(director_name);
                        END;""")
        conn.commit()

def create_triggers(cursor, conn):
    cursor.execute("SHOW TRIGGERS")
    triggers = [item[0] for item in cursor.fetchall()]

    if "check_rating_trigger" not in triggers:
        cursor.execute("""CREATE TRIGGER check_rating_trigger 
                          BEFORE INSERT ON Review
                          FOR EACH ROW
                          BEGIN
                              IF NEW.rating < 0 OR NEW.rating > 10 THEN
                                  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Rating must be between 0 and 10';
                              END IF;
                          END;""")
        conn.commit()

    if "unique_username_trigger" not in triggers:
        cursor.execute("""CREATE TRIGGER unique_username_trigger
                          BEFORE INSERT ON User
                          FOR EACH ROW
                          BEGIN
                              DECLARE user_count INT;
                              SELECT COUNT(*) INTO user_count FROM User WHERE username = NEW.username;
                              IF user_count > 0 THEN
                                  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Username already exists';
                              END IF;
                          END;""")
        conn.commit()

    if "update_avg_rating_trigger" not in triggers:
        cursor.execute("""CREATE TRIGGER update_avg_rating_trigger
                          AFTER INSERT ON Review
                          FOR EACH ROW
                          BEGIN
                              IF NEW.movie_id IS NOT NULL THEN
                                  UPDATE Movie SET rating = (SELECT AVG(rating) FROM Review WHERE movie_id = NEW.movie_id) WHERE movie_id = NEW.movie_id;
                              ELSEIF NEW.show_id IS NOT NULL THEN
                                  UPDATE TV_Show SET rating = (SELECT AVG(rating) FROM Review WHERE show_id = NEW.show_id) WHERE show_id = NEW.show_id;
                              END IF;
                          END;""")
        conn.commit()

    if "prevent_deletion_trigger" not in triggers:
        cursor.execute("""CREATE TRIGGER prevent_deletion_trigger
                          BEFORE DELETE ON Movie
                          FOR EACH ROW
                          BEGIN
                              DECLARE review_count INT;
                              SELECT COUNT(*) INTO review_count FROM Review WHERE movie_id = OLD.movie_id;
                              IF review_count > 0 THEN
                                  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot delete movie with reviews';
                              END IF;
                          END;""")
        conn.commit()

    if "log_user_changes_trigger" not in triggers:
        cursor.execute("""CREATE TRIGGER log_user_changes_trigger
                          AFTER UPDATE ON User
                          FOR EACH ROW
                          BEGIN
                              INSERT INTO User_Change_Log (user_id, old_username, new_username, change_date)
                              VALUES (NEW.user_id, OLD.username, NEW.username, NOW());
                          END;""")
        conn.commit()

def create_views(cursor, conn):
    cursor.execute("SHOW FULL TABLES IN tv_show_movie_db WHERE TABLE_TYPE LIKE 'VIEW';")
    existing_views = [item[0].lower() for item in cursor.fetchall()]  # Ensure case-insensitive comparison

    if "usermoviereviews" not in existing_views:
        cursor.execute("""CREATE VIEW UserMovieReviews AS
                          SELECT User.username, Movie.title, Review.rating, Review.review_text, Review.review_date
                          FROM User
                          JOIN Review ON User.user_id = Review.user_id
                          JOIN Movie ON Review.movie_id = Movie.movie_id;""")
        conn.commit()

    if "usershowreviews" not in existing_views:
        cursor.execute("""CREATE VIEW UserShowReviews AS
                          SELECT User.username, TV_Show.title, Review.rating, Review.review_text, Review.review_date
                          FROM User
                          JOIN Review ON User.user_id = Review.user_id
                          JOIN TV_Show ON Review.show_id = TV_Show.show_id;""")
        conn.commit()

    if "movie_avg_ratings" not in existing_views:
        cursor.execute("""CREATE VIEW Movie_Avg_Ratings AS
                          SELECT Movie.title, AVG(Review.rating) AS avg_rating
                          FROM Movie
                          JOIN Review ON Movie.movie_id = Review.movie_id
                          GROUP BY Movie.title;""")
        conn.commit()

    if "show_avg_ratings" not in existing_views:
        cursor.execute("""CREATE VIEW Show_Avg_Ratings AS
                          SELECT TV_Show.title, AVG(Review.rating) AS avg_rating
                          FROM TV_Show
                          JOIN Review ON TV_Show.show_id = Review.show_id
                          GROUP BY TV_Show.title;""")
        conn.commit()

    if "user_review_counts" not in existing_views:
        cursor.execute("""CREATE VIEW User_Review_Counts AS
                          SELECT User.username, COUNT(Review.review_id) AS review_count
                          FROM User
                          JOIN Review ON User.user_id = Review.user_id
                          GROUP BY User.username;""")
        conn.commit()

    if "movies_most_reviews" not in existing_views:
        cursor.execute("""CREATE VIEW Movies_Most_Reviews AS
                          SELECT Movie.title, COUNT(Review.review_id) AS review_count
                          FROM Movie
                          JOIN Review ON Movie.movie_id = Review.movie_id
                          GROUP BY Movie.title
                          ORDER BY review_count DESC
                          LIMIT 10;""")
        conn.commit()

    if "shows_most_reviews" not in existing_views:
        cursor.execute("""CREATE VIEW Shows_Most_Reviews AS
                          SELECT TV_Show.title, COUNT(Review.review_id) AS review_count
                          FROM TV_Show
                          JOIN Review ON TV_Show.show_id = Review.show_id
                          GROUP BY TV_Show.title
                          ORDER BY review_count DESC
                          LIMIT 10;""")
        conn.commit()

def add_views(cursor, conn):
    cursor.execute("""
        CREATE OR REPLACE VIEW MostWatchedMovies AS
        SELECT M.title, COUNT(WI.movie_id) AS watch_count
        FROM Watchlist_Item WI
        JOIN Movie M ON WI.movie_id = M.movie_id
        GROUP BY WI.movie_id
        ORDER BY watch_count DESC
        LIMIT 10
    """)
    cursor.execute("""
        CREATE OR REPLACE VIEW MostWatchedShows AS
        SELECT S.title, COUNT(WI.show_id) AS watch_count
        FROM Watchlist_Item WI
        JOIN TV_Show S ON WI.show_id = S.show_id
        GROUP BY WI.show_id
        ORDER BY watch_count DESC
        LIMIT 10
    """)
    cursor.execute("""
        CREATE OR REPLACE VIEW MostReviewedMovies AS
        SELECT M.title, COUNT(R.movie_id) AS review_count
        FROM Review R
        JOIN Movie M ON R.movie_id = M.movie_id
        GROUP BY R.movie_id
        ORDER BY review_count DESC
        LIMIT 10
    """)
    cursor.execute("""
        CREATE OR REPLACE VIEW MostReviewedShows AS
        SELECT S.title, COUNT(R.show_id) AS review_count
        FROM Review R
        JOIN TV_Show S ON R.show_id = S.show_id
        GROUP BY R.show_id
        ORDER BY review_count DESC
        LIMIT 10
    """)
    cursor.execute("""
        CREATE OR REPLACE VIEW WorstRatedMovies AS
        SELECT M.title, AVG(R.rating) AS avg_rating
        FROM Review R
        JOIN Movie M ON R.movie_id = M.movie_id
        GROUP BY R.movie_id
        ORDER BY avg_rating ASC
        LIMIT 10
    """)
    cursor.execute("""
        CREATE OR REPLACE VIEW WorstRatedShows AS
        SELECT S.title, AVG(R.rating) AS avg_rating
        FROM Review R
        JOIN TV_Show S ON R.show_id = S.show_id
        GROUP BY R.show_id
        ORDER BY avg_rating ASC
        LIMIT 10
    """)
    conn.commit()

def add_procedures(cursor, conn):

    cursor.execute("SHOW PROCEDURE STATUS WHERE Db = 'tv_show_movie_db'")
    procedures = [item[1] for item in cursor.fetchall()]

    cursor.execute("DROP PROCEDURE IF EXISTS GetCastAndCrew")
    cursor.execute("""
        CREATE PROCEDURE GetCastAndCrew(IN show_movie_id INT, IN type CHAR(1))
        BEGIN
            IF type = 'M' THEN
                SELECT C.name, C.role
                FROM Cast C
                JOIN Movie_Cast MC ON C.cast_id = MC.cast_id
                WHERE MC.movie_id = show_movie_id;
            ELSEIF type = 'S' THEN
                SELECT C.name, C.role
                FROM Crew C
                JOIN TV_Show_Crew SC ON C.crew_id = SC.crew_id
                WHERE SC.show_id = show_movie_id;
            END IF;
        END
    """)
    conn.commit()

    cursor.execute("DROP PROCEDURE IF EXISTS AddMovieWithDirector")
    cursor.execute("""
        CREATE PROCEDURE AddMovieWithDirector(IN title VARCHAR(255), IN description TEXT, IN release_date DATE, 
                                              IN genre VARCHAR(50), IN rating FLOAT, IN director_name VARCHAR(100))
        BEGIN
            DECLARE director_id INT;
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
            BEGIN
                ROLLBACK;
                RESIGNAL;
            END;
            START TRANSACTION;
            INSERT INTO Director (name) VALUES (director_name);
            SET director_id = LAST_INSERT_ID();
            INSERT INTO Movie (title, description, release_date, genre, rating, director_id) 
            VALUES (title, description, release_date, genre, rating, director_id);
            COMMIT;
        END
    """)
    conn.commit()

    cursor.execute("DROP PROCEDURE IF EXISTS AddShowWithDirector")
    cursor.execute("""
        CREATE PROCEDURE AddShowWithDirector(IN title VARCHAR(255), IN description TEXT, IN release_date DATE, 
                                             IN genre VARCHAR(50), IN rating FLOAT, IN director_name VARCHAR(100))
        BEGIN
            DECLARE director_id INT;
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
            BEGIN
                ROLLBACK;
                RESIGNAL;
            END;
            START TRANSACTION;
            INSERT INTO Director (name) VALUES (director_name);
            SET director_id = LAST_INSERT_ID();
            INSERT INTO TV_Show (title, description, release_date, genre, rating, director_id) 
            VALUES (title, description, release_date, genre, rating, director_id);
            COMMIT;
        END
    """)
    conn.commit()

    cursor.execute("DROP PROCEDURE IF EXISTS AddReviewAndUpdateRating")
    cursor.execute("""
        CREATE PROCEDURE AddReviewAndUpdateRating(IN user_id INT, IN show_id INT, IN movie_id INT, IN rating FLOAT, 
                                                  IN review_text VARCHAR(255), IN review_date DATE)
        BEGIN
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
            BEGIN
                ROLLBACK;
                RESIGNAL;
            END;
            START TRANSACTION;
            INSERT INTO Review (user_id, show_id, movie_id, rating, review_text, review_date) 
            VALUES (user_id, show_id, movie_id, rating, review_text, review_date);
            IF movie_id IS NOT NULL THEN
                UPDATE Movie SET rating = (SELECT AVG(rating) FROM Review WHERE movie_id = movie_id) WHERE movie_id = movie_id;
            ELSEIF show_id IS NOT NULL THEN
                UPDATE TV_Show SET rating = (SELECT AVG(rating) FROM Review WHERE show_id = show_id) WHERE show_id = show_id;
            END IF;
            COMMIT;
        END
    """)
    conn.commit()

    if "GenerateRecommendations" not in procedures:
        cursor.execute("""
            CREATE PROCEDURE GenerateRecommendations(IN userId INT)
            BEGIN
                DECLARE finished INTEGER DEFAULT 0;
                DECLARE movieId INT;
                DECLARE showId INT;

                DECLARE cur CURSOR FOR
                    SELECT movie_id FROM Review WHERE user_id = userId
                    UNION
                    SELECT movie_id FROM Watchlist_Item WHERE watchlist_id IN (SELECT watchlist_id FROM Watchlist WHERE user_id = userId);

                DECLARE cur2 CURSOR FOR
                    SELECT show_id FROM Review WHERE user_id = userId
                    UNION
                    SELECT show_id FROM Watchlist_Item WHERE watchlist_id IN (SELECT watchlist_id FROM Watchlist WHERE user_id = userId);

                DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;

                OPEN cur;

                recommendation_loop: LOOP
                    FETCH cur INTO movieId;
                    IF finished = 1 THEN
                        LEAVE recommendation_loop;
                    END IF;
                    INSERT INTO Recommendation (user_id, movie_id) VALUES (userId, movieId) ON DUPLICATE KEY UPDATE movie_id = movieId;
                END LOOP recommendation_loop;

                CLOSE cur;

                SET finished = 0;

                OPEN cur2;

                recommendation_loop2: LOOP
                    FETCH cur2 INTO showId;
                    IF finished = 1 THEN
                        LEAVE recommendation_loop2;
                    END IF;
                    INSERT INTO Recommendation (user_id, show_id) VALUES (userId, showId) ON DUPLICATE KEY UPDATE show_id = showId;
                END LOOP recommendation_loop2;

                CLOSE cur2;
            END
        """)
        conn.commit()
# def setup_privileges_and_roles(cursor, conn):
#     # Create roles
#     cursor.execute("CREATE ROLE IF NOT EXISTS admin_role")
#     cursor.execute("CREATE ROLE IF NOT EXISTS critic_role")
#     cursor.execute("CREATE ROLE IF NOT EXISTS user_role")
#
#     # Grant privileges to roles
#     cursor.execute("GRANT ALL PRIVILEGES ON tv_show_movie_db.* TO 'admin_role'")
#     cursor.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON tv_show_movie_db.Review TO 'critic_role'")
#     cursor.execute("GRANT SELECT ON tv_show_movie_db.* TO 'user_role'")
#
#     # Assign roles to users (example)
#     cursor.execute("GRANT 'admin_role' TO 'admin_user'@'localhost'")
#     cursor.execute("GRANT 'critic_role' TO 'critic_user'@'localhost'")
#     cursor.execute("GRANT 'user_role' TO 'regular_user'@'localhost'")
#
#     conn.commit()

def dropAllDB():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="begum57",
    )

    cursor = mydb.cursor()
    cursor.execute("SHOW DATABASES")
    temp = cursor.fetchall()
    dbs = [item[0] for item in temp]
    if "tv_show_movie_db" in dbs:
        cursor.execute("DROP DATABASE tv_show_movie_db")
    print("DATABASE DROPPED")

def clearEntries(entries):
    k = len(entries)
    for i in range(k):
        entries.pop().delete(0, END)

if __name__ == "__main__":
    mydb, cursor = initialize_connection()
    # setup_privileges_and_roles(cursor, mydb)
    Main_App().run()