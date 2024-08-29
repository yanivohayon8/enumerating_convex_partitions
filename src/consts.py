import numpy as np

PLOT_COLORS = ['b', 'g', 'r', 'black','c', 'y',   'brown','orange', 'purple','lime', 'pink', 'gold', 'teal', 'indigo', 'lavender', 'coral', 'olive', 'maroon'] # ["blue","green","red","black","yellow","magenta","cyan"] 'k', 'w',

# shades_of_blue = [
#      (0/255, 0/255, 255/255),        # Pure blue
#     (0/255, 51/255, 255/255),       # Dodger blue
#     (0/255, 102/255, 204/255),      # Medium blue
#     (0/255, 153/255, 204/255),      # Steel blue
#     (0/255, 204/255, 255/255),      # Deep sky blue
#     (51/255, 153/255, 255/255),     # Light sky blue
#     (102/255, 178/255, 255/255),    # Light steel blue
#     (153/255, 204/255, 255/255)     # Alice blue
# ]

# PLOT_COLORS = shades_of_blue

def generate_blue_shades(num_shades):
    blue_values = np.linspace(0, 255, num_shades).astype(int)
    shades_of_blue = [(0, 0, blue_value/255) for blue_value in blue_values]

    return shades_of_blue