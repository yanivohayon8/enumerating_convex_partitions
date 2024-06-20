import tkinter as tk
from src.data_structures import Point


def create_click_tracker(canvas_width=4000, canvas_height=4000):
    """
    Creates a white canvas of specified width and height.
    Users can click on the canvas to place red circles and store coordinates.
    The function returns the list of coordinates when the user quits the application.

    Parameters:
    canvas_width (int): Width of the canvas
    canvas_height (int): Height of the canvas

    Returns:
    list: List of tuples containing the coordinates of clicks
    """
    def on_canvas_click(event):
        # Draw a red circle at the click location
        x, y = event.x, event.y
        radius = 5
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill='red')
        # Store the coordinates
        click_coordinates.append((x, y))

    def on_quit():
        # Close the application
        root.quit()

    # Create the main window
    root = tk.Tk()
    root.title("Click Tracker")

    # Create a canvas widget
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
    canvas.pack()

    # List to store click coordinates
    click_coordinates = []

    # Bind the click event to the canvas
    canvas.bind("<Button-1>", on_canvas_click)

    # Add a button to quit the application
    quit_button = tk.Button(root, text="Quit", command=on_quit)
    quit_button.pack()

    # Run the Tkinter event loop
    root.mainloop()

    return [Point(coord[0],coord[1]) for coord in click_coordinates]

