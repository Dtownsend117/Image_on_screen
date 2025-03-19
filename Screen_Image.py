import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os

class Avatar:
    def __init__(self, gif_path):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.geometry("300x300")  # Change size to fit your image
        self.root.attributes("-topmost", True)  # This will keep the image as the top window on the screen
      
        self.load_last_position() # This loads the image to its last position on the screen

        self.image = Image.open(gif_path)
        self.frames = []
        
        try:
            for i in range(self.image.n_frames):
                self.image.seek(i)
                frame = self.create_circular_image(self.image.copy())
                self.frames.append(ImageTk.PhotoImage(frame))
        except EOFError:
            pass

        self.current_frame = 0

        self.label = tk.Label(self.root, image=self.frames[self.current_frame])
        self.label.pack()

        # This is if you want a button on the image to manually close it
        self.close_button = tk.Button(self.root, text="X", command=self.fade_out, bg='blue', fg='black', font=('Arial', 10, 'bold'))
        self.close_button.place(x=270, y=5)  # Set the position of the button on screen

        self.label.bind("<ButtonPress-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.do_drag)

        self.update_gif()
        self.fade_in()
        self.root.mainloop()

    def update_gif(self):
        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.label.configure(image=self.frames[self.current_frame])

        duration = self.image.info.get('duration', 100) 
        self.root.after(duration, self.update_gif) 

    def fade_in(self, alpha=0): # Sets the image to fade on screen
        if alpha < 255:
            self.root.attributes("-alpha", alpha / 255)
            self.root.after(10, self.fade_in, alpha + 5) 

    def fade_out(self, alpha=255): # Sets the image to fade off screen
        if alpha > 0:
            self.root.attributes("-alpha", alpha / 255)
            self.root.after(10, self.fade_out, alpha - 5) 
        else:
            self.save_last_position()  
            self.root.destroy()  

    def start_drag(self, event):
        self.last_x = event.x
        self.last_y = event.y
        self.start_x = self.root.winfo_x()
        self.start_y = self.root.winfo_y()

    def do_drag(self, event):
        x = self.start_x + (event.x - self.last_x)
        y = self.start_y + (event.y - self.last_y)
        self.root.geometry(f"+{x}+{y}")

    def load_last_position(self):
        """Load the last position from a file."""
        if os.path.exists("last_position.txt"):
            with open("last_position.txt", "r") as f:
                position = f.read().strip().split(',')
                if len(position) == 2:
                    x, y = map(int, position)
                    self.root.geometry(f"+{x}+{y}")

    def save_last_position(self):
        """Save the current position to a file."""
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        with open("last_position.txt", "w") as f:
            f.write(f"{x},{y}")

if __name__ == "__main__":
    gif_path = ""  # Use the file path to your image
    viewer = Avatar(gif_path)
