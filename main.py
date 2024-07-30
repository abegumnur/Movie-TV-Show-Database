from tkinter import *
from tkinter import messagebox
from connection import *

mydb, cursor = initialize_connection()
mydb.autocommit = False

def close_previous_results(cursor):
    while cursor.nextset():
        pass

class Critic_App:
    def __init__(self, critic_id):
        self.critic_id = critic_id
        self.entries = []

        self.window = Tk()
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        self.window.config(background="#FFC0CB")
        self.window.title("Critic")

        home_button = Button(self.window, text="Home", command=self.go_home)
        home_button.pack()

        self.entries = []
        self.create_scrollable_frame()

        list_movie_button = Button(self.window, text="List Movies", width=12, height=3, command=self.listMovies)
        list_movie_button.pack()

        list_show_button = Button(self.window, text="List Shows", width=12, height=3, command=self.listShows)
        list_show_button.pack()

        write_review_button = Button(self.window, text="Write Review", width=12, height=3, command=self.writeReview)
        write_review_button.pack()

        edit_review_button = Button(self.window, text="Edit Review", width=12, height=3, command=self.editReview)
        edit_review_button.pack()

        delete_review_button = Button(self.window, text="Delete Review", width=12, height=3, command=self.deleteReview)
        delete_review_button.pack()

        view_reviews_button = Button(self.window, text="View My Reviews", width=15, height=3, command=self.viewReviews)
        view_reviews_button.pack()

    def create_scrollable_frame(self):
        self.canvas = Canvas(self.window)
        self.scrollable_frame = Frame(self.canvas)
        self.scrollbar = Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def listMovies(self):
        global cursor
        clearEntries(self.entries)

        cursor.execute("SELECT * FROM Movie")
        movies = cursor.fetchall()  # Fetch all rows at once

        column_names = [desc[0] for desc in cursor.description]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, movie in enumerate(movies, start=1):
            for j, value in enumerate(movie):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def listShows(self):
        global cursor
        clearEntries(self.entries)

        cursor.execute("SELECT * FROM TV_Show")
        shows = cursor.fetchall()  # Fetch all rows at once

        column_names = [desc[0] for desc in cursor.description]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, show in enumerate(shows, start=1):
            for j, value in enumerate(show):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def writeReview(self):
        review_window = Tk()
        review_window.geometry("400x400")
        review_window.title("Write Review")

        show_id_label = Label(review_window, text="Show ID (if applicable)")
        show_id_label.pack()
        show_id_entry = Entry(review_window)
        show_id_entry.pack()

        movie_id_label = Label(review_window, text="Movie ID (if applicable)")
        movie_id_label.pack()
        movie_id_entry = Entry(review_window)
        movie_id_entry.pack()

        rating_label = Label(review_window, text="Rating")
        rating_label.pack()
        rating_entry = Entry(review_window)
        rating_entry.pack()

        review_text_label = Label(review_window, text="Review Text")
        review_text_label.pack()
        review_text_entry = Entry(review_window)
        review_text_entry.pack()

        review_date_label = Label(review_window, text="Review Date (YYYY-MM-DD)")
        review_date_label.pack()
        review_date_entry = Entry(review_window)
        review_date_entry.pack()

        save_button = Button(review_window, text="Save", command=lambda: self.save_review(show_id_entry, movie_id_entry, rating_entry, review_text_entry, review_date_entry, review_window))
        save_button.pack()

    def save_review(self, show_id_entry, movie_id_entry, rating_entry, review_text_entry, review_date_entry, review_window):
        show_id = int(show_id_entry.get()) if show_id_entry.get() else None
        movie_id = int(movie_id_entry.get()) if movie_id_entry.get() else None
        rating = float(rating_entry.get())
        review_text = review_text_entry.get()
        review_date = review_date_entry.get()

        global cursor, mydb
        cursor.execute("""INSERT INTO Review (user_id, show_id, movie_id, rating, review_text, review_date) 
                          VALUES (%s, %s, %s, %s, %s, %s)""",
                       (self.critic_id, show_id, movie_id, rating, review_text, review_date))
        mydb.commit()
        review_window.destroy()

    def editReview(self):
        edit_review_window = Tk()
        edit_review_window.geometry("400x400")
        edit_review_window.title("Edit Review")

        review_id_label = Label(edit_review_window, text="Review ID")
        review_id_label.pack()
        review_id_entry = Entry(edit_review_window)
        review_id_entry.pack()

        rating_label = Label(edit_review_window, text="New Rating")
        rating_label.pack()
        rating_entry = Entry(edit_review_window)
        rating_entry.pack()

        review_text_label = Label(edit_review_window, text="New Review Text")
        review_text_label.pack()
        review_text_entry = Entry(edit_review_window)
        review_text_entry.pack()

        save_button = Button(edit_review_window, text="Save", command=lambda: self.update_review(review_id_entry, rating_entry, review_text_entry, edit_review_window))
        save_button.pack()

    def update_review(self, review_id_entry, rating_entry, review_text_entry, edit_review_window):
        review_id = int(review_id_entry.get())
        new_rating = float(rating_entry.get())
        new_review_text = review_text_entry.get()

        global cursor, mydb
        cursor.execute("""UPDATE Review SET rating = %s, review_text = %s WHERE review_id = %s AND user_id = %s""",
                       (new_rating, new_review_text, review_id, self.critic_id))
        mydb.commit()
        edit_review_window.destroy()

    def deleteReview(self):
        delete_review_window = Tk()
        delete_review_window.geometry("400x400")
        delete_review_window.title("Delete Review")

        review_id_label = Label(delete_review_window, text="Review ID")
        review_id_label.pack()
        review_id_entry = Entry(delete_review_window)
        review_id_entry.pack()

        delete_button = Button(delete_review_window, text="Delete", command=lambda: self.remove_review(review_id_entry, delete_review_window))
        delete_button.pack()

    def remove_review(self, review_id_entry, delete_review_window):
        review_id = int(review_id_entry.get())

        global cursor, mydb
        cursor.execute("""DELETE FROM Review WHERE review_id = %s AND user_id = %s""", (review_id, self.critic_id))
        mydb.commit()
        delete_review_window.destroy()

    def viewReviews(self):
        global cursor
        # Debug print to verify critic_id
        print(f"Critic ID: {self.critic_id}")
        close_previous_results(cursor)
        clearEntries(self.entries)

        query = """
            SELECT R.review_id, U.username, M.title AS movie_title, S.title AS show_title, R.rating, R.review_text, R.review_date 
            FROM Review R
            LEFT JOIN User U ON R.user_id = U.user_id
            LEFT JOIN Movie M ON R.movie_id = M.movie_id
            LEFT JOIN TV_Show S ON R.show_id = S.show_id
            WHERE R.user_id = %s
        """
        cursor.execute(query, (self.critic_id,))
        reviews = cursor.fetchall()

        # Debug print to verify fetched reviews
        print(f"Fetched reviews: {reviews}")

        column_names = [desc[0] for desc in cursor.description]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, review in enumerate(reviews, start=1):
            for j, value in enumerate(review):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)
        # cursor.execute("""SELECT R.review_id, U.username, M.title AS movie_title, S.title AS show_title, R.rating, R.review_text, R.review_date
        #                   FROM Review R
        #                   LEFT JOIN User U ON R.user_id = U.user_id
        #                   LEFT JOIN Movie M ON R.movie_id = M.movie_id
        #                   LEFT JOIN TV_Show S ON R.show_id = S.show_id
        #                   WHERE R.user_id = %s""", (self.critic_id,))
        # reviews = cursor.fetchall()
        #
        # column_names = [desc[0] for desc in cursor.description]
        # for j, column_name in enumerate(column_names):
        #     entry = Entry(self.scrollable_frame, width=20, fg='black')
        #     entry.grid(row=0, column=j, padx=5, pady=5)
        #     entry.insert(END, column_name)
        #     self.entries.append(entry)
        #
        # for i, review in enumerate(reviews, start=1):
        #     for j, value in enumerate(review):
        #         entry = Entry(self.scrollable_frame, width=20, fg='black')
        #         entry.grid(row=i, column=j, padx=5, pady=5)
        #         entry.insert(END, str(value))
        #         self.entries.append(entry)

    def go_home(self):
        self.window.destroy()
        Main_App().run()

    def run(self):
        self.window.mainloop()

class Critic_Login:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("400x290")
        self.window.resizable(True, True)
        self.window.config(background="#FFC0CB")
        self.window.title("Critic Login")

        username_label = Label(self.window, text="Username")
        username_label.pack()
        self.username_entry = Entry(self.window)
        self.username_entry.pack()

        password_label = Label(self.window, text="Password")
        password_label.pack()
        self.password_entry = Entry(self.window, show="*")
        self.password_entry.pack()
        login_button = Button(self.window, text="Login", command=self.login)
        login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        global cursor
        close_previous_results(cursor)
        cursor.execute("SELECT user_id FROM User WHERE username = %s AND password = %s AND role = 'critic'", (username, password))
        result = cursor.fetchone()

        if result:
            user_id = result[0]
            cursor.execute("SELECT critic_id FROM Critic WHERE user_id = %s", (user_id,))
            critic_id = cursor.fetchone()[0]
            self.window.destroy()
            Critic_App(critic_id).run()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def run(self):
        self.window.mainloop()



class User_Login:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("400x290")
        self.window.resizable(True, True)
        self.window.config(background="#FFC0CB")
        self.window.title("User Login")

        username_label = Label(self.window, text="Username")
        username_label.pack()
        self.username_entry = Entry(self.window)
        self.username_entry.pack()

        password_label = Label(self.window, text="Password")
        password_label.pack()
        self.password_entry = Entry(self.window, show="*")
        self.password_entry.pack()

        login_button = Button(self.window, text="Login", command=self.login)
        login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        global cursor
        close_previous_results(cursor)
        cursor.execute("SELECT user_id FROM User WHERE username = %s AND password = %s AND role = 'viewer'", (username, password))
        result = cursor.fetchone()

        if result:
            user_id = result[0]
            self.window.destroy()
            User_App(user_id)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def run(self):
        self.window.mainloop()

class User_App:
    def __init__(self, user_id):
        self.user_id = user_id
        self.window = Tk()
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        self.window.config(background="#FFC0CB")
        self.window.title("User")

        home_button = Button(self.window, text="Home", command=self.go_home)
        home_button.pack()

        self.entries = []
        self.create_scrollable_frame()


        list_movie_button = Button(self.window, text="List Movies", width=12, height=3, command=self.listMovies)
        list_movie_button.pack()

        list_show_button = Button(self.window, text="List Shows", width=12, height=3, command=self.listShows)
        list_show_button.pack()

        search_button = Button(self.window, text="Search", width=12, height=3, command=self.searchMoviesAndShows)
        search_button.pack()
        write_review_button = Button(self.window, text="Write Review", width=12, height=3, command=self.writeReview)
        write_review_button.pack()

        edit_review_button = Button(self.window, text="Edit Review", width=12, height=3, command=self.editReview)
        edit_review_button.pack()

        delete_review_button = Button(self.window, text="Delete Review", width=12, height=3, command=self.deleteReview)
        delete_review_button.pack()

        view_reviews_button = Button(self.window, text="View Reviews", width=12, height=3, command=self.viewReviews)
        view_reviews_button.pack()

        create_watchlist_button = Button(self.window, text="Create Watchlist", width=12, height=3, command=self.createWatchlist)
        create_watchlist_button.pack()

        add_to_watchlist_button = Button(self.window, text="Add to Watchlist", width=15, height=3, command=self.addToWatchlist)
        add_to_watchlist_button.pack()

        remove_from_watchlist_button = Button(self.window, text="Remove from Watchlist", width=15, height=3, command=self.removeFromWatchlist)
        remove_from_watchlist_button.pack()

        view_watchlist_button = Button(self.window, text="View Watchlists", width=15, height=3, command=self.viewWatchlists)
        view_watchlist_button.pack()

        view_recommendations_button = Button(self.window, text="View Recommendations", command=self.viewRecommendations, width=20)
        view_recommendations_button.pack()


    def viewRecommendations(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        cursor.execute("CALL GenerateRecommendations(%s)", (self.user_id,))
        cursor.execute("""
            SELECT Movie.title AS Movie, TV_Show.title AS Show
            FROM Recommendation
            LEFT JOIN Movie ON Recommendation.movie_id = Movie.movie_id
            LEFT JOIN TV_Show ON Recommendation.show_id = TV_Show.show_id
            WHERE Recommendation.user_id = %s
        """, (self.user_id,))
        recommendations = cursor.fetchall()

        column_names = ["Movie", "Show"]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, recommendation in enumerate(recommendations, start=1):
            for j, value in enumerate(recommendation):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)


    def viewWatchlists(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        # Prompt the user to select a watchlist
        watchlist_selection_window = Tk()
        watchlist_selection_window.geometry("400x200")
        watchlist_selection_window.title("Select Watchlist")

        watchlist_id_label = Label(watchlist_selection_window, text="Watchlist ID or Name")
        watchlist_id_label.pack()
        watchlist_id_entry = Entry(watchlist_selection_window)
        watchlist_id_entry.pack()

        def show_watchlist():
            watchlist_id_or_name = watchlist_id_entry.get()
            watchlist_selection_window.destroy()
            self.display_watchlist_items(watchlist_id_or_name)

        show_button = Button(watchlist_selection_window, text="Show", command=show_watchlist)
        show_button.pack()

    def display_watchlist_items(self, watchlist_id_or_name):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        # Query to fetch watchlist items based on watchlist ID or name
        query = """
        SELECT W.watchlist_id, W.name AS watchlist_name, 
               WI.show_id, S.title AS show_title, 
               WI.movie_id, M.title AS movie_title
        FROM Watchlist W
        LEFT JOIN Watchlist_Item WI ON W.watchlist_id = WI.watchlist_id
        LEFT JOIN TV_Show S ON WI.show_id = S.show_id
        LEFT JOIN Movie M ON WI.movie_id = M.movie_id
        WHERE W.user_id = %s AND (W.watchlist_id = %s OR W.name = %s)
        """
        cursor.execute(query, (self.user_id, watchlist_id_or_name, watchlist_id_or_name))
        watchlists = cursor.fetchall()

        column_names = ["Watchlist ID", "Watchlist Name", "Show ID", "Show Title", "Movie ID", "Movie Title"]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, watchlist in enumerate(watchlists, start=1):
            for j, value in enumerate(watchlist):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def searchMoviesAndShows(self):
        search_window = Tk()
        search_window.geometry("400x400")
        search_window.title("Search Movies and Shows")

        search_label = Label(search_window, text="Search")
        search_label.pack()
        search_entry = Entry(search_window)
        search_entry.pack()

        genre_label = Label(search_window, text="Genre")
        genre_label.pack()
        genre_entry = Entry(search_window)
        genre_entry.pack()

        rating_label = Label(search_window, text="Rating")
        rating_label.pack()
        rating_entry = Entry(search_window)
        rating_entry.pack()

        release_date_label = Label(search_window, text="Release Date (YYYY-MM-DD)")
        release_date_label.pack()
        release_date_entry = Entry(search_window)
        release_date_entry.pack()

        search_button = Button(search_window, text="Search", command=lambda: self.execute_search(search_entry, genre_entry, rating_entry, release_date_entry, search_window))
        search_button.pack()

    def execute_search(self, search_entry, genre_entry, rating_entry, release_date_entry, search_window):
        search_term = search_entry.get()
        genre = genre_entry.get()
        rating = rating_entry.get()
        release_date = release_date_entry.get()

        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        query = """
        SELECT movie_id, title, description, release_date, genre, rating, director_id FROM Movie
        WHERE (title LIKE %s OR description LIKE %s)
        """
        params = [f"%{search_term}%", f"%{search_term}%"]

        if genre:
            query += " AND genre = %s"
            params.append(genre)
        if rating:
            query += " AND rating >= %s"
            params.append(rating)
        if release_date:
            query += " AND release_date = %s"
            params.append(release_date)

        cursor.execute(query, params)
        movies = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, movie in enumerate(movies, start=1):
            for j, value in enumerate(movie):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

        search_window.destroy()

    def create_scrollable_frame(self):
        self.canvas = Canvas(self.window)
        self.scrollable_frame = Frame(self.canvas)
        self.scrollbar = Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def listMovies(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        cursor.execute("SELECT * FROM Movie")
        movies = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, movie in enumerate(movies, start=1):
            for j, value in enumerate(movie):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def listShows(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        cursor.execute("SELECT * FROM TV_Show")
        shows = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, show in enumerate(shows, start=1):
            for j, value in enumerate(show):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def writeReview(self):
        review_window = Tk()
        review_window.geometry("400x400")
        review_window.title("Write Review")

        rating_label = Label(review_window, text="Rating")
        rating_label.pack()
        rating_entry = Entry(review_window)
        rating_entry.pack()

        review_text_label = Label(review_window, text="Review Text")
        review_text_label.pack()
        review_text_entry = Entry(review_window)
        review_text_entry.pack()

        review_date_label = Label(review_window, text="Review Date (YYYY-MM-DD)")
        review_date_label.pack()
        review_date_entry = Entry(review_window)
        review_date_entry.pack()

        movie_id_label = Label(review_window, text="Movie ID (if applicable)")
        movie_id_label.pack()
        movie_id_entry = Entry(review_window)
        movie_id_entry.pack()

        show_id_label = Label(review_window, text="Show ID (if applicable)")
        show_id_label.pack()
        show_id_entry = Entry(review_window)
        show_id_entry.pack()

        save_button = Button(review_window, text="Save",
                             command=lambda: self.save_review(rating_entry, review_text_entry, review_date_entry,
                                                              movie_id_entry, show_id_entry, review_window))
        save_button.pack()

    def save_review(self, rating_entry, review_text_entry, review_date_entry, movie_id_entry, show_id_entry,
                    review_window):
        rating = float(rating_entry.get())
        review_text = review_text_entry.get()
        review_date = review_date_entry.get()
        movie_id = movie_id_entry.get() or None
        show_id = show_id_entry.get() or None

        global cursor, mydb
        cursor.execute("""INSERT INTO Review (user_id, rating, review_text, review_date, movie_id, show_id)
                          VALUES (%s, %s, %s, %s, %s, %s)""",
                       (self.user_id, rating, review_text, review_date, movie_id, show_id))
        mydb.commit()
        review_window.destroy()

    def editReview(self):
        edit_review_window = Tk()
        edit_review_window.geometry("400x400")
        edit_review_window.title("Edit Review")

        review_id_label = Label(edit_review_window, text="Review ID")
        review_id_label.pack()
        review_id_entry = Entry(edit_review_window)
        review_id_entry.pack()

        rating_label = Label(edit_review_window, text="New Rating")
        rating_label.pack()
        rating_entry = Entry(edit_review_window)
        rating_entry.pack()

        review_text_label = Label(edit_review_window, text="New Review Text")
        review_text_label.pack()
        review_text_entry = Entry(edit_review_window)
        review_text_entry.pack()

        save_button = Button(edit_review_window, text="Save",
                             command=lambda: self.update_review(review_id_entry, rating_entry, review_text_entry,
                                                                edit_review_window))
        save_button.pack()

    def update_review(self, review_id_entry, rating_entry, review_text_entry, edit_review_window):
        review_id = int(review_id_entry.get())
        new_rating = float(rating_entry.get())
        new_review_text = review_text_entry.get()

        global cursor, mydb
        cursor.execute("""UPDATE Review SET rating = %s, review_text = %s WHERE review_id = %s""",
                       (new_rating, new_review_text, review_id))
        mydb.commit()
        edit_review_window.destroy()

    def deleteReview(self):
        delete_review_window = Tk()
        delete_review_window.geometry("400x400")
        delete_review_window.title("Delete Review")

        review_id_label = Label(delete_review_window, text="Review ID")
        review_id_label.pack()
        review_id_entry = Entry(delete_review_window)
        review_id_entry.pack()

        delete_button = Button(delete_review_window, text="Delete", command=lambda: self.remove_review(review_id_entry, delete_review_window))
        delete_button.pack()

    def remove_review(self, review_id_entry, delete_review_window):
        review_id = int(review_id_entry.get())

        global cursor, mydb
        cursor.execute("""DELETE FROM Review WHERE review_id = %s""", (review_id,))
        mydb.commit()
        delete_review_window.destroy()


    def viewReviews(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        cursor.execute("""SELECT R.review_id, U.username, M.title, S.title, R.rating, R.review_text, R.review_date
                          FROM Review R
                          LEFT JOIN User U ON R.user_id = U.user_id
                          LEFT JOIN Movie M ON R.movie_id = M.movie_id
                          LEFT JOIN TV_Show S ON R.show_id = S.show_id
                          WHERE R.user_id = %s""", (self.user_id,))
        reviews = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, review in enumerate(reviews, start=1):
            for j, value in enumerate(review):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)


    # def writeReview(self):
    #     review_window = Tk()
    #     review_window.geometry("400x400")
    #     review_window.title("Write Review")
    #
    #     rating_label = Label(review_window, text="Rating")
    #     rating_label.pack()
    #     rating_entry = Entry(review_window)
    #     rating_entry.pack()
    #
    #     review_text_label = Label(review_window, text="Review Text")
    #     review_text_label.pack()
    #     review_text_entry = Entry(review_window)
    #     review_text_entry.pack()
    #
    #     review_date_label = Label(review_window, text="Review Date (YYYY-MM-DD)")
    #     review_date_label.pack()
    #     review_date_entry = Entry(review_window)
    #     review_date_entry.pack()
    #
    #     save_button = Button(review_window, text="Save", command=lambda: self.save_review(rating_entry, review_text_entry, review_date_entry, review_window))
    #     save_button.pack()
    #
    # def save_review(self, rating_entry, review_text_entry, review_date_entry, review_window):
    #     rating = float(rating_entry.get())
    #     review_text = review_text_entry.get()
    #     review_date = review_date_entry.get()
    #
    #     global cursor, mydb
    #     cursor.execute("""INSERT INTO Review (user_id, rating, review_text, review_date)
    #                       VALUES (%s, %s, %s, %s)""",
    #                    (self.user_id, rating, review_text, review_date))
    #     mydb.commit()
    #     review_window.destroy()
    #
    # def editReview(self):
    #     edit_review_window = Tk()
    #     edit_review_window.geometry("400x400")
    #     edit_review_window.title("Edit Review")
    #
    #     review_id_label = Label(edit_review_window, text="Review ID")
    #     review_id_label.pack()
    #     review_id_entry = Entry(edit_review_window)
    #     review_id_entry.pack()
    #
    #     rating_label = Label(edit_review_window, text="New Rating")
    #     rating_label.pack()
    #     rating_entry = Entry(edit_review_window)
    #     rating_entry.pack()
    #
    #     review_text_label = Label(edit_review_window, text="New Review Text")
    #     review_text_label.pack()
    #     review_text_entry = Entry(edit_review_window)
    #     review_text_entry.pack()
    #
    #     save_button = Button(edit_review_window, text="Save", command=lambda: self.update_review(review_id_entry, rating_entry, review_text_entry, edit_review_window))
    #     save_button.pack()
    #
    # def update_review(self, review_id_entry, rating_entry, review_text_entry, edit_review_window):
    #     review_id = int(review_id_entry.get())
    #     new_rating = float(rating_entry.get())
    #     new_review_text = review_text_entry.get()
    #
    #     global cursor, mydb
    #     cursor.execute("""UPDATE Review SET rating = %s, review_text = %s WHERE review_id = %s""",
    #                    (new_rating, new_review_text, review_id))
    #     mydb.commit()
    #     edit_review_window.destroy()
    #
    # def deleteReview(self):
    #     delete_review_window = Tk()
    #     delete_review_window.geometry("400x400")
    #     delete_review_window.title("Delete Review")
    #
    #     review_id_label = Label(delete_review_window, text="Review ID")
    #     review_id_label.pack()
    #     review_id_entry = Entry(delete_review_window)
    #     review_id_entry.pack()
    #
    #     delete_button = Button(delete_review_window, text="Delete", command=lambda: self.remove_review(review_id_entry, delete_review_window))
    #     delete_button.pack()
    #
    # def remove_review(self, review_id_entry, delete_review_window):
    #     review_id = int(review_id_entry.get())
    #
    #     global cursor, mydb
    #     cursor.execute("""DELETE FROM Review WHERE review_id = %s""", (review_id,))
    #     mydb.commit()
    #     delete_review_window.destroy()
    #
    # def viewReviews(self):
    #     global cursor
    #     close_previous_results(cursor)
    #     clearEntries(self.entries)
    #
    #     cursor.execute("""SELECT R.review_id, U.username, M.title, S.title, R.rating, R.review_text, R.review_date
    #                       FROM Review R
    #                       LEFT JOIN User U ON R.user_id = U.user_id
    #                       LEFT JOIN Movie M ON R.movie_id = M.movie_id
    #                       LEFT JOIN TV_Show S ON R.show_id = S.show_id
    #                       WHERE R.user_id = %s""", (self.user_id,))
    #     reviews = cursor.fetchall()
    #
    #     column_names = [desc[0] for desc in cursor.description]
    #     for j, column_name in enumerate(column_names):
    #         entry = Entry(self.scrollable_frame, width=20, fg='black')
    #         entry.grid(row=0, column=j, padx=5, pady=5)
    #         entry.insert(END, column_name)
    #         self.entries.append(entry)
    #
    #     for i, review in enumerate(reviews, start=1):
    #         for j, value in enumerate(review):
    #             entry = Entry(self.scrollable_frame, width=20, fg='black')
    #             entry.grid(row=i, column=j, padx=5, pady=5)
    #             entry.insert(END, str(value))
    #             self.entries.append(entry)

    def createWatchlist(self):
        watchlist_window = Tk()
        watchlist_window.geometry("400x400")
        watchlist_window.title("Create Watchlist")

        name_label = Label(watchlist_window, text="Watchlist Name")
        name_label.pack()
        name_entry = Entry(watchlist_window)
        name_entry.pack()

        save_button = Button(watchlist_window, text="Save",
                             command=lambda: self.save_watchlist(name_entry, watchlist_window))
        save_button.pack()

    def save_watchlist(self, name_entry, watchlist_window):
        name = name_entry.get()

        global cursor, mydb
        cursor.execute("""INSERT INTO Watchlist (user_id, name) VALUES (%s, %s)""", (self.user_id, name))
        mydb.commit()
        watchlist_window.destroy()

    def addToWatchlist(self):
        add_window = Tk()
        add_window.geometry("400x400")
        add_window.title("Add to Watchlist")

        watchlist_id_label = Label(add_window, text="Watchlist ID")
        watchlist_id_label.pack()
        watchlist_id_entry = Entry(add_window)
        watchlist_id_entry.pack()

        show_id_label = Label(add_window, text="Show ID (if applicable)")
        show_id_label.pack()
        show_id_entry = Entry(add_window)
        show_id_entry.pack()

        movie_id_label = Label(add_window, text="Movie ID (if applicable)")
        movie_id_label.pack()
        movie_id_entry = Entry(add_window)
        movie_id_entry.pack()

        save_button = Button(add_window, text="Save",
                             command=lambda: self.save_to_watchlist(watchlist_id_entry, show_id_entry, movie_id_entry,
                                                                    add_window))
        save_button.pack()

    def save_to_watchlist(self, watchlist_id_entry, show_id_entry, movie_id_entry, add_window):
        watchlist_id = int(watchlist_id_entry.get())
        show_id = int(show_id_entry.get()) if show_id_entry.get() else None
        movie_id = int(movie_id_entry.get()) if movie_id_entry.get() else None

        global cursor, mydb
        cursor.execute("""INSERT INTO Watchlist_Item (watchlist_id, show_id, movie_id) 
                           VALUES (%s, %s, %s)""",
                       (watchlist_id, show_id, movie_id))
        mydb.commit()
        add_window.destroy()

    def removeFromWatchlist(self):
        remove_window = Tk()
        remove_window.geometry("400x200")
        remove_window.title("Remove from Watchlist")

        watchlist_id_label = Label(remove_window, text="Watchlist ID")
        watchlist_id_label.pack()
        watchlist_id_entry = Entry(remove_window)
        watchlist_id_entry.pack()

        def show_items_to_remove():
            watchlist_id = int(watchlist_id_entry.get())
            remove_window.destroy()
            self.show_watchlist_items_to_remove(watchlist_id)

        show_button = Button(remove_window, text="Show Items", command=show_items_to_remove)
        show_button.pack()

    def delete_from_watchlist(self, watchlist_item_id_entry, remove_window):
        watchlist_item_id = int(watchlist_item_id_entry.get())

        global cursor, mydb
        cursor.execute("""DELETE FROM Watchlist_Item WHERE watchlist_item_id = %s""", (watchlist_item_id,))
        mydb.commit()
        remove_window.destroy()

    def show_watchlist_items_to_remove(self, watchlist_id):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        # Simulating a full outer join using UNION of left and right joins
        full_outer_join_query = """
        SELECT WI.watchlist_item_id, WI.show_id, S.title AS show_title, 
               WI.movie_id, M.title AS movie_title
        FROM Watchlist_Item WI
        LEFT JOIN TV_Show S ON WI.show_id = S.show_id
        LEFT JOIN Movie M ON WI.movie_id = M.movie_id
        WHERE WI.watchlist_id = %s
        UNION
        SELECT WI.watchlist_item_id, WI.show_id, S.title AS show_title, 
               WI.movie_id, M.title AS movie_title
        FROM Watchlist_Item WI
        RIGHT JOIN TV_Show S ON WI.show_id = S.show_id
        RIGHT JOIN Movie M ON WI.movie_id = M.movie_id
        WHERE WI.watchlist_id = %s AND WI.watchlist_item_id IS NULL
        """
        cursor.execute(full_outer_join_query, (watchlist_id, watchlist_id))
        items = cursor.fetchall()

        remove_item_window = Tk()
        remove_item_window.geometry("600x400")
        remove_item_window.title("Remove Watchlist Item")

        column_names = ["Watchlist Item ID", "Show ID", "Show Title", "Movie ID", "Movie Title"]
        for j, column_name in enumerate(column_names):
            entry = Entry(remove_item_window, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)

        for i, item in enumerate(items, start=1):
            for j, value in enumerate(item):
                entry = Entry(remove_item_window, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))

        watchlist_item_id_label = Label(remove_item_window, text="Watchlist Item ID to Remove")
        watchlist_item_id_label.grid(row=len(items) + 1, column=0, padx=5, pady=5)
        watchlist_item_id_entry = Entry(remove_item_window)
        watchlist_item_id_entry.grid(row=len(items) + 1, column=1, padx=5, pady=5)

        delete_button = Button(remove_item_window, text="Delete",
                               command=lambda: self.delete_from_watchlist(watchlist_item_id_entry, remove_item_window))
        delete_button.grid(row=len(items) + 1, column=2, padx=5, pady=5)

    def viewWatchlists(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        # Using RIGHT JOIN to fetch data
        right_join_query = """
        SELECT W.watchlist_id, W.name AS watchlist_name, 
               WI.show_id, S.title AS show_title, 
               WI.movie_id, M.title AS movie_title
        FROM Watchlist_Item WI
        RIGHT JOIN Watchlist W ON WI.watchlist_id = W.watchlist_id
        LEFT JOIN TV_Show S ON WI.show_id = S.show_id
        LEFT JOIN Movie M ON WI.movie_id = M.movie_id
        WHERE W.user_id = %s
        """
        cursor.execute(right_join_query, (self.user_id,))
        watchlists = cursor.fetchall()

        column_names = ["Watchlist ID", "Watchlist Name", "Show ID", "Show Title", "Movie ID", "Movie Title"]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, watchlist in enumerate(watchlists, start=1):
            for j, value in enumerate(watchlist):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def go_home(self):
        self.window.destroy()
        Main_App().run()

    def run(self):
        self.window.mainloop()
class User_App:
    def __init__(self, user_id):
        self.user_id = user_id
        self.window = Tk()
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        self.window.config(background="#FFC0CB")
        self.window.title("User")

        home_button = Button(self.window, text="Home", command=self.go_home)
        home_button.pack()

        self.entries = []
        self.create_scrollable_frame()

        list_movie_button = Button(self.window, text="List Movies", width=12, height=3, command=self.listMovies)
        list_movie_button.pack()

        list_show_button = Button(self.window, text="List Shows", width=12, height=3, command=self.listShows)
        list_show_button.pack()

        search_button = Button(self.window, text="Search", width=12, height=3, command=self.searchMoviesAndShows)
        search_button.pack()
        write_review_button = Button(self.window, text="Write Review", width=12, height=3, command=self.writeReview)
        write_review_button.pack()

        edit_review_button = Button(self.window, text="Edit Review", width=12, height=3, command=self.editReview)
        edit_review_button.pack()

        delete_review_button = Button(self.window, text="Delete Review", width=12, height=3, command=self.deleteReview)
        delete_review_button.pack()

        view_reviews_button = Button(self.window, text="View Reviews", width=12, height=3, command=self.viewReviews)
        view_reviews_button.pack()

        create_watchlist_button = Button(self.window, text="Create Watchlist", width=12, height=3, command=self.createWatchlist)
        create_watchlist_button.pack()

        add_to_watchlist_button = Button(self.window, text="Add to Watchlist", width=12, height=3, command=self.addToWatchlist)
        add_to_watchlist_button.pack()

        remove_from_watchlist_button = Button(self.window, text="Remove from Watchlist", width=18, height=3, command=self.removeFromWatchlist)
        remove_from_watchlist_button.pack()

        view_watchlist_button = Button(self.window, text="View Watchlists", width=12, height=3, command=self.viewWatchlists)
        view_watchlist_button.pack()

    def viewWatchlists(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        # Prompt the user to select a watchlist
        watchlist_selection_window = Tk()
        watchlist_selection_window.geometry("400x200")
        watchlist_selection_window.title("Select Watchlist")

        watchlist_id_label = Label(watchlist_selection_window, text="Watchlist ID or Name")
        watchlist_id_label.pack()
        watchlist_id_entry = Entry(watchlist_selection_window)
        watchlist_id_entry.pack()

        def show_watchlist():
            watchlist_id_or_name = watchlist_id_entry.get()
            watchlist_selection_window.destroy()
            self.display_watchlist_items(watchlist_id_or_name)

        show_button = Button(watchlist_selection_window, text="Show", command=show_watchlist)
        show_button.pack()

    def display_watchlist_items(self, watchlist_id_or_name):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        # Query to fetch watchlist items based on watchlist ID or name
        query = """
        SELECT W.watchlist_id, W.name AS watchlist_name, 
               WI.show_id, S.title AS show_title, 
               WI.movie_id, M.title AS movie_title
        FROM Watchlist W
        LEFT JOIN Watchlist_Item WI ON W.watchlist_id = WI.watchlist_id
        LEFT JOIN TV_Show S ON WI.show_id = S.show_id
        LEFT JOIN Movie M ON WI.movie_id = M.movie_id
        WHERE W.user_id = %s AND (W.watchlist_id = %s OR W.name = %s)
        """
        cursor.execute(query, (self.user_id, watchlist_id_or_name, watchlist_id_or_name))
        watchlists = cursor.fetchall()

        column_names = ["Watchlist ID", "Watchlist Name", "Show ID", "Show Title", "Movie ID", "Movie Title"]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, watchlist in enumerate(watchlists, start=1):
            for j, value in enumerate(watchlist):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def searchMoviesAndShows(self):
        search_window = Tk()
        search_window.geometry("400x400")
        search_window.title("Search Movies and Shows")

        search_label = Label(search_window, text="Search")
        search_label.pack()
        search_entry = Entry(search_window)
        search_entry.pack()

        genre_label = Label(search_window, text="Genre")
        genre_label.pack()
        genre_entry = Entry(search_window)
        genre_entry.pack()

        rating_label = Label(search_window, text="Rating")
        rating_label.pack()
        rating_entry = Entry(search_window)
        rating_entry.pack()

        release_date_label = Label(search_window, text="Release Date (YYYY-MM-DD)")
        release_date_label.pack()
        release_date_entry = Entry(search_window)
        release_date_entry.pack()

        search_button = Button(search_window, text="Search", command=lambda: self.execute_search(search_entry, genre_entry, rating_entry, release_date_entry, search_window))
        search_button.pack()

    def execute_search(self, search_entry, genre_entry, rating_entry, release_date_entry, search_window):
        search_term = search_entry.get()
        genre = genre_entry.get()
        rating = rating_entry.get()
        release_date = release_date_entry.get()

        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        query = """
        SELECT movie_id, title, description, release_date, genre, rating, director_id FROM Movie
        WHERE (title LIKE %s OR description LIKE %s)
        """
        params = [f"%{search_term}%", f"%{search_term}%"]

        if genre:
            query += " AND genre = %s"
            params.append(genre)
        if rating:
            query += " AND rating >= %s"
            params.append(rating)
        if release_date:
            query += " AND release_date = %s"
            params.append(release_date)

        cursor.execute(query, params)
        movies = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, movie in enumerate(movies, start=1):
            for j, value in enumerate(movie):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

        search_window.destroy()

    def create_scrollable_frame(self):
        self.canvas = Canvas(self.window)
        self.scrollable_frame = Frame(self.canvas)
        self.scrollbar = Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def listMovies(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        cursor.execute("SELECT * FROM Movie")
        movies = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, movie in enumerate(movies, start=1):
            for j, value in enumerate(movie):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def listShows(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        cursor.execute("SELECT * FROM TV_Show")
        shows = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, show in enumerate(shows, start=1):
            for j, value in enumerate(show):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def writeReview(self):
        review_window = Tk()
        review_window.geometry("400x400")
        review_window.title("Write Review")

        rating_label = Label(review_window, text="Rating")
        rating_label.pack()
        rating_entry = Entry(review_window)
        rating_entry.pack()

        review_text_label = Label(review_window, text="Review Text")
        review_text_label.pack()
        review_text_entry = Entry(review_window)
        review_text_entry.pack()

        review_date_label = Label(review_window, text="Review Date (YYYY-MM-DD)")
        review_date_label.pack()
        review_date_entry = Entry(review_window)
        review_date_entry.pack()

        save_button = Button(review_window, text="Save", command=lambda: self.save_review(rating_entry, review_text_entry, review_date_entry, review_window))
        save_button.pack()

    def save_review(self, rating_entry, review_text_entry, review_date_entry, review_window):
        rating = float(rating_entry.get())
        review_text = review_text_entry.get()
        review_date = review_date_entry.get()

        global cursor, mydb
        cursor.execute("""INSERT INTO Review (user_id, rating, review_text, review_date) 
                          VALUES (%s, %s, %s, %s)""",
                       (self.user_id, rating, review_text, review_date))
        mydb.commit()
        review_window.destroy()

    def editReview(self):
        edit_review_window = Tk()
        edit_review_window.geometry("400x400")
        edit_review_window.title("Edit Review")

        review_id_label = Label(edit_review_window, text="Review ID")
        review_id_label.pack()
        review_id_entry = Entry(edit_review_window)
        review_id_entry.pack()

        rating_label = Label(edit_review_window, text="New Rating")
        rating_label.pack()
        rating_entry = Entry(edit_review_window)
        rating_entry.pack()

        review_text_label = Label(edit_review_window, text="New Review Text")
        review_text_label.pack()
        review_text_entry = Entry(edit_review_window)
        review_text_entry.pack()

        save_button = Button(edit_review_window, text="Save", command=lambda: self.update_review(review_id_entry, rating_entry, review_text_entry, edit_review_window))
        save_button.pack()

    def update_review(self, review_id_entry, rating_entry, review_text_entry, edit_review_window):
        review_id = int(review_id_entry.get())
        new_rating = float(rating_entry.get())
        new_review_text = review_text_entry.get()

        global cursor, mydb
        cursor.execute("""UPDATE Review SET rating = %s, review_text = %s WHERE review_id = %s""",
                       (new_rating, new_review_text, review_id))
        mydb.commit()
        edit_review_window.destroy()

    def deleteReview(self):
        delete_review_window = Tk()
        delete_review_window.geometry("400x400")
        delete_review_window.title("Delete Review")

        review_id_label = Label(delete_review_window, text="Review ID")
        review_id_label.pack()
        review_id_entry = Entry(delete_review_window)
        review_id_entry.pack()

        delete_button = Button(delete_review_window, text="Delete", command=lambda: self.remove_review(review_id_entry, delete_review_window))
        delete_button.pack()

    def remove_review(self, review_id_entry, delete_review_window):
        review_id = int(review_id_entry.get())

        global cursor, mydb
        cursor.execute("""DELETE FROM Review WHERE review_id = %s""", (review_id,))
        mydb.commit()
        delete_review_window.destroy()

    def viewReviews(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        cursor.execute("""SELECT R.review_id, U.username, M.title, S.title, R.rating, R.review_text, R.review_date 
                          FROM Review R
                          LEFT JOIN User U ON R.user_id = U.user_id
                          LEFT JOIN Movie M ON R.movie_id = M.movie_id
                          LEFT JOIN TV_Show S ON R.show_id = S.show_id
                          WHERE R.user_id = %s""", (self.user_id,))
        reviews = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, review in enumerate(reviews, start=1):
            for j, value in enumerate(review):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def createWatchlist(self):
        watchlist_window = Tk()
        watchlist_window.geometry("400x400")
        watchlist_window.title("Create Watchlist")

        name_label = Label(watchlist_window, text="Watchlist Name")
        name_label.pack()
        name_entry = Entry(watchlist_window)
        name_entry.pack()

        save_button = Button(watchlist_window, text="Save",
                             command=lambda: self.save_watchlist(name_entry, watchlist_window))
        save_button.pack()

    def save_watchlist(self, name_entry, watchlist_window):
        name = name_entry.get()

        global cursor, mydb
        cursor.execute("""INSERT INTO Watchlist (user_id, name) VALUES (%s, %s)""", (self.user_id, name))
        mydb.commit()
        watchlist_window.destroy()

    def addToWatchlist(self):
        add_window = Tk()
        add_window.geometry("400x400")
        add_window.title("Add to Watchlist")

        watchlist_id_label = Label(add_window, text="Watchlist ID")
        watchlist_id_label.pack()
        watchlist_id_entry = Entry(add_window)
        watchlist_id_entry.pack()

        show_id_label = Label(add_window, text="Show ID (if applicable)")
        show_id_label.pack()
        show_id_entry = Entry(add_window)
        show_id_entry.pack()

        movie_id_label = Label(add_window, text="Movie ID (if applicable)")
        movie_id_label.pack()
        movie_id_entry = Entry(add_window)
        movie_id_entry.pack()

        save_button = Button(add_window, text="Save",
                             command=lambda: self.save_to_watchlist(watchlist_id_entry, show_id_entry, movie_id_entry,
                                                                    add_window))
        save_button.pack()

    def save_to_watchlist(self, watchlist_id_entry, show_id_entry, movie_id_entry, add_window):
        watchlist_id = int(watchlist_id_entry.get())
        show_id = int(show_id_entry.get()) if show_id_entry.get() else None
        movie_id = int(movie_id_entry.get()) if movie_id_entry.get() else None

        global cursor, mydb
        cursor.execute("""INSERT INTO Watchlist_Item (watchlist_id, show_id, movie_id) 
                           VALUES (%s, %s, %s)""",
                       (watchlist_id, show_id, movie_id))
        mydb.commit()
        add_window.destroy()

    def removeFromWatchlist(self):
        remove_window = Tk()
        remove_window.geometry("400x200")
        remove_window.title("Remove from Watchlist")

        watchlist_id_label = Label(remove_window, text="Watchlist ID")
        watchlist_id_label.pack()
        watchlist_id_entry = Entry(remove_window)
        watchlist_id_entry.pack()

        def show_items_to_remove():
            watchlist_id = int(watchlist_id_entry.get())
            remove_window.destroy()
            self.show_watchlist_items_to_remove(watchlist_id)

        show_button = Button(remove_window, text="Show Items", command=show_items_to_remove)
        show_button.pack()

    def delete_from_watchlist(self, watchlist_item_id_entry, remove_window):
        watchlist_item_id = int(watchlist_item_id_entry.get())

        global cursor, mydb
        cursor.execute("""DELETE FROM Watchlist_Item WHERE watchlist_item_id = %s""", (watchlist_item_id,))
        mydb.commit()
        remove_window.destroy()

    def show_watchlist_items_to_remove(self, watchlist_id):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        # Simulating a full outer join using UNION of left and right joins
        full_outer_join_query = """
        SELECT WI.watchlist_item_id, WI.show_id, S.title AS show_title, 
               WI.movie_id, M.title AS movie_title
        FROM Watchlist_Item WI
        LEFT JOIN TV_Show S ON WI.show_id = S.show_id
        LEFT JOIN Movie M ON WI.movie_id = M.movie_id
        WHERE WI.watchlist_id = %s
        UNION
        SELECT WI.watchlist_item_id, WI.show_id, S.title AS show_title, 
               WI.movie_id, M.title AS movie_title
        FROM Watchlist_Item WI
        RIGHT JOIN TV_Show S ON WI.show_id = S.show_id
        RIGHT JOIN Movie M ON WI.movie_id = M.movie_id
        WHERE WI.watchlist_id = %s AND WI.watchlist_item_id IS NULL
        """
        cursor.execute(full_outer_join_query, (watchlist_id, watchlist_id))
        items = cursor.fetchall()

        remove_item_window = Tk()
        remove_item_window.geometry("600x400")
        remove_item_window.title("Remove Watchlist Item")

        column_names = ["Watchlist Item ID", "Show ID", "Show Title", "Movie ID", "Movie Title"]
        for j, column_name in enumerate(column_names):
            entry = Entry(remove_item_window, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)

        for i, item in enumerate(items, start=1):
            for j, value in enumerate(item):
                entry = Entry(remove_item_window, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))

        watchlist_item_id_label = Label(remove_item_window, text="Watchlist Item ID to Remove")
        watchlist_item_id_label.grid(row=len(items) + 1, column=0, padx=5, pady=5)
        watchlist_item_id_entry = Entry(remove_item_window)
        watchlist_item_id_entry.grid(row=len(items) + 1, column=1, padx=5, pady=5)

        delete_button = Button(remove_item_window, text="Delete",
                               command=lambda: self.delete_from_watchlist(watchlist_item_id_entry, remove_item_window))
        delete_button.grid(row=len(items) + 1, column=2, padx=5, pady=5)

    def viewWatchlists(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        # Using RIGHT JOIN to fetch data
        right_join_query = """
        SELECT W.watchlist_id, W.name AS watchlist_name, 
               WI.show_id, S.title AS show_title, 
               WI.movie_id, M.title AS movie_title
        FROM Watchlist_Item WI
        RIGHT JOIN Watchlist W ON WI.watchlist_id = W.watchlist_id
        LEFT JOIN TV_Show S ON WI.show_id = S.show_id
        LEFT JOIN Movie M ON WI.movie_id = M.movie_id
        WHERE W.user_id = %s
        """
        cursor.execute(right_join_query, (self.user_id,))
        watchlists = cursor.fetchall()

        column_names = ["Watchlist ID", "Watchlist Name", "Show ID", "Show Title", "Movie ID", "Movie Title"]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, watchlist in enumerate(watchlists, start=1):
            for j, value in enumerate(watchlist):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def go_home(self):
        self.window.destroy()
        Main_App().run()

    def run(self):
        self.window.mainloop()

class Main_App:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("400x400")
        self.window.resizable(True, True)
        self.window.config(background="#FFC0CB")
        self.window.title("TV Show and Movie Management System")

        user_button = Button(self.window, text="User Login", width=46, height=3, command=self.open_user_login)
        user_button.place(x=2, y=5)

        critic_button = Button(self.window, text="Critic Login", width=46, height=3, command=self.open_critic_login)
        critic_button.place(x=2, y=75)

        admin_button = Button(self.window, text="Admin Login", width=46, height=3, command=self.open_admin_app)
        admin_button.place(x=2, y=145)

        most_watched_movies_button = Button(self.window, text="Most Watched Movies", width=46, height=3, command=self.viewMostWatchedMovies)
        most_watched_movies_button.place(x=2, y=215)

        most_watched_shows_button = Button(self.window, text="Most Watched Shows", width=46, height=3, command=self.viewMostWatchedShows)
        most_watched_shows_button.place(x=2, y=285)

    def open_user_login(self):
        self.window.destroy()
        User_Login().run()

    def open_critic_login(self):
        self.window.destroy()
        Critic_Login().run()

    def open_admin_app(self):
        self.window.destroy()
        Admin_App().run()

    def viewMostWatchedMovies(self):
        self.window.destroy()
        View_Most_Watched_Movies().run()

    def viewMostWatchedShows(self):
        self.window.destroy()
        View_Most_Watched_Shows().run()

    def run(self):
        self.window.mainloop()

class View_Most_Watched_Movies:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        self.window.config(background="#FFC0CB")
        self.window.title("Most Watched Movies")

        home_button = Button(self.window, text="Home", command=self.go_home)
        home_button.pack()

        self.entries = []
        self.create_scrollable_frame()
        self.viewMostWatchedMovies()

    def create_scrollable_frame(self):
        self.canvas = Canvas(self.window)
        self.scrollable_frame = Frame(self.canvas)
        self.scrollbar = Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def viewMostWatchedMovies(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        cursor.execute("SELECT * FROM MostWatchedMovies")
        most_watched = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, item in enumerate(most_watched, start=1):
            for j, value in enumerate(item):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def go_home(self):
        self.window.destroy()
        Main_App().run()

    def run(self):
        self.window.mainloop()

class View_Most_Watched_Shows:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        self.window.config(background="#FFC0CB")
        self.window.title("Most Watched Shows")

        home_button = Button(self.window, text="Home", command=self.go_home)
        home_button.pack()

        self.entries = []
        self.create_scrollable_frame()
        self.viewMostWatchedShows()

    def create_scrollable_frame(self):
        self.canvas = Canvas(self.window)
        self.scrollable_frame = Frame(self.canvas)
        self.scrollbar = Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def viewMostWatchedShows(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        cursor.execute("SELECT * FROM MostWatchedShows")
        most_watched = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, item in enumerate(most_watched, start=1):
            for j, value in enumerate(item):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def go_home(self):
        self.window.destroy()
        Main_App().run()

    def run(self):
        self.window.mainloop()


class Admin_App:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        self.window.config(background="#FFC0CB")
        self.window.title("Admin")

        home_button = Button(self.window, text="Home", command=self.go_home)
        home_button.pack()

        self.entries = []
        self.create_scrollable_frame()

        view_users_button = Button(self.window, text="View Users", width=12, height=3, command=self.viewUsers)
        view_users_button.pack()

        view_reviews_button = Button(self.window, text="View Reviews", width=12, height=3, command=self.viewReviews)
        view_reviews_button.pack()

        view_most_watched_button = Button(self.window, text="Most Watched", width=12, height=3, command=self.viewMostWatched)
        view_most_watched_button.pack()

        view_most_reviewed_button = Button(self.window, text="Most Reviewed", width=12, height=3, command=self.viewMostReviewed)
        view_most_reviewed_button.pack()

        view_worst_rated_button = Button(self.window, text="Worst Rated", width=12, height=3, command=self.viewWorstRated)
        view_worst_rated_button.pack()

        view_cast_button = Button(self.window, text="View Cast", width=12, height=3, command=self.viewCast)
        view_cast_button.pack()

        view_crew_button = Button(self.window, text="View Crew", width=12, height=3, command=self.viewCrew)
        view_crew_button.pack()

        add_movie_button = Button(self.window, text="Add Movie", width=12, height=3, command=self.addMovie)
        add_movie_button.pack()

        list_movie_button = Button(self.window, text="List Movies", width=12, height=3, command=self.listMovies)
        list_movie_button.pack()

        add_show_button = Button(self.window, text="Add TV Show", width=12, height=3, command=self.addTVShow)
        add_show_button.pack()

        list_show_button = Button(self.window, text="List TV Shows", width=12, height=3, command=self.listTVShows)
        list_show_button.pack()

        add_movie_with_director_button = Button(self.window, text="Add Movie with Director", width=20, height=3, command=self.addMovieWithDirector)
        add_movie_with_director_button.pack()

        add_show_with_director_button = Button(self.window, text="Add Show with Director", width=20, height=3, command=self.addShowWithDirector)
        add_show_with_director_button.pack()

    def create_scrollable_frame(self):
        self.canvas = Canvas(self.window)
        self.scrollable_frame = Frame(self.canvas)
        self.scrollbar = Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def viewUsers(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        cursor.execute("SELECT * FROM User")
        users = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, user in enumerate(users, start=1):
            for j, value in enumerate(user):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def viewReviews(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        cursor.execute("SELECT * FROM Review")
        reviews = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, review in enumerate(reviews, start=1):
            for j, value in enumerate(review):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def viewMostWatched(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        cursor.execute("SELECT * FROM MostWatchedMovies")
        most_watched = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, item in enumerate(most_watched, start=1):
            for j, value in enumerate(item):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def viewMostReviewed(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        cursor.execute("SELECT * FROM MostReviewedMovies")
        most_reviewed = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, item in enumerate(most_reviewed, start=1):
            for j, value in enumerate(item):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def viewWorstRated(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        cursor.execute("SELECT * FROM WorstRatedMovies")
        worst_rated = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, item in enumerate(worst_rated, start=1):
            for j, value in enumerate(item):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def viewCast(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        cursor.execute("""
            SELECT role, name 
            FROM Cast
            ORDER BY role, name
        """)
        cast = cursor.fetchall()

        column_names = ["Role", "Name"]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, member in enumerate(cast, start=1):
            for j, value in enumerate(member):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def show_cast(self, movie_id):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        cursor.callproc('GetCastAndCrew', (int(movie_id), 'M'))
        for result in cursor.stored_results():
            cast = result.fetchall()

        column_names = ["Name", "Role"]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, member in enumerate(cast, start=1):
            for j, value in enumerate(member):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def viewCrew(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        cursor.execute("""
             SELECT name, job_title 
             FROM Crew
             ORDER BY name
         """)
        crew = cursor.fetchall()

        column_names = ["Name", "Job Title"]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, member in enumerate(crew, start=1):
            for j, value in enumerate(member):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def show_crew(self, show_id):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        cursor.callproc('GetCastAndCrew', (int(show_id), 'S'))
        for result in cursor.stored_results():
            crew = result.fetchall()

        column_names = ["Name", "Job"]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, member in enumerate(crew, start=1):
            for j, value in enumerate(member):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def addMovie(self):
        def save_movie():
            title = title_entry.get()
            description = description_entry.get()
            release_date = release_date_entry.get()
            genre = genre_entry.get()
            rating = float(rating_entry.get())
            director_id = int(director_id_entry.get())

            global cursor, mydb
            cursor.execute("""INSERT INTO Movie (title, description, release_date, genre, rating, director_id) 
                              VALUES (%s, %s, %s, %s, %s, %s)""",
                           (title, description, release_date, genre, rating, director_id))
            mydb.commit()
            add_movie_window.destroy()

        add_movie_window = Tk()
        add_movie_window.geometry("400x400")
        add_movie_window.title("Add Movie")

        title_label = Label(add_movie_window, text="Title")
        title_label.pack()
        title_entry = Entry(add_movie_window)
        title_entry.pack()

        description_label = Label(add_movie_window, text="Description")
        description_label.pack()
        description_entry = Entry(add_movie_window)
        description_entry.pack()

        release_date_label = Label(add_movie_window, text="Release Date (YYYY-MM-DD)")
        release_date_label.pack()
        release_date_entry = Entry(add_movie_window)
        release_date_entry.pack()

        genre_label = Label(add_movie_window, text="Genre")
        genre_label.pack()
        genre_entry = Entry(add_movie_window)
        genre_entry.pack()

        rating_label = Label(add_movie_window, text="Rating")
        rating_label.pack()
        rating_entry = Entry(add_movie_window)
        rating_entry.pack()

        director_id_label = Label(add_movie_window, text="Director ID")
        director_id_label.pack()
        director_id_entry = Entry(add_movie_window)
        director_id_entry.pack()

        save_button = Button(add_movie_window, text="Save", command=save_movie)
        save_button.pack()

    def listMovies(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        cursor.execute("SELECT * FROM Movie")
        movies = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, movie in enumerate(movies, start=1):
            for j, value in enumerate(movie):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def addTVShow(self):
        def save_show():
            title = title_entry.get()
            description = description_entry.get()
            release_date = release_date_entry.get()
            genre = genre_entry.get()
            rating = float(rating_entry.get())
            director_id = int(director_id_entry.get())

            global cursor, mydb
            cursor.execute("""INSERT INTO TV_Show (title, description, release_date, genre, rating, director_id) 
                              VALUES (%s, %s, %s, %s, %s, %s)""",
                           (title, description, release_date, genre, rating, director_id))
            mydb.commit()
            add_show_window.destroy()

        add_show_window = Tk()
        add_show_window.geometry("400x400")
        add_show_window.title("Add TV Show")

        title_label = Label(add_show_window, text="Title")
        title_label.pack()
        title_entry = Entry(add_show_window)
        title_entry.pack()

        description_label = Label(add_show_window, text="Description")
        description_label.pack()
        description_entry = Entry(add_show_window)
        description_entry.pack()

        release_date_label = Label(add_show_window, text="Release Date (YYYY-MM-DD)")
        release_date_label.pack()
        release_date_entry = Entry(add_show_window)
        release_date_entry.pack()

        genre_label = Label(add_show_window, text="Genre")
        genre_label.pack()
        genre_entry = Entry(add_show_window)
        genre_entry.pack()

        rating_label = Label(add_show_window, text="Rating")
        rating_label.pack()
        rating_entry = Entry(add_show_window)
        rating_entry.pack()

        director_id_label = Label(add_show_window, text="Director ID")
        director_id_label.pack()
        director_id_entry = Entry(add_show_window)
        director_id_entry.pack()

        save_button = Button(add_show_window, text="Save", command=save_show)
        save_button.pack()

    def addMovieWithDirector(self):
        def save_movie():
            title = title_entry.get()
            description = description_entry.get()
            release_date = release_date_entry.get()
            genre = genre_entry.get()
            rating = float(rating_entry.get())
            director_name = director_name_entry.get()

            global cursor, mydb
            cursor.callproc('AddMovieWithDirector', (title, description, release_date, genre, rating, director_name))
            mydb.commit()
            add_movie_window.destroy()

        add_movie_window = Tk()
        add_movie_window.geometry("400x400")
        add_movie_window.title("Add Movie with Director")

        title_label = Label(add_movie_window, text="Title")
        title_label.pack()
        title_entry = Entry(add_movie_window)
        title_entry.pack()

        description_label = Label(add_movie_window, text="Description")
        description_label.pack()
        description_entry = Entry(add_movie_window)
        description_entry.pack()

        release_date_label = Label(add_movie_window, text="Release Date (YYYY-MM-DD)")
        release_date_label.pack()
        release_date_entry = Entry(add_movie_window)
        release_date_entry.pack()

        genre_label = Label(add_movie_window, text="Genre")
        genre_label.pack()
        genre_entry = Entry(add_movie_window)
        genre_entry.pack()

        rating_label = Label(add_movie_window, text="Rating")
        rating_label.pack()
        rating_entry = Entry(add_movie_window)
        rating_entry.pack()

        director_name_label = Label(add_movie_window, text="Director Name")
        director_name_label.pack()
        director_name_entry = Entry(add_movie_window)
        director_name_entry.pack()

        save_button = Button(add_movie_window, text="Save", command=save_movie)
        save_button.pack()

    def addShowWithDirector(self):
        def save_show():
            title = title_entry.get()
            description = description_entry.get()
            release_date = release_date_entry.get()
            genre = genre_entry.get()
            rating = float(rating_entry.get())
            director_name = director_name_entry.get()

            global cursor, mydb
            cursor.callproc('AddShowWithDirector', (title, description, release_date, genre, rating, director_name))
            mydb.commit()
            add_show_window.destroy()

        add_show_window = Tk()
        add_show_window.geometry("400x400")
        add_show_window.title("Add Show with Director")

        title_label = Label(add_show_window, text="Title")
        title_label.pack()
        title_entry = Entry(add_show_window)
        title_entry.pack()

        description_label = Label(add_show_window, text="Description")
        description_label.pack()
        description_entry = Entry(add_show_window)
        description_entry.pack()

        release_date_label = Label(add_show_window, text="Release Date (YYYY-MM-DD)")
        release_date_label.pack()
        release_date_entry = Entry(add_show_window)
        release_date_entry.pack()

        genre_label = Label(add_show_window, text="Genre")
        genre_label.pack()
        genre_entry = Entry(add_show_window)
        genre_entry.pack()

        rating_label = Label(add_show_window, text="Rating")
        rating_label.pack()
        rating_entry = Entry(add_show_window)
        rating_entry.pack()

        director_name_label = Label(add_show_window, text="Director Name")
        director_name_label.pack()
        director_name_entry = Entry(add_show_window)
        director_name_entry.pack()

        save_button = Button(add_show_window, text="Save", command=save_show)
        save_button.pack()

    def listTVShows(self):
        global cursor
        close_previous_results(cursor)
        clearEntries(self.entries)

        cursor.execute("SELECT * FROM TV_Show")
        shows = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        for j, column_name in enumerate(column_names):
            entry = Entry(self.scrollable_frame, width=20, fg='black')
            entry.grid(row=0, column=j, padx=5, pady=5)
            entry.insert(END, column_name)
            self.entries.append(entry)

        for i, show in enumerate(shows, start=1):
            for j, value in enumerate(show):
                entry = Entry(self.scrollable_frame, width=20, fg='black')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(END, str(value))
                self.entries.append(entry)

    def go_home(self):
        self.window.destroy()
        Main_App().run()

    def run(self):
        self.window.mainloop()
def clearEntries(entries):
    for entry in entries:
        entry.destroy()
    entries.clear()


if __name__ == "__main__":
    main_app = Main_App()
    main_app.run()


# from tkinter import *
# from tkinter import messagebox
# from connection import *
#
# mydb, cursor = initialize_connection()
# mydb.autocommit = False
#
# def close_previous_results(cursor):
#     while cursor.nextset():
#         pass
#
# class Main_App:
#     def __init__(self):
#         self.window = Tk()
#         self.window.geometry("400x290")
#         self.window.resizable(True, True)
#         self.window.config(background="#FFC0CB")
#         self.window.title("TV Show and Movie Management System")
#
#         user_button = Button(self.window, text="User Login", width=46, height=3, command=self.open_user_login)
#         user_button.place(x=2, y=5)
#
#         critic_button = Button(self.window, text="Critic Login", width=46, height=3, command=self.open_critic_login)
#         critic_button.place(x=2, y=75)
#
#         admin_button = Button(self.window, text="Admin Login", width=46, height=3, command=self.open_admin_app)
#         admin_button.place(x=2, y=145)
#
#     def open_user_login(self):
#         self.window.destroy()
#         User_Login()
#
#     def open_critic_login(self):
#         self.window.destroy()
#         Critic_Login().run()
#
#     # def open_critic_app(self):
#     #     self.window.destroy()
#     #     Critic_App()
#
#     def open_admin_app(self):
#         self.window.destroy()
#         Admin_App()
#
#     def run(self):
#         self.window.mainloop()
#
# class Critic_Login:
#     def __init__(self):
#         self.window = Tk()
#         self.window.geometry("400x290")
#         self.window.resizable(True, True)
#         self.window.config(background="#FFC0CB")
#         self.window.title("Critic Login")
#
#         username_label = Label(self.window, text="Username")
#         username_label.pack()
#         self.username_entry = Entry(self.window)
#         self.username_entry.pack()
#
#         password_label = Label(self.window, text="Password")
#         password_label.pack()
#         self.password_entry = Entry(self.window, show="*")
#         self.password_entry.pack()
#
#         login_button = Button(self.window, text="Login", command=self.login)
#         login_button.pack()
#
#     def login(self):
#         username = self.username_entry.get()
#         password = self.password_entry.get()
#
#         global cursor
#         close_previous_results(cursor)
#         cursor.execute("SELECT user_id FROM User WHERE username = %s AND password = %s AND role = 'critic'", (username, password))
#         result = cursor.fetchone()
#
#         if result:
#             user_id = result[0]
#             self.window.destroy()
#             Critic_App(user_id)
#         else:
#             messagebox.showerror("Error", "Invalid username or password")
#
#     def run(self):
#         self.window.mainloop()
#
#
#
# class User_Login:
#     def __init__(self):
#         self.window = Tk()
#         self.window.geometry("400x290")
#         self.window.resizable(True, True)
#         self.window.config(background="#FFC0CB")
#         self.window.title("User Login")
#
#         username_label = Label(self.window, text="Username")
#         username_label.pack()
#         self.username_entry = Entry(self.window)
#         self.username_entry.pack()
#
#         password_label = Label(self.window, text="Password")
#         password_label.pack()
#         self.password_entry = Entry(self.window, show="*")
#         self.password_entry.pack()
#
#         login_button = Button(self.window, text="Login", command=self.login)
#         login_button.pack()
#
#     def login(self):
#         username = self.username_entry.get()
#         password = self.password_entry.get()
#
#         global cursor
#         close_previous_results(cursor)
#         cursor.execute("SELECT user_id FROM User WHERE username = %s AND password = %s AND role = 'viewer'", (username, password))
#         result = cursor.fetchone()
#
#         if result:
#             user_id = result[0]
#             self.window.destroy()
#             User_App(user_id)
#         else:
#             messagebox.showerror("Error", "Invalid username or password")
#
#     def run(self):
#         self.window.mainloop()
#
# class User_App:
#     def __init__(self, user_id):
#         self.user_id = user_id
#         self.window = Tk()
#         self.window.geometry("800x600")
#         self.window.resizable(True, True)
#         self.window.config(background="#FFC0CB")
#         self.window.title("User")
#
#         home_button = Button(self.window, text="Home", command=self.go_home)
#         home_button.pack()
#
#         self.entries = []
#         self.create_scrollable_frame()
#
#         list_movie_button = Button(self.window, text="List Movies", width=12, height=3, command=self.listMovies)
#         list_movie_button.pack()
#
#         list_show_button = Button(self.window, text="List Shows", width=12, height=3, command=self.listShows)
#         list_show_button.pack()
#
#         search_button = Button(self.window, text="Search", width=12, height=3, command=self.searchMoviesAndShows)
#         search_button.pack()
#         write_review_button = Button(self.window, text="Write Review", width=12, height=3, command=self.writeReview)
#         write_review_button.pack()
#
#         edit_review_button = Button(self.window, text="Edit Review", width=12, height=3, command=self.editReview)
#         edit_review_button.pack()
#
#         delete_review_button = Button(self.window, text="Delete Review", width=12, height=3, command=self.deleteReview)
#         delete_review_button.pack()
#
#         view_reviews_button = Button(self.window, text="View Reviews", width=12, height=3, command=self.viewReviews)
#         view_reviews_button.pack()
#
#         create_watchlist_button = Button(self.window, text="Create Watchlist", width=12, height=3, command=self.createWatchlist)
#         create_watchlist_button.pack()
#
#         add_to_watchlist_button = Button(self.window, text="Add to Watchlist", width=12, height=3, command=self.addToWatchlist)
#         add_to_watchlist_button.pack()
#
#         remove_from_watchlist_button = Button(self.window, text="Remove from Watchlist", width=12, height=3, command=self.removeFromWatchlist)
#         remove_from_watchlist_button.pack()
#
#         view_watchlist_button = Button(self.window, text="View Watchlists", width=12, height=3, command=self.viewWatchlists)
#         view_watchlist_button.pack()
#
#     def viewWatchlists(self):
#         global cursor
#         close_previous_results(cursor)
#         clearEntries(self.entries)
#
#         # Prompt the user to select a watchlist
#         watchlist_selection_window = Tk()
#         watchlist_selection_window.geometry("400x200")
#         watchlist_selection_window.title("Select Watchlist")
#
#         watchlist_id_label = Label(watchlist_selection_window, text="Watchlist ID or Name")
#         watchlist_id_label.pack()
#         watchlist_id_entry = Entry(watchlist_selection_window)
#         watchlist_id_entry.pack()
#
#         def show_watchlist():
#             watchlist_id_or_name = watchlist_id_entry.get()
#             watchlist_selection_window.destroy()
#             self.display_watchlist_items(watchlist_id_or_name)
#
#         show_button = Button(watchlist_selection_window, text="Show", command=show_watchlist)
#         show_button.pack()
#
#     def display_watchlist_items(self, watchlist_id_or_name):
#         global cursor
#         close_previous_results(cursor)
#         clearEntries(self.entries)
#
#         # Query to fetch watchlist items based on watchlist ID or name
#         query = """
#         SELECT W.watchlist_id, W.name AS watchlist_name,
#                WI.show_id, S.title AS show_title,
#                WI.movie_id, M.title AS movie_title
#         FROM Watchlist W
#         LEFT JOIN Watchlist_Item WI ON W.watchlist_id = WI.watchlist_id
#         LEFT JOIN TV_Show S ON WI.show_id = S.show_id
#         LEFT JOIN Movie M ON WI.movie_id = M.movie_id
#         WHERE W.user_id = %s AND (W.watchlist_id = %s OR W.name = %s)
#         """
#         cursor.execute(query, (self.user_id, watchlist_id_or_name, watchlist_id_or_name))
#         watchlists = cursor.fetchall()
#
#         column_names = ["Watchlist ID", "Watchlist Name", "Show ID", "Show Title", "Movie ID", "Movie Title"]
#         for j, column_name in enumerate(column_names):
#             entry = Entry(self.scrollable_frame, width=20, fg='black')
#             entry.grid(row=0, column=j, padx=5, pady=5)
#             entry.insert(END, column_name)
#             self.entries.append(entry)
#
#         for i, watchlist in enumerate(watchlists, start=1):
#             for j, value in enumerate(watchlist):
#                 entry = Entry(self.scrollable_frame, width=20, fg='black')
#                 entry.grid(row=i, column=j, padx=5, pady=5)
#                 entry.insert(END, str(value))
#                 self.entries.append(entry)
#     def searchMoviesAndShows(self):
#         search_window = Tk()
#         search_window.geometry("400x400")
#         search_window.title("Search Movies and Shows")
#
#         search_label = Label(search_window, text="Search")
#         search_label.pack()
#         search_entry = Entry(search_window)
#         search_entry.pack()
#
#         genre_label = Label(search_window, text="Genre")
#         genre_label.pack()
#         genre_entry = Entry(search_window)
#         genre_entry.pack()
#
#         rating_label = Label(search_window, text="Rating")
#         rating_label.pack()
#         rating_entry = Entry(search_window)
#         rating_entry.pack()
#
#         release_date_label = Label(search_window, text="Release Date (YYYY-MM-DD)")
#         release_date_label.pack()
#         release_date_entry = Entry(search_window)
#         release_date_entry.pack()
#
#         search_button = Button(search_window, text="Search", command=lambda: self.execute_search(search_entry, genre_entry, rating_entry, release_date_entry, search_window))
#         search_button.pack()
#
#     def execute_search(self, search_entry, genre_entry, rating_entry, release_date_entry, search_window):
#         search_term = search_entry.get()
#         genre = genre_entry.get()
#         rating = rating_entry.get()
#         release_date = release_date_entry.get()
#
#         global cursor
#         close_previous_results(cursor)
#         clearEntries(self.entries)
#
#         query = """
#         SELECT movie_id, title, description, release_date, genre, rating, director_id FROM Movie
#         WHERE (title LIKE %s OR description LIKE %s)
#         """
#         params = [f"%{search_term}%", f"%{search_term}%"]
#
#         if genre:
#             query += " AND genre = %s"
#             params.append(genre)
#         if rating:
#             query += " AND rating >= %s"
#             params.append(rating)
#         if release_date:
#             query += " AND release_date = %s"
#             params.append(release_date)
#
#         cursor.execute(query, params)
#         movies = cursor.fetchall()
#
#         column_names = [desc[0] for desc in cursor.description]
#         for j, column_name in enumerate(column_names):
#             entry = Entry(self.scrollable_frame, width=20, fg='black')
#             entry.grid(row=0, column=j, padx=5, pady=5)
#             entry.insert(END, column_name)
#             self.entries.append(entry)
#
#         for i, movie in enumerate(movies, start=1):
#             for j, value in enumerate(movie):
#                 entry = Entry(self.scrollable_frame, width=20, fg='black')
#                 entry.grid(row=i, column=j, padx=5, pady=5)
#                 entry.insert(END, str(value))
#                 self.entries.append(entry)
#
#         search_window.destroy()
#
#     def create_scrollable_frame(self):
#         self.canvas = Canvas(self.window)
#         self.scrollable_frame = Frame(self.canvas)
#         self.scrollbar = Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
#         self.canvas.configure(yscrollcommand=self.scrollbar.set)
#
#         self.scrollbar.pack(side="right", fill="y")
#         self.canvas.pack(side="left", fill="both", expand=True)
#         self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
#         self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
#
#     def listMovies(self):
#         global cursor
#         close_previous_results(cursor)
#         clearEntries(self.entries)
#
#         cursor.execute("SELECT * FROM Movie")
#         movies = cursor.fetchall()
#
#         column_names = [desc[0] for desc in cursor.description]
#         for j, column_name in enumerate(column_names):
#             entry = Entry(self.scrollable_frame, width=20, fg='black')
#             entry.grid(row=0, column=j, padx=5, pady=5)
#             entry.insert(END, column_name)
#             self.entries.append(entry)
#
#         for i, movie in enumerate(movies, start=1):
#             for j, value in enumerate(movie):
#                 entry = Entry(self.scrollable_frame, width=20, fg='black')
#                 entry.grid(row=i, column=j, padx=5, pady=5)
#                 entry.insert(END, str(value))
#                 self.entries.append(entry)
#
#     def listShows(self):
#         global cursor
#         close_previous_results(cursor)
#         clearEntries(self.entries)
#
#         cursor.execute("SELECT * FROM TV_Show")
#         shows = cursor.fetchall()
#
#         column_names = [desc[0] for desc in cursor.description]
#         for j, column_name in enumerate(column_names):
#             entry = Entry(self.scrollable_frame, width=20, fg='black')
#             entry.grid(row=0, column=j, padx=5, pady=5)
#             entry.insert(END, column_name)
#             self.entries.append(entry)
#
#         for i, show in enumerate(shows, start=1):
#             for j, value in enumerate(show):
#                 entry = Entry(self.scrollable_frame, width=20, fg='black')
#                 entry.grid(row=i, column=j, padx=5, pady=5)
#                 entry.insert(END, str(value))
#                 self.entries.append(entry)
#
#     def writeReview(self):
#         review_window = Tk()
#         review_window.geometry("400x400")
#         review_window.title("Write Review")
#
#         rating_label = Label(review_window, text="Rating")
#         rating_label.pack()
#         rating_entry = Entry(review_window)
#         rating_entry.pack()
#
#         review_text_label = Label(review_window, text="Review Text")
#         review_text_label.pack()
#         review_text_entry = Entry(review_window)
#         review_text_entry.pack()
#
#         review_date_label = Label(review_window, text="Review Date (YYYY-MM-DD)")
#         review_date_label.pack()
#         review_date_entry = Entry(review_window)
#         review_date_entry.pack()
#
#         save_button = Button(review_window, text="Save", command=lambda: self.save_review(rating_entry, review_text_entry, review_date_entry, review_window))
#         save_button.pack()
#
#     def save_review(self, rating_entry, review_text_entry, review_date_entry, review_window):
#         rating = float(rating_entry.get())
#         review_text = review_text_entry.get()
#         review_date = review_date_entry.get()
#
#         global cursor, mydb
#         cursor.execute("""INSERT INTO Review (user_id, rating, review_text, review_date)
#                           VALUES (%s, %s, %s, %s)""",
#                        (self.user_id, rating, review_text, review_date))
#         mydb.commit()
#         review_window.destroy()
#
#     def editReview(self):
#         edit_review_window = Tk()
#         edit_review_window.geometry("400x400")
#         edit_review_window.title("Edit Review")
#
#         review_id_label = Label(edit_review_window, text="Review ID")
#         review_id_label.pack()
#         review_id_entry = Entry(edit_review_window)
#         review_id_entry.pack()
#
#         rating_label = Label(edit_review_window, text="New Rating")
#         rating_label.pack()
#         rating_entry = Entry(edit_review_window)
#         rating_entry.pack()
#
#         review_text_label = Label(edit_review_window, text="New Review Text")
#         review_text_label.pack()
#         review_text_entry = Entry(edit_review_window)
#         review_text_entry.pack()
#
#         save_button = Button(edit_review_window, text="Save", command=lambda: self.update_review(review_id_entry, rating_entry, review_text_entry, edit_review_window))
#         save_button.pack()
#
#     def update_review(self, review_id_entry, rating_entry, review_text_entry, edit_review_window):
#         review_id = int(review_id_entry.get())
#         new_rating = float(rating_entry.get())
#         new_review_text = review_text_entry.get()
#
#         global cursor, mydb
#         cursor.execute("""UPDATE Review SET rating = %s, review_text = %s WHERE review_id = %s""",
#                        (new_rating, new_review_text, review_id))
#         mydb.commit()
#         edit_review_window.destroy()
#
#     def deleteReview(self):
#         delete_review_window = Tk()
#         delete_review_window.geometry("400x400")
#         delete_review_window.title("Delete Review")
#
#         review_id_label = Label(delete_review_window, text="Review ID")
#         review_id_label.pack()
#         review_id_entry = Entry(delete_review_window)
#         review_id_entry.pack()
#
#         delete_button = Button(delete_review_window, text="Delete", command=lambda: self.remove_review(review_id_entry, delete_review_window))
#         delete_button.pack()
#
#     def remove_review(self, review_id_entry, delete_review_window):
#         review_id = int(review_id_entry.get())
#
#         global cursor, mydb
#         cursor.execute("""DELETE FROM Review WHERE review_id = %s""", (review_id,))
#         mydb.commit()
#         delete_review_window.destroy()
#
#
#     def viewReviews(self):
#         global cursor
#         close_previous_results(cursor)
#         clearEntries(self.entries)
#
#         cursor.execute("""SELECT R.review_id, U.username, M.title, S.title, R.rating, R.review_text, R.review_date
#                           FROM Review R
#                           LEFT JOIN User U ON R.user_id = U.user_id
#                           LEFT JOIN Movie M ON R.movie_id = M.movie_id
#                           LEFT JOIN TV_Show S ON R.show_id = S.show_id
#                           WHERE R.user_id = %s""", (self.user_id,))
#         reviews = cursor.fetchall()
#
#         column_names = [desc[0] for desc in cursor.description]
#         for j, column_name in enumerate(column_names):
#             entry = Entry(self.scrollable_frame, width=20, fg='black')
#             entry.grid(row=0, column=j, padx=5, pady=5)
#             entry.insert(END, column_name)
#             self.entries.append(entry)
#
#         for i, review in enumerate(reviews, start=1):
#             for j, value in enumerate(review):
#                 entry = Entry(self.scrollable_frame, width=20, fg='black')
#                 entry.grid(row=i, column=j, padx=5, pady=5)
#                 entry.insert(END, str(value))
#                 self.entries.append(entry)
#
#     def createWatchlist(self):
#         watchlist_window = Tk()
#         watchlist_window.geometry("400x400")
#         watchlist_window.title("Create Watchlist")
#
#         name_label = Label(watchlist_window, text="Watchlist Name")
#         name_label.pack()
#         name_entry = Entry(watchlist_window)
#         name_entry.pack()
#
#         save_button = Button(watchlist_window, text="Save",
#                              command=lambda: self.save_watchlist(name_entry, watchlist_window))
#         save_button.pack()
#
#     def save_watchlist(self, name_entry, watchlist_window):
#         name = name_entry.get()
#
#         global cursor, mydb
#         cursor.execute("""INSERT INTO Watchlist (user_id, name) VALUES (%s, %s)""", (self.user_id, name))
#         mydb.commit()
#         watchlist_window.destroy()
#
#     def addToWatchlist(self):
#         add_window = Tk()
#         add_window.geometry("400x400")
#         add_window.title("Add to Watchlist")
#
#         watchlist_id_label = Label(add_window, text="Watchlist ID")
#         watchlist_id_label.pack()
#         watchlist_id_entry = Entry(add_window)
#         watchlist_id_entry.pack()
#
#         show_id_label = Label(add_window, text="Show ID (if applicable)")
#         show_id_label.pack()
#         show_id_entry = Entry(add_window)
#         show_id_entry.pack()
#
#         movie_id_label = Label(add_window, text="Movie ID (if applicable)")
#         movie_id_label.pack()
#         movie_id_entry = Entry(add_window)
#         movie_id_entry.pack()
#
#         save_button = Button(add_window, text="Save",
#                              command=lambda: self.save_to_watchlist(watchlist_id_entry, show_id_entry, movie_id_entry,
#                                                                     add_window))
#         save_button.pack()
#
#     def save_to_watchlist(self, watchlist_id_entry, show_id_entry, movie_id_entry, add_window):
#         watchlist_id = int(watchlist_id_entry.get())
#         show_id = int(show_id_entry.get()) if show_id_entry.get() else None
#         movie_id = int(movie_id_entry.get()) if movie_id_entry.get() else None
#
#         global cursor, mydb
#         cursor.execute("""INSERT INTO Watchlist_Item (watchlist_id, show_id, movie_id)
#                            VALUES (%s, %s, %s)""",
#                        (watchlist_id, show_id, movie_id))
#         mydb.commit()
#         add_window.destroy()
#
#     def removeFromWatchlist(self):
#         remove_window = Tk()
#         remove_window.geometry("400x200")
#         remove_window.title("Remove from Watchlist")
#
#         watchlist_id_label = Label(remove_window, text="Watchlist ID")
#         watchlist_id_label.pack()
#         watchlist_id_entry = Entry(remove_window)
#         watchlist_id_entry.pack()
#
#         def show_items_to_remove():
#             watchlist_id = int(watchlist_id_entry.get())
#             remove_window.destroy()
#             self.show_watchlist_items_to_remove(watchlist_id)
#
#         show_button = Button(remove_window, text="Show Items", command=show_items_to_remove)
#         show_button.pack()
#
#     def delete_from_watchlist(self, watchlist_item_id_entry, remove_window):
#         watchlist_item_id = int(watchlist_item_id_entry.get())
#
#         global cursor, mydb
#         cursor.execute("""DELETE FROM Watchlist_Item WHERE watchlist_item_id = %s""", (watchlist_item_id,))
#         mydb.commit()
#         remove_window.destroy()
#
#     def show_watchlist_items_to_remove(self, watchlist_id):
#         global cursor
#         close_previous_results(cursor)
#         clearEntries(self.entries)
#
#         # Simulating a full outer join using UNION of left and right joins
#         full_outer_join_query = """
#         SELECT WI.watchlist_item_id, WI.show_id, S.title AS show_title,
#                WI.movie_id, M.title AS movie_title
#         FROM Watchlist_Item WI
#         LEFT JOIN TV_Show S ON WI.show_id = S.show_id
#         LEFT JOIN Movie M ON WI.movie_id = M.movie_id
#         WHERE WI.watchlist_id = %s
#         UNION
#         SELECT WI.watchlist_item_id, WI.show_id, S.title AS show_title,
#                WI.movie_id, M.title AS movie_title
#         FROM Watchlist_Item WI
#         RIGHT JOIN TV_Show S ON WI.show_id = S.show_id
#         RIGHT JOIN Movie M ON WI.movie_id = M.movie_id
#         WHERE WI.watchlist_id = %s AND WI.watchlist_item_id IS NULL
#         """
#         cursor.execute(full_outer_join_query, (watchlist_id, watchlist_id))
#         items = cursor.fetchall()
#
#         remove_item_window = Tk()
#         remove_item_window.geometry("600x400")
#         remove_item_window.title("Remove Watchlist Item")
#
#         column_names = ["Watchlist Item ID", "Show ID", "Show Title", "Movie ID", "Movie Title"]
#         for j, column_name in enumerate(column_names):
#             entry = Entry(remove_item_window, width=20, fg='black')
#             entry.grid(row=0, column=j, padx=5, pady=5)
#             entry.insert(END, column_name)
#
#         for i, item in enumerate(items, start=1):
#             for j, value in enumerate(item):
#                 entry = Entry(remove_item_window, width=20, fg='black')
#                 entry.grid(row=i, column=j, padx=5, pady=5)
#                 entry.insert(END, str(value))
#
#         watchlist_item_id_label = Label(remove_item_window, text="Watchlist Item ID to Remove")
#         watchlist_item_id_label.grid(row=len(items) + 1, column=0, padx=5, pady=5)
#         watchlist_item_id_entry = Entry(remove_item_window)
#         watchlist_item_id_entry.grid(row=len(items) + 1, column=1, padx=5, pady=5)
#
#         delete_button = Button(remove_item_window, text="Delete",
#                                command=lambda: self.delete_from_watchlist(watchlist_item_id_entry, remove_item_window))
#         delete_button.grid(row=len(items) + 1, column=2, padx=5, pady=5)
#
#     def viewWatchlists(self):
#         global cursor
#         close_previous_results(cursor)
#         clearEntries(self.entries)
#
#         # Using RIGHT JOIN to fetch data
#         right_join_query = """
#         SELECT W.watchlist_id, W.name AS watchlist_name,
#                WI.show_id, S.title AS show_title,
#                WI.movie_id, M.title AS movie_title
#         FROM Watchlist_Item WI
#         RIGHT JOIN Watchlist W ON WI.watchlist_id = W.watchlist_id
#         LEFT JOIN TV_Show S ON WI.show_id = S.show_id
#         LEFT JOIN Movie M ON WI.movie_id = M.movie_id
#         WHERE W.user_id = %s
#         """
#         cursor.execute(right_join_query, (self.user_id,))
#         watchlists = cursor.fetchall()
#
#         column_names = ["Watchlist ID", "Watchlist Name", "Show ID", "Show Title", "Movie ID", "Movie Title"]
#         for j, column_name in enumerate(column_names):
#             entry = Entry(self.scrollable_frame, width=20, fg='black')
#             entry.grid(row=0, column=j, padx=5, pady=5)
#             entry.insert(END, column_name)
#             self.entries.append(entry)
#
#         for i, watchlist in enumerate(watchlists, start=1):
#             for j, value in enumerate(watchlist):
#                 entry = Entry(self.scrollable_frame, width=20, fg='black')
#                 entry.grid(row=i, column=j, padx=5, pady=5)
#                 entry.insert(END, str(value))
#                 self.entries.append(entry)
#
#     def go_home(self):
#         self.window.destroy()
#         Main_App().run()
#
#     def run(self):
#         self.window.mainloop()
#
#
#
# class Critic_App:
#     def __init__(self, critic_id):
#         self.critic_id = critic_id
#         self.window = Tk()
#         self.window.geometry("800x600")
#         self.window.resizable(True, True)
#         self.window.config(background="#FFC0CB")
#         self.window.title("Critic")
#
#         home_button = Button(self.window, text="Home", command=self.go_home)
#         home_button.pack()
#
#         self.entries = []
#         self.create_scrollable_frame()
#
#         list_movie_button = Button(self.window, text="List Movies", width=12, height=3, command=self.listMovies)
#         list_movie_button.pack()
#
#         list_show_button = Button(self.window, text="List Shows", width=12, height=3, command=self.listShows)
#         list_show_button.pack()
#
#         write_review_button = Button(self.window, text="Write Review", width=12, height=3, command=self.writeReview)
#         write_review_button.pack()
#
#         edit_review_button = Button(self.window, text="Edit Review", width=12, height=3, command=self.editReview)
#         edit_review_button.pack()
#
#         delete_review_button = Button(self.window, text="Delete Review", width=12, height=3, command=self.deleteReview)
#         delete_review_button.pack()
#
#         view_reviews_button = Button(self.window, text="View My Reviews", width=12, height=3, command=self.viewReviews)
#         view_reviews_button.pack()
#
#     def create_scrollable_frame(self):
#         self.canvas = Canvas(self.window)
#         self.scrollable_frame = Frame(self.canvas)
#         self.scrollbar = Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
#         self.canvas.configure(yscrollcommand=self.scrollbar.set)
#
#         self.scrollbar.pack(side="right", fill="y")
#         self.canvas.pack(side="left", fill="both", expand=True)
#         self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
#         self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
#
#     def listMovies(self):
#         global cursor
#         clearEntries(self.entries)
#
#         cursor.execute("SELECT * FROM Movie")
#         movies = cursor.fetchall()  # Fetch all rows at once
#
#         column_names = [desc[0] for desc in cursor.description]
#         for j, column_name in enumerate(column_names):
#             entry = Entry(self.scrollable_frame, width=20, fg='black')
#             entry.grid(row=0, column=j, padx=5, pady=5)
#             entry.insert(END, column_name)
#             self.entries.append(entry)
#
#         for i, movie in enumerate(movies, start=1):
#             for j, value in enumerate(movie):
#                 entry = Entry(self.scrollable_frame, width=20, fg='black')
#                 entry.grid(row=i, column=j, padx=5, pady=5)
#                 entry.insert(END, str(value))
#                 self.entries.append(entry)
#
#     def listShows(self):
#         global cursor
#         clearEntries(self.entries)
#
#         cursor.execute("SELECT * FROM TV_Show")
#         shows = cursor.fetchall()  # Fetch all rows at once
#
#         column_names = [desc[0] for desc in cursor.description]
#         for j, column_name in enumerate(column_names):
#             entry = Entry(self.scrollable_frame, width=20, fg='black')
#             entry.grid(row=0, column=j, padx=5, pady=5)
#             entry.insert(END, column_name)
#             self.entries.append(entry)
#
#         for i, show in enumerate(shows, start=1):
#             for j, value in enumerate(show):
#                 entry = Entry(self.scrollable_frame, width=20, fg='black')
#                 entry.grid(row=i, column=j, padx=5, pady=5)
#                 entry.insert(END, str(value))
#                 self.entries.append(entry)
#
#     def writeReview(self):
#         review_window = Tk()
#         review_window.geometry("400x400")
#         review_window.title("Write Review")
#
#         show_id_label = Label(review_window, text="Show ID (if applicable)")
#         show_id_label.pack()
#         show_id_entry = Entry(review_window)
#         show_id_entry.pack()
#
#         movie_id_label = Label(review_window, text="Movie ID (if applicable)")
#         movie_id_label.pack()
#         movie_id_entry = Entry(review_window)
#         movie_id_entry.pack()
#
#         rating_label = Label(review_window, text="Rating")
#         rating_label.pack()
#         rating_entry = Entry(review_window)
#         rating_entry.pack()
#
#         review_text_label = Label(review_window, text="Review Text")
#         review_text_label.pack()
#         review_text_entry = Entry(review_window)
#         review_text_entry.pack()
#
#         review_date_label = Label(review_window, text="Review Date (YYYY-MM-DD)")
#         review_date_label.pack()
#         review_date_entry = Entry(review_window)
#         review_date_entry.pack()
#
#         save_button = Button(review_window, text="Save", command=lambda: self.save_review(show_id_entry, movie_id_entry, rating_entry, review_text_entry, review_date_entry, review_window))
#         save_button.pack()
#
#     def save_review(self, show_id_entry, movie_id_entry, rating_entry, review_text_entry, review_date_entry, review_window):
#         show_id = int(show_id_entry.get()) if show_id_entry.get() else None
#         movie_id = int(movie_id_entry.get()) if movie_id_entry.get() else None
#         rating = float(rating_entry.get())
#         review_text = review_text_entry.get()
#         review_date = review_date_entry.get()
#
#         global cursor, mydb
#         cursor.execute("""INSERT INTO Review (user_id, show_id, movie_id, rating, review_text, review_date)
#                           VALUES (%s, %s, %s, %s, %s, %s)""",
#                        (self.user_id, show_id, movie_id, rating, review_text, review_date))
#         mydb.commit()
#         review_window.destroy()
#
#     def editReview(self):
#         edit_review_window = Tk()
#         edit_review_window.geometry("400x400")
#         edit_review_window.title("Edit Review")
#
#         review_id_label = Label(edit_review_window, text="Review ID")
#         review_id_label.pack()
#         review_id_entry = Entry(edit_review_window)
#         review_id_entry.pack()
#
#         rating_label = Label(edit_review_window, text="New Rating")
#         rating_label.pack()
#         rating_entry = Entry(edit_review_window)
#         rating_entry.pack()
#
#         review_text_label = Label(edit_review_window, text="New Review Text")
#         review_text_label.pack()
#         review_text_entry = Entry(edit_review_window)
#         review_text_entry.pack()
#
#         save_button = Button(edit_review_window, text="Save", command=lambda: self.update_review(review_id_entry, rating_entry, review_text_entry, edit_review_window))
#         save_button.pack()
#
#     def viewReviews(self):
#         global cursor
#         close_previous_results(cursor)
#         clearEntries(self.entries)
#
#         cursor.execute("""SELECT * FROM CriticReviews WHERE user_id = %s""", (self.user_id,))
#         reviews = cursor.fetchall()
#
#         column_names = [desc[0] for desc in cursor.description]
#         for j, column_name in enumerate(column_names):
#             entry = Entry(self.scrollable_frame, width=20, fg='black')
#             entry.grid(row=0, column=j, padx=5, pady=5)
#             entry.insert(END, column_name)
#             self.entries.append(entry)
#
#         for i, review in enumerate(reviews, start=1):
#             for j, value in enumerate(review):
#                 entry = Entry(self.scrollable_frame, width=20, fg='black')
#                 entry.grid(row=i, column=j, padx=5, pady=5)
#                 entry.insert(END, str(value))
#                 self.entries.append(entry)
#     def update_review(self, review_id_entry, rating_entry, review_text_entry, edit_review_window):
#         review_id = int(review_id_entry.get())
#         new_rating = float(rating_entry.get())
#         new_review_text = review_text_entry.get()
#
#         global cursor, mydb
#         cursor.execute("""UPDATE Review SET rating = %s, review_text = %s WHERE review_id = %s AND user_id = %s""",
#                        (new_rating, new_review_text, review_id, self.user_id))
#         mydb.commit()
#         edit_review_window.destroy()
#
#     def deleteReview(self):
#         delete_review_window = Tk()
#         delete_review_window.geometry("400x400")
#         delete_review_window.title("Delete Review")
#
#         review_id_label = Label(delete_review_window, text="Review ID")
#         review_id_label.pack()
#         review_id_entry = Entry(delete_review_window)
#         review_id_entry.pack()
#
#         delete_button = Button(delete_review_window, text="Delete", command=lambda: self.remove_review(review_id_entry, delete_review_window))
#         delete_button.pack()
#
#     def remove_review(self, review_id_entry, delete_review_window):
#         review_id = int(review_id_entry.get())
#
#         global cursor, mydb
#         cursor.execute("""DELETE FROM Review WHERE review_id = %s AND user_id = %s""", (review_id, self.user_id))
#         mydb.commit()
#         delete_review_window.destroy()
#
#     def go_home(self):
#         self.window.destroy()
#         Main_App().run()
#
#     def run(self):
#         self.window.mainloop()
#
#
# class Admin_App:
#     def __init__(self):
#         self.window = Tk()
#         self.window.geometry("800x600")
#         self.window.resizable(True, True)
#         self.window.config(background="#FFC0CB")
#         self.window.title("Admin")
#
#         home_button = Button(self.window, text="Home", command=self.go_home)
#         home_button.pack()
#
#         self.entries = []
#         self.create_scrollable_frame()
#
#         view_users_button = Button(self.window, text="View Users", width=12, height=3, command=self.viewUsers)
#         view_users_button.pack()
#
#         view_reviews_button = Button(self.window, text="View Reviews", width=12, height=3, command=self.viewReviews)
#         view_reviews_button.pack()
#
#         view_most_watched_button = Button(self.window, text="Most Watched", width=12, height=3, command=self.viewMostWatched)
#         view_most_watched_button.pack()
#
#         view_most_reviewed_button = Button(self.window, text="Most Reviewed", width=12, height=3, command=self.viewMostReviewed)
#         view_most_reviewed_button.pack()
#
#         view_worst_rated_button = Button(self.window, text="Worst Rated", width=12, height=3, command=self.viewWorstRated)
#         view_worst_rated_button.pack()
#
#         view_cast_button = Button(self.window, text="View Cast", width=12, height=3, command=self.viewCast)
#         view_cast_button.pack()
#
#         view_crew_button = Button(self.window, text="View Crew", width=12, height=3, command=self.viewCrew)
#         view_crew_button.pack()
#
#         add_movie_button = Button(self.window, text="Add Movie", width=12, height=3, command=self.addMovie)
#         add_movie_button.pack()
#
#         list_movie_button = Button(self.window, text="List Movies", width=12, height=3, command=self.listMovies)
#         list_movie_button.pack()
#
#         add_show_button = Button(self.window, text="Add TV Show", width=12, height=3, command=self.addTVShow)
#         add_show_button.pack()
#
#         list_show_button = Button(self.window, text="List TV Shows", width=12, height=3, command=self.listTVShows)
#         list_show_button.pack()
#
#     def create_scrollable_frame(self):
#         self.canvas = Canvas(self.window)
#         self.scrollable_frame = Frame(self.canvas)
#         self.scrollbar = Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
#         self.canvas.configure(yscrollcommand=self.scrollbar.set)
#
#         self.scrollbar.pack(side="right", fill="y")
#         self.canvas.pack(side="left", fill="both", expand=True)
#         self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
#         self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
#
#     def viewUsers(self):
#         global cursor
#         close_previous_results(cursor)
#         clearEntries(self.entries)
#
#         cursor.execute("SELECT * FROM User")
#         users = cursor.fetchall()
#
#         column_names = [desc[0] for desc in cursor.description]
#         for j, column_name in enumerate(column_names):
#             entry = Entry(self.scrollable_frame, width=20, fg='black')
#             entry.grid(row=0, column=j, padx=5, pady=5)
#             entry.insert(END, column_name)
#             self.entries.append(entry)
#
#         for i, user in enumerate(users, start=1):
#             for j, value in enumerate(user):
#                 entry = Entry(self.scrollable_frame, width=20, fg='black')
#                 entry.grid(row=i, column=j, padx=5, pady=5)
#                 entry.insert(END, str(value))
#                 self.entries.append(entry)
#
#     def viewReviews(self):
#         global cursor
#         close_previous_results(cursor)
#         clearEntries(self.entries)
#
#         cursor.execute("SELECT * FROM Review")
#         reviews = cursor.fetchall()
#
#         column_names = [desc[0] for desc in cursor.description]
#         for j, column_name in enumerate(column_names):
#             entry = Entry(self.scrollable_frame, width=20, fg='black')
#             entry.grid(row=0, column=j, padx=5, pady=5)
#             entry.insert(END, column_name)
#             self.entries.append(entry)
#
#         for i, review in enumerate(reviews, start=1):
#             for j, value in enumerate(review):
#                 entry = Entry(self.scrollable_frame, width=20, fg='black')
#                 entry.grid(row=i, column=j, padx=5, pady=5)
#                 entry.insert(END, str(value))
#                 self.entries.append(entry)
#
#     def viewMostWatched(self):
#         global cursor
#         close_previous_results(cursor)
#         clearEntries(self.entries)
#
#         cursor.execute("SELECT * FROM MostWatchedMovies")
#         most_watched = cursor.fetchall()
#
#         column_names = [desc[0] for desc in cursor.description]
#         for j, column_name in enumerate(column_names):
#             entry = Entry(self.scrollable_frame, width=20, fg='black')
#             entry.grid(row=0, column=j, padx=5, pady=5)
#             entry.insert(END, column_name)
#             self.entries.append(entry)
#
#         for i, item in enumerate(most_watched, start=1):
#             for j, value in enumerate(item):
#                 entry = Entry(self.scrollable_frame, width=20, fg='black')
#                 entry.grid(row=i, column=j, padx=5, pady=5)
#                 entry.insert(END, str(value))
#                 self.entries.append(entry)
#
#     def viewMostReviewed(self):
#         global cursor
#         close_previous_results(cursor)
#         clearEntries(self.entries)
#
#         cursor.execute("SELECT * FROM MostReviewedMovies")
#         most_reviewed = cursor.fetchall()
#
#         column_names = [desc[0] for desc in cursor.description]
#         for j, column_name in enumerate(column_names):
#             entry = Entry(self.scrollable_frame, width=20, fg='black')
#             entry.grid(row=0, column=j, padx=5, pady=5)
#             entry.insert(END, column_name)
#             self.entries.append(entry)
#
#         for i, item in enumerate(most_reviewed, start=1):
#             for j, value in enumerate(item):
#                 entry = Entry(self.scrollable_frame, width=20, fg='black')
#                 entry.grid(row=i, column=j, padx=5, pady=5)
#                 entry.insert(END, str(value))
#                 self.entries.append(entry)
#
#     def viewWorstRated(self):
#         global cursor
#         close_previous_results(cursor)
#         clearEntries(self.entries)
#
#         cursor.execute("SELECT * FROM WorstRatedMovies")
#         worst_rated = cursor.fetchall()
#
#         column_names = [desc[0] for desc in cursor.description]
#         for j, column_name in enumerate(column_names):
#             entry = Entry(self.scrollable_frame, width=20, fg='black')
#             entry.grid(row=0, column=j, padx=5, pady=5)
#             entry.insert(END, column_name)
#             self.entries.append(entry)
#
#         for i, item in enumerate(worst_rated, start=1):
#             for j, value in enumerate(item):
#                 entry = Entry(self.scrollable_frame, width=20, fg='black')
#                 entry.grid(row=i, column=j, padx=5, pady=5)
#                 entry.insert(END, str(value))
#                 self.entries.append(entry)
#
#     def viewCast(self):
#         global cursor
#         close_previous_results(cursor)
#         clearEntries(self.entries)
#
#         movie_id_entry = Entry(self.window)
#         movie_id_entry.pack()
#         movie_id_label = Label(self.window, text="Enter Movie ID:")
#         movie_id_label.pack()
#         submit_button = Button(self.window, text="Submit", command=lambda: self.show_cast(movie_id_entry.get()))
#         submit_button.pack()
#
#     def show_cast(self, movie_id):
#         global cursor
#         close_previous_results(cursor)
#         clearEntries(self.entries)
#
#         cursor.callproc('GetCastAndCrew', (int(movie_id), 'M'))
#         for result in cursor.stored_results():
#             cast = result.fetchall()
#
#         column_names = ["Name", "Role"]
#         for j, column_name in enumerate(column_names):
#             entry = Entry(self.scrollable_frame, width=20, fg='black')
#             entry.grid(row=0, column=j, padx=5, pady=5)
#             entry.insert(END, column_name)
#             self.entries.append(entry)
#
#         for i, member in enumerate(cast, start=1):
#             for j, value in enumerate(member):
#                 entry = Entry(self.scrollable_frame, width=20, fg='black')
#                 entry.grid(row=i, column=j, padx=5, pady=5)
#                 entry.insert(END, str(value))
#                 self.entries.append(entry)
#
#     def viewCrew(self):
#         global cursor
#         close_previous_results(cursor)
#         clearEntries(self.entries)
#
#         show_id_entry = Entry(self.window)
#         show_id_entry.pack()
#         show_id_label = Label(self.window, text="Enter Show ID:")
#         show_id_label.pack()
#         submit_button = Button(self.window, text="Submit", command=lambda: self.show_crew(show_id_entry.get()))
#         submit_button.pack()
#
#     def show_crew(self, show_id):
#         global cursor
#         close_previous_results(cursor)
#         clearEntries(self.entries)
#
#         cursor.callproc('GetCastAndCrew', (int(show_id), 'S'))
#         for result in cursor.stored_results():
#             crew = result.fetchall()
#
#         column_names = ["Name", "Role"]
#         for j, column_name in enumerate(column_names):
#             entry = Entry(self.scrollable_frame, width=20, fg='black')
#             entry.grid(row=0, column=j, padx=5, pady=5)
#             entry.insert(END, column_name)
#             self.entries.append(entry)
#
#         for i, member in enumerate(crew, start=1):
#             for j, value in enumerate(member):
#                 entry = Entry(self.scrollable_frame, width=20, fg='black')
#                 entry.grid(row=i, column=j, padx=5, pady=5)
#                 entry.insert(END, str(value))
#                 self.entries.append(entry)
#
#     def addMovie(self):
#         def save_movie():
#             title = title_entry.get()
#             description = description_entry.get()
#             release_date = release_date_entry.get()
#             genre = genre_entry.get()
#             rating = float(rating_entry.get())
#             director_id = int(director_id_entry.get())
#
#             global cursor, mydb
#             cursor.execute("""INSERT INTO Movie (title, description, release_date, genre, rating, director_id)
#                               VALUES (%s, %s, %s, %s, %s, %s)""",
#                            (title, description, release_date, genre, rating, director_id))
#             mydb.commit()
#             add_movie_window.destroy()
#
#         add_movie_window = Tk()
#         add_movie_window.geometry("400x400")
#         add_movie_window.title("Add Movie")
#
#         title_label = Label(add_movie_window, text="Title")
#         title_label.pack()
#         title_entry = Entry(add_movie_window)
#         title_entry.pack()
#
#         description_label = Label(add_movie_window, text="Description")
#         description_label.pack()
#         description_entry = Entry(add_movie_window)
#         description_entry.pack()
#
#         release_date_label = Label(add_movie_window, text="Release Date (YYYY-MM-DD)")
#         release_date_label.pack()
#         release_date_entry = Entry(add_movie_window)
#         release_date_entry.pack()
#
#         genre_label = Label(add_movie_window, text="Genre")
#         genre_label.pack()
#         genre_entry = Entry(add_movie_window)
#         genre_entry.pack()
#
#         rating_label = Label(add_movie_window, text="Rating")
#         rating_label.pack()
#         rating_entry = Entry(add_movie_window)
#         rating_entry.pack()
#
#         director_id_label = Label(add_movie_window, text="Director ID")
#         director_id_label.pack()
#         director_id_entry = Entry(add_movie_window)
#         director_id_entry.pack()
#
#         save_button = Button(add_movie_window, text="Save", command=save_movie)
#         save_button.pack()
#
#     def listMovies(self):
#         global cursor
#         close_previous_results(cursor)
#         clearEntries(self.entries)
#
#         cursor.execute("SELECT * FROM Movie")
#         movies = cursor.fetchall()
#
#         column_names = [desc[0] for desc in cursor.description]
#         for j, column_name in enumerate(column_names):
#             entry = Entry(self.scrollable_frame, width=20, fg='black')
#             entry.grid(row=0, column=j, padx=5, pady=5)
#             entry.insert(END, column_name)
#             self.entries.append(entry)
#
#         for i, movie in enumerate(movies, start=1):
#             for j, value in enumerate(movie):
#                 entry = Entry(self.scrollable_frame, width=20, fg='black')
#                 entry.grid(row=i, column=j, padx=5, pady=5)
#                 entry.insert(END, str(value))
#                 self.entries.append(entry)
#
#     def addTVShow(self):
#         def save_show():
#             title = title_entry.get()
#             description = description_entry.get()
#             release_date = release_date_entry.get()
#             genre = genre_entry.get()
#             rating = float(rating_entry.get())
#             director_id = int(director_id_entry.get())
#
#             global cursor, mydb
#             cursor.execute("""INSERT INTO TV_Show (title, description, release_date, genre, rating, director_id)
#                               VALUES (%s, %s, %s, %s, %s, %s)""",
#                            (title, description, release_date, genre, rating, director_id))
#             mydb.commit()
#             add_show_window.destroy()
#
#         add_show_window = Tk()
#         add_show_window.geometry("400x400")
#         add_show_window.title("Add TV Show")
#
#         title_label = Label(add_show_window, text="Title")
#         title_label.pack()
#         title_entry = Entry(add_show_window)
#         title_entry.pack()
#
#         description_label = Label(add_show_window, text="Description")
#         description_label.pack()
#         description_entry = Entry(add_show_window)
#         description_entry.pack()
#
#         release_date_label = Label(add_show_window, text="Release Date (YYYY-MM-DD)")
#         release_date_label.pack()
#         release_date_entry = Entry(add_show_window)
#         release_date_entry.pack()
#
#         genre_label = Label(add_show_window, text="Genre")
#         genre_label.pack()
#         genre_entry = Entry(add_show_window)
#         genre_entry.pack()
#
#         rating_label = Label(add_show_window, text="Rating")
#         rating_label.pack()
#         rating_entry = Entry(add_show_window)
#         rating_entry.pack()
#
#         director_id_label = Label(add_show_window, text="Director ID")
#         director_id_label.pack()
#         director_id_entry = Entry(add_show_window)
#         director_id_entry.pack()
#
#         save_button = Button(add_show_window, text="Save", command=save_show)
#         save_button.pack()
#
#     def listTVShows(self):
#         global cursor
#         close_previous_results(cursor)
#         clearEntries(self.entries)
#
#         cursor.execute("SELECT * FROM TV_Show")
#         shows = cursor.fetchall()
#
#         column_names = [desc[0] for desc in cursor.description]
#         for j, column_name in enumerate(column_names):
#             entry = Entry(self.scrollable_frame, width=20, fg='black')
#             entry.grid(row=0, column=j, padx=5, pady=5)
#             entry.insert(END, column_name)
#             self.entries.append(entry)
#
#         for i, show in enumerate(shows, start=1):
#             for j, value in enumerate(show):
#                 entry = Entry(self.scrollable_frame, width=20, fg='black')
#                 entry.grid(row=i, column=j, padx=5, pady=5)
#                 entry.insert(END, str(value))
#                 self.entries.append(entry)
#
#     def go_home(self):
#         self.window.destroy()
#         Main_App().run()
#
#     def run(self):
#         self.window.mainloop()
#
#
# def clearEntries(entries):
#     for entry in entries:
#         entry.destroy()
#     entries.clear()
#
#
# if __name__ == "__main__":
#     main_app = Main_App()
#     main_app.run()
