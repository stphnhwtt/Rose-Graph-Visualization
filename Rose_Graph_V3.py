import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from math import gcd
from functools import reduce

# Create figure and axis with a sepia-toned background
plt.style.use('seaborn-v0_8-paper')
fig = plt.figure(figsize=(10, 10), facecolor='#FDF5E6')
ax = plt.axes([0.1, 0.1, 0.8, 0.8], facecolor='#FDF5E6')

# Customize grid and spokes
ax.set_xlim(-1.01, 1.01)
ax.set_ylim(-1.01, 1.01)
ax.grid(False)  # Remove grid
ax.axhline(y=0, color='#8B7355', alpha=0.3, linestyle='-', linewidth=0.5)  # Add x-axis line
ax.axvline(x=0, color='#8B7355', alpha=0.3, linestyle='-', linewidth=0.5)  # Add y-axis line
ax.set_aspect('equal')

# Hide all spines, ticks, and labels
ax.set_xticks([])  # Remove x-axis ticks
ax.set_yticks([])  # Remove y-axis ticks
for spine in ax.spines.values():
    spine.set_visible(False)  # Hide the bounding box

# Customize tick colors
ax.tick_params(colors='#8B4513', grid_color='#8B7355', grid_alpha=0.3)
plt.setp(ax.spines.values(), color='#8B4513', alpha=0.5)

# Function to generate rose curve in Cartesian coordinates
def lcm(a, b):
    a, b = int(round(a)), int(round(b))  # Convert to integers
    return abs(a * b) // gcd(a, b)

def rose_curve(m, n):
    # Convert to integers for LCM calculation
    m_int, n_int = int(round(m)), int(round(n))
    cycles = lcm(n_int, m_int)
    theta = np.linspace(0, 2 * np.pi * cycles, 4000)  # Increased to 4000 points
    r = np.cos((n/m) * theta)  # Use original float values for the curve
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

# Function to get next values in sequence
def get_next_values(current_m, current_n):
    next_m = current_m
    next_n = current_n
    
    # Determine if we're moving up or down based on current m
    ascending = (current_m % 2 == 1)  # Odd m means ascending
    
    if ascending:
        next_n = current_n + 1  # Moving up
        if next_n > 8:
            next_m = current_m + 1
            next_n = 8  # Start at top for descending
    else:
        next_n = current_n - 1  # Moving down
        if next_n < 1:
            next_m = current_m + 1
            next_n = 1  # Start at bottom for ascending
    
    # If we've reached the end of all values, start over
    if next_m > 8:
        next_m = 1
        next_n = 1
            
    return next_m, next_n

# Initialize values
transition_frames = 180  # Reduced from 200 (10% faster transitions)
current_m = 1
current_n = 1
target_m, target_n = get_next_values(current_m, current_n)
transition_progress = 0
pause_frames = 30  # Add pause frames at each complete curve

# Initialize plot
x, y = rose_curve(current_m, current_n)
line, = ax.plot(x, y, color='#8B4513', linewidth=2.5)

# Add titles
fig.suptitle('Rose Curves', fontsize=16, color='#8B4513', y=0.95, 
             fontname='serif', fontweight='bold')

def update(frame):
    global current_m, current_n, target_m, target_n, transition_progress
    
    # Update transition progress
    transition_progress += 1/transition_frames
    
    if transition_progress >= 1:
        # Add pause when reaching a complete curve
        if transition_progress < 1 + (pause_frames/transition_frames):
            transition_progress += 1/transition_frames
            return line,
            
        # After pause, move to next curve
        current_m, current_n = target_m, target_n
        target_m, target_n = get_next_values(current_m, current_n)
        transition_progress = 0
    
    # Smooth easing function
    t = transition_progress
    ease = t * t * t * (10 - 15 * t + 6 * t * t) # Quintic easing
    
    # Interpolate between current and target values
    m = current_m + (target_m - current_m) * ease
    n = current_n + (target_n - current_n) * ease
    
    # Update the plot
    x, y = rose_curve(m, n)
    line.set_data(x, y)
    
    # Clear previous equation and update with new one
    ax.set_title("")  # Clear the old title
    ax.set_title(f"$r = \\cos(\\frac{{{n:.2f}}}{{{m:.2f}}}\\theta)$", 
                 pad=20, color='#8B4513', fontsize=10,
                 fontname='serif', 
                 loc='right',
                 y=-0.1)
    
    return line,

# Create animation
ani = animation.FuncAnimation(fig, update, frames=None, 
                            interval=45,
                            blit=False,  # Changed from True to False
                            save_count=500)

plt.show() 