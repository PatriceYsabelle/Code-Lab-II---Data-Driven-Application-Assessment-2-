import tkinter as tk
from PIL import Image, ImageTk
import requests
import io
import os
import subprocess

class PopflixViewApp:
    def __init__(self, root):
        # MovieDB API key and base URL
        self.API_KEY = "d22bf11794a739fb956a2cf784f49fd3"
        self.MOVIEDB_URL = "https://api.themoviedb.org/3/discover/movie"
        self.image_cache_folder = "image_cache"

        self.root = root
        self.root.title("Popflix - View Window")
        self.root.geometry("989x605")
        self.root.resizable(0, 0)

        # Setup background, profile button, genre buttons, and movie frame
        self.setup_background()
        self.setup_profile_button()
        self.genres = self.get_genres()
        self.setup_genre_buttons()
        self.setup_movie_frame()

    def setup_background(self):
        # Load and display the background image
        bg_image = Image.open("Asset/view.png").resize((989, 605))
        self.bg_image_tk = ImageTk.PhotoImage(bg_image)
        self.bg_image_view = tk.Label(self.root, image=self.bg_image_tk)
        self.bg_image_view.place(x=-2, y=-2)

    def setup_profile_button(self):
        # Load and display the profile image button
        profile_2_small = Image.open("Asset/profile_2_small.png").resize((50, 50))
        self.profile_2_small_tk = ImageTk.PhotoImage(profile_2_small)
        self.profile_2_small_button = tk.Button(self.root, image=self.profile_2_small_tk, border=0,
                                                activebackground="#5825FE", foreground="black",
                                                bg="black", command=self.open_new_window)
        self.profile_2_small_button.place(relx=.93, rely=0.04)

    def setup_genre_buttons(self):
        # Get the list of movie genres and create genre buttons
        genre_buttons = []
        for i, genre in enumerate(self.genres[:5]):
            genre_button = tk.Button(self.root, text=genre, command=lambda g=genre: self.genre_button_clicked(self.get_genre_id(g)),
                                     bg="#111111", fg="white", relief="flat", activebackground="#111111",
                                     activeforeground="red", bd=0)
            genre_button.place(relx=0.1 + i * 0.2, rely=0.17, width=140, height=30, anchor="center")
            genre_buttons.append(genre_button)
        self.genre_buttons = genre_buttons

    def setup_movie_frame(self):
        # Create a frame for displaying movie posters
        self.movie_frame = tk.Frame(self.root, bg="black")
        self.movie_frame.place(relx=.12, rely=.23)

    def open_new_window(self):
        # Function to open a new window (profile window)
        self.root.destroy()
        subprocess.run(["python", "profile_window.py"])

    def get_genres(self):
        # Function to get a list of movie genres from MovieDB API
        response = requests.get("https://api.themoviedb.org/3/genre/movie/list", 
                                params={"api_key": self.API_KEY})
        genres = response.json().get("genres", [])
        return [genre["name"] for genre in genres]

    def get_genre_id(self, genre_name):
        # Function to get the genre ID for a given genre name
        response = requests.get("https://api.themoviedb.org/3/genre/movie/list", 
                                params={"api_key": self.API_KEY})
        genres = response.json().get("genres", [])
        for genre in genres:
            if genre["name"] == genre_name:
                return genre["id"]
        return None

    def download_image(self, url):
        # Function to download and return an image from a URL
        response = requests.get(url, stream=True)
        return Image.open(io.BytesIO(response.content)) if response.status_code == 200 else None

    def get_cached_image_path(self, image_url):
        # Function to get the cached image path for a given URL
        filename = os.path.join(self.image_cache_folder, image_url.replace("/", "_").replace(":", "_"))
        return filename

    def get_image(self, url):
        # Function to get an image, either from cache or download, to help the image load faster
        cached_image_path = self.get_cached_image_path(url)

        if not os.path.exists(cached_image_path):
            image = self.download_image(url)
            if image:
                os.makedirs(self.image_cache_folder, exist_ok=True)
                image.save(cached_image_path)

        return Image.open(cached_image_path)

    def update_movies(self, genre_id):
        # Function to update the movies based on selected genre & grid placement
        params = {"api_key": self.API_KEY, "with_genres": genre_id, "include_adult": False}
        response = requests.get(self.MOVIEDB_URL, params=params)
        movies = response.json().get("results", [])

        for widget in self.movie_frame.winfo_children():
            widget.destroy()

        row, col = 0, 0
        for movie in movies[:10]:
            poster_url = f"https://image.tmdb.org/t/p/w342/{movie.get('poster_path', '')}"
            img = self.get_image(poster_url)

            if img:
                img = img.resize((135, 210), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(img)
                poster = tk.Label(self.movie_frame, image=photo, bg="black")
                poster.grid(row=row, column=col, padx=5, pady=5)
                col += 1
                if col > 4:
                    col = 0
                    row += 1
                poster.image = photo

    def genre_button_clicked(self, genre_id):
        # Function to handle genre button click event
        self.update_movies(genre_id)

# Create the main window
root = tk.Tk()
app = PopflixViewApp(root)
root.mainloop()
