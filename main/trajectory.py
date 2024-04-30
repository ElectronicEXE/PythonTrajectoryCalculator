import numpy as np
import matplotlib.pyplot as plt
import time
import tkinter as tk
from tkinter import ttk

# Global variables to store entry widgets
entry_height = None
entry_angle = None
entry_velocity = None
entry_gravity = None
entry_density = None
entry_drag_coefficient = None
entry_mass = None
entry_time_step = None
entry_radius = None

def plot_setup():
    plt.figure(facecolor='black')
    plt.xlabel('Horizontal Distance (m)', color='white')
    plt.ylabel('Vertical Distance (m)', color='white')
    plt.title('Projectile Trajectory with Air Resistance', color='white')
    plt.grid(True, color='gray')
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.gca().set_facecolor('black')  # Set background color of plot area
    plt.gca().spines['bottom'].set_color('white')  # Set color of x-axis spine
    plt.gca().spines['left'].set_color('white')  # Set color of y-axis spine
    plt.gca().xaxis.label.set_color('white')  # Set color of x-axis label
    plt.gca().yaxis.label.set_color('white')  # Set color of y-axis label
    plt.gca().tick_params(axis='x', colors='white')  # Set color of x-axis ticks
    plt.gca().tick_params(axis='y', colors='white')  # Set color of y-axis ticks
    plt.ion()  # Enable interactive mode
    plt.show()  # Show the plot without blocking the code execution
    plt.get_current_fig_manager().window.wm_state('zoomed')  # Maximize the window
    time.sleep(0.1)  # Introduce a 2-second delay before plotting starts

def calculate_trajectory_with_air_resistance(h, alpha_deg, v0, g, rho, A, Cd, m, dt=0.01, pause=True):
    alpha_rad = np.deg2rad(alpha_deg)
    cos_alpha = np.cos(alpha_rad)
    sin_alpha = np.sin(alpha_rad)
    tan_alpha = np.tan(alpha_rad)

    x_values = [0]
    y_values = [h]
    if alpha_deg == 90:  # Special case for vertical launch
        vx = 0
        vy = v0
    else:
        vx = v0 * cos_alpha
        vy = v0 * sin_alpha

    plot_setup()  # Call plot setup function

    while y_values[-1] >= 0:
        v = np.sqrt(vx ** 2 + vy ** 2)
        F_drag_x = -0.5 * rho * A * Cd * v * vx
        F_drag_y = -0.5 * rho * A * Cd * v * vy
        ax = F_drag_x / m
        ay = -g + F_drag_y / m

        vx += ax * dt
        vy += ay * dt

        x_values.append(x_values[-1] + vx * dt)
        y_values.append(y_values[-1] + vy * dt)

        plt.plot(x_values, y_values, color='cyan', linewidth=2)  # Update plot with new trajectory
        if pause:
            plt.pause(0.001)  # Pause to allow the plot to update

    plt.ioff()  # Disable interactive mode
    plt.show()  # Show the final plot

def run_simulation(var_pause):
    h = float(entry_height.get())
    alpha = float(entry_angle.get())
    v0 = float(entry_velocity.get())
    g = float(entry_gravity.get())
    rho = float(entry_density.get())
    Cd = float(entry_drag_coefficient.get())
    m = float(entry_mass.get())
    dt = float(entry_time_step.get())
    r = float(entry_radius.get())
    A = r
    pause_enabled = var_pause.get()

    calculate_trajectory_with_air_resistance(h, alpha, v0, g, rho, A, Cd, m, dt, pause_enabled)


def main():
    global entry_height, entry_angle, entry_velocity, entry_gravity, entry_density, entry_drag_coefficient, entry_mass, entry_time_step, entry_radius

    root = tk.Tk()
    root.title("Projectile Trajectory Parameters")

    # Dark mode theme colors
    bg_color = "#2b2b2b"  # Background color
    fg_color = "#dcdcdc"  # Foreground color (text color)
    entry_bg_color = "#3a3a3a"  # Entry background color
    entry_fg_color = "black"  # Entry foreground color (text color)

    root.configure(bg=bg_color)

    # Labels and entry fields for input parameters
    parameters = [
        ("Height (m):", "0.03"),
        ("Launch Angle (degrees):", "45"),
        ("Initial Velocity (m/s):", "6"),
        ("Gravity (m/s^2):", "9.81"),
        ("Air Density (kg/m^3):", "1.225"),
        ("Drag Coefficient:", "0.47"),
        ("Mass (kg):", "0.0027"),
        ("Time Step (s):", "0.01"),
        ("Surface Area (m^2):", "0.00502654834")
    ]

    for row, (param, default) in enumerate(parameters):
        label = ttk.Label(root, text=param, background=bg_color, foreground='white')
        label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        entry = ttk.Entry(root, background=bg_color, foreground='black')
        entry.insert(0, default)
        entry.grid(row=row, column=1, padx=5, pady=5)
        if "Height" in param:
            entry_height = entry
        elif "Launch Angle" in param:
            entry_angle = entry
        elif "Initial Velocity" in param:
            entry_velocity = entry
        elif "Gravity" in param:
            entry_gravity = entry
        elif "Air Density" in param:
            entry_density = entry
        elif "Drag Coefficient" in param:
            entry_drag_coefficient = entry
        elif "Mass" in param:
            entry_mass = entry
        elif "Time Step" in param:
            entry_time_step = entry
        elif "Surface Area" in param:  # Check for the correct spelling and inclusion of the radius parameter
            entry_radius = entry  # Ensure entry_radius is properly assigned


    var_pause = tk.BooleanVar()
    chk_pause = ttk.Checkbutton(root, text="Animate", variable=var_pause, style='Dark.TCheckbutton')
    chk_pause.grid(row=len(parameters), columnspan=2, pady=5)

    btn_run = ttk.Button(root, text="Run Simulation", command=lambda: run_simulation(var_pause), style='Dark.TButton')
    btn_run.grid(row=len(parameters) + 1, columnspan=2, pady=5)

    # Style for dark buttons and checkbutton
    s = ttk.Style()
    s.configure('Dark.TButton', foreground='black', background='black')
    s.configure('Dark.TCheckbutton', background=bg_color, foreground='white')

    root.mainloop()

if __name__ == "__main__":
    main()
