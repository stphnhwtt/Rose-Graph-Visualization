import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Initialize parameters
value_range = (1, 8)  # Range from 1 to 8
transition_frames = 100  # Number of frames for smooth transition

# Create figure and axis with a sepia-toned background
plt.style.use('seaborn-v0_8-paper')
fig = plt.figure(figsize=(10, 10), facecolor='#FDF5E6')
ax = fig.add_subplot(111, projection='polar', facecolor='#FDF5E6')

# Customize grid and spokes
ax.set_ylim(0, 1)
ax.grid(True, color='#8B7355', alpha=0.3, linestyle='-', linewidth=0.5)
ax.set_rticks([0, 0.25, 0.5, 0.75, 1])
ax.set_rlabel_position(90)

# Customize spoke labels and tick colors
ax.tick_params(colors='#8B4513', grid_color='#8B7355', grid_alpha=0.3)
plt.setp(ax.spines.values(), color='#8B4513', alpha=0.5)

# Function to generate rose curve
def rose_curve(m, n):
    theta = np.linspace(0, 2 * np.pi, 1000)
    r = np.cos((n / m) * theta)
    return theta, r

# Function to get new random values
def get_new_values():
    m = random.randint(1, 8)
    n = random.randint(1, 8)
    while n == m:  # Ensure m and n are different to avoid diagonal cases
        n = random.randint(1, 8)
    return m, n

# Initialize starting and target values
current_m, current_n = get_new_values()
target_m, target_n = get_new_values()
transition_progress = 0

# Initialize plot
theta, r = rose_curve(current_m, current_n)
line, = ax.plot(theta, r, color='#8B4513', linewidth=2.5)

# Add titles
fig.suptitle('Rose Curves', fontsize=16, color='#8B4513', y=0.95, 
             fontname='serif', fontweight='bold')
ax.text(0, 1.4, 'A Study of Mathematical Harmonics', 
        horizontalalignment='center', color='#8B4513', 
        fontsize=10, fontname='serif', transform=ax.transAxes)

def update(frame):
    global current_m, current_n, target_m, target_n, transition_progress
    
    # Update transition progress
    transition_progress += 1/transition_frames
    
    if transition_progress >= 1:
        # Transition complete, update current values and get new targets
        current_m, current_n = target_m, target_n
        target_m, target_n = get_new_values()
        transition_progress = 0
    
    # Smooth easing function
    t = transition_progress
    ease = t * t * (3 - 2 * t)  # Smooth step interpolation
    
    # Interpolate between current and target values
    m = current_m + (target_m - current_m) * ease
    n = current_n + (target_n - current_n) * ease
    
    # Update the plot
    theta, r = rose_curve(m, n)
    line.set_data(theta, r)
    
    # Update equation
    ax.set_title(f"$r = \\cos(\\frac{{{n:.2f}}}{{{m:.2f}}} \\theta)$", 
                 pad=20, color='#8B4513', fontsize=14, fontname='serif')
    
    return line,

# Create animation
ani = animation.FuncAnimation(fig, update, interval=30, blit=True)

plt.show() 