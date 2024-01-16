from tkinter import *
import tkinter as tk
from io import BytesIO
from PIL import Image, ImageTk
import requests
import subprocess

class PopflixSearchApp:
    def __init__(self, root):
        self.root = root
        self.current_index = 0 

        # Constants
        self.API_KEY = "d22bf11794a739fb956a2cf784f49fd3"
        self.MOVIEDB_URL = "https://api.themoviedb.org/3/search/movie"
        self.FONT = ("Roboto", 11, "bold")
        self.WHITE = "white"
        self.BLACK = "black"

        # Widgets creation and placement
        self.widgets()

    def widgets(self):
        # Create and place various widgets on the window.
        self.search_background()
        self.profile_button()
        self.entry_and_search_button()
        self.movie_info_labels()
        self.image_label()
        self.navigation_buttons()

    def search_background(self):
        # Load and display the search background image.
        search_image = Image.open("Asset/search.png").resize((989, 605))
        self.search_image = ImageTk.PhotoImage(search_image)
        bg_image_search = tk.Label(self.root, image=self.search_image)
        bg_image_search.place(x=-2, y=-2)

    def profile_button(self):
        # Load and display the profile button image.
        profile_1_small_image = Image.open("Asset/profile_1_small.png")
        self.profile_1_small = ImageTk.PhotoImage(profile_1_small_image)
        profile_1_small_button = Button(self.root, image=self.profile_1_small, border=0,
                                        activebackground=self.BLACK, foreground=self.BLACK,
                                        bg=self.BLACK, command=self.open_new_window)
        profile_1_small_button.place(relx=.93, rely=0.044)

    def entry_and_search_button(self):
        # Create entry widget for movie search and the associated search button.
        self.entry = tk.Entry(self.root, bd=0, bg="#000000", fg=self.WHITE, font=("Roboto", 10), highlightthickness=0)
        self.entry.place(x=690.0, y=33.0, width=182.0, height=24.0)

        search_image_button = Image.open("Asset/search_button.png")
        self.search_button_image = ImageTk.PhotoImage(search_image_button)
        self.search_button = tk.Button(self.root, image=self.search_button_image, border=0,
                                      activebackground=self.BLACK, foreground=self.BLACK, bg=self.BLACK,
                                      command=lambda: self.display_movie(self.search_movies(self.entry.get()), 0))
        self.search_button.place(relx=.66, rely=0.057)

    def movie_info_labels(self):
        # Create labels for movie information.
        self.title_label = tk.Label(self.root, text="Movie Title", wraplength=600, bg="#0E0E0E",
                                    fg=self.WHITE, font=("Roboto", 33, "bold"), justify="left")
        self.title_label.place(relx=0.08, rely=0.32)

        self.id_label = tk.Label(self.root, text="ID: 000000", bg="#E50815", fg=self.WHITE,
                                 font=("Roboto", 10, "bold"))
        self.id_label.place(relx=0.09, rely=0.243)

        self.overview_label = tk.Label(self.root, text="Movie Description", wraplength=515, bg="#0B0B0B",
                                       fg=self.WHITE, justify="left", font=("Roboto", 10))
        self.overview_label.place(relx=0.08, rely=0.46)

        self.language_label = tk.Label(self.root, text="n/a", bg=self.BLACK, fg=self.WHITE, font=self.FONT)
        self.language_label.place(relx=0.177, rely=0.745)

        self.rating_label = tk.Label(self.root, text="Rating: 0", bg=self.BLACK, fg=self.WHITE, font=self.FONT)
        self.rating_label.place(relx=0.11, rely=0.827)

    def image_label(self):
        # Create label for displaying movie poster.
        empty_poster = Image.open("Asset/no_poster.png")
        self.empty_poster_image = ImageTk.PhotoImage(empty_poster)
        self.image_label = tk.Label(self.root, image=self.empty_poster_image, bg="#0E0E0E", fg=self.WHITE)
        self.image_label.place(relx=0.68, rely=0.26)

    def navigation_buttons(self):
        # Create previous, next buttons, and label for current page.
        previous_image = Image.open("Asset/left_button.png")
        self.previous_button_image = ImageTk.PhotoImage(previous_image)
        self.previous_button = tk.Button(self.root, image=self.previous_button_image, border=0,
                                         activebackground=self.BLACK, foreground=self.BLACK,
                                         command=lambda: self.navigate_movies(-1))
        self.previous_button.place(relx=.85, rely=.89)

        self.page_label = tk.Label(self.root, text="0", bg=self.BLACK, fg=self.WHITE, font=("Roboto", 14))
        self.page_label.place(relx=.897, rely=.89)

        next_image = Image.open("Asset/right_button.png")
        self.next_button_image = ImageTk.PhotoImage(next_image)
        self.next_button = tk.Button(self.root, image=self.next_button_image, border=0,
                                     activebackground=self.BLACK, foreground=self.BLACK,
                                     command=lambda: self.navigate_movies(1))
        self.next_button.place(relx=.93, rely=.89)

    def open_new_window(self):
        #Open a new frame for profile.
        self.root.destroy()
        subprocess.run(["python", "profile_window.py"])

    def search_movies(self, query):
        #Search movies based on the given query.
        param = {'api_key': self.API_KEY, 'query': query}
        response = requests.get(self.MOVIEDB_URL, params=param)
        data = response.json()
        return data.get('results', [])

    def display_movie(self, movies, index):
        #Display movie details.
        if movies and 0 <= index < len(movies):
            movie = movies[index]
            self.title_label.config(text=movie.get('title', 'N/A'))
            self.overview_label.config(text=movie.get('overview', 'N/A'))
            self.rating_label.config(text=f"Rating: {movie.get('vote_average', 'N/A')}")
            self.language_label.config(text=f"{movie.get('original_language', 'N/A')}")
            self.id_label.config(text=f"ID: {movie.get('id', 'N/A')}")

            poster_path = movie.get('poster_path')
            if poster_path:
                image_url = f"https://image.tmdb.org/t/p/w185{poster_path}"
                image = self.get_image_from_url(image_url)
                self.image_label.config(image=image)
                self.image_label.photo = image

            self.update_page_label(index + 1)
        else:
            self.clear_labels()

    def navigate_movies(self, offset):
        #Navigate to the previous or next movie.
        movies = self.search_movies(self.entry.get())
        if movies:
            self.current_index = (self.current_index + offset) % len(movies)
            self.display_movie(movies, self.current_index)

    def clear_labels(self):
        #Clear labels and reset the image.
        labels_to_clear = [self.title_label, self.overview_label, 
                           self.rating_label, self.language_label, 
                           self.id_label]
        for label in labels_to_clear:
            label.config(text="")

        self.image_label.config(image="")
        self.update_page_label(0)

    def update_page_label(self, current):
        #Update the page label.
        self.page_label.config(text=f"{current}")

    def get_image_from_url(self, url):
        #Load an image from the given URL.
        try:
            response = requests.get(url)
            image_data = BytesIO(response.content)
            img = Image.open(image_data)
            photo = ImageTk.PhotoImage(img)
            return photo
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

# Create the main window
root = Tk()
root.title("Popflix - Search Window")
root.geometry("989x605")
root.configure(bg='black')
root.resizable(0, 0)

# Initialize the PopflixSearchApp class
app = PopflixSearchApp(root)

# Run the application
root.mainloop()
