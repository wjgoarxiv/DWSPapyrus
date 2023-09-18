import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib import rcParams

def rcparams():
    rcParams['figure.figsize'] = 5, 4
    rcParams['font.family'] = 'sans-serif'

    # Check whether Arial or SF Pro Display are installed in the computer
    try:
        rcParams['font.sans-serif'] = ['SF Pro Display']
    except:
        try:
            rcParams['font.sans-serif'] = ['Arial']
        except:
            print("ERROR Note that Arial and SF Pro are not installed in the computer. The program will use the default font.")
            pass

    # Label should be far away from the axes
    rcParams['axes.labelpad'] = 8
    rcParams['xtick.major.pad'] = 7
    rcParams['ytick.major.pad'] = 7

    # Add minor ticks
    rcParams['xtick.minor.visible'] = True
    rcParams['ytick.minor.visible'] = True

    # Tick width
    rcParams['xtick.major.width'] = 1
    rcParams['ytick.major.width'] = 1
    rcParams['xtick.minor.width'] = 0.5
    rcParams['ytick.minor.width'] = 0.5

    # Tick length
    rcParams['xtick.major.size'] = 5
    rcParams['ytick.major.size'] = 5
    rcParams['xtick.minor.size'] = 3
    rcParams['ytick.minor.size'] = 3

    # Tick color
    rcParams['xtick.color'] = 'black'
    rcParams['ytick.color'] = 'black'

    rcParams['font.size'] = 14
    rcParams['axes.titlepad'] = 10
    rcParams['axes.titleweight'] = 'normal'
    rcParams['axes.titlesize'] = 18

    # Axes settings
    rcParams['axes.labelweight'] = 'normal'
    rcParams['xtick.labelsize'] = 12
    rcParams['ytick.labelsize'] = 12
    rcParams['axes.labelsize'] = 16
    rcParams['xtick.direction'] = 'in'
    rcParams['ytick.direction'] = 'in'

rcparams()

class DWSPapyrusGUI:
    def __init__(self, master):
        self.master = master
        master.title("DWSPapyrus V1.0")

        self.x_var_var = tk.StringVar(value="Temperature")
        self.y_var_var = tk.StringVar(value="Pressure")
        self.x_label_var = tk.StringVar(value="Temperature (℃)")
        self.y_label_var = tk.StringVar(value="Pressure (bar)")
        self.dpi_var = tk.StringVar(value="200")
        self.transparent_var = tk.BooleanVar(value=True)
        self.time_unit_var = tk.StringVar(value="Seconds")
        self.line_width = tk.IntVar(value=2)
        self.line_or_scatter = tk.StringVar(value="Scatter")

        # Create the title label
        self.title_label = tk.Label(master, text="DWSPapyrus V1.0", font=("Arial", 24))
        self.title_label.pack()

        # Create the author label
        self.author_label = tk.Label(master, text="by @wjgoarxiv (https://github.com/wjgoarxiv)", font=("Arial", 12))
        self.author_label.pack()

        # Create the pressure sensor selection label
        self.pressure_label = tk.Label(master, text="Pressure sensor selection:")
        self.pressure_label.pack()

        # Create the pressure sensor selection dropdown menu
        self.pressure_var = tk.StringVar(master)
        self.pressure_var.set("1") # Default value
        self.pressure_dropdown = tk.OptionMenu(master, self.pressure_var, "1", "2")
        self.pressure_dropdown.pack()

        # Create the temperature sensor selection label
        self.temperature_label = tk.Label(master, text="Temperature sensor selection:")
        self.temperature_label.pack()

        # Create the temperature sensor selection dropdown menu
        self.temperature_var = tk.StringVar(master)
        self.temperature_var.set("1") # Default value
        self.temperature_dropdown = tk.OptionMenu(master, self.temperature_var, "1", "2", "3", "4")
        self.temperature_dropdown.pack()

        # Create the load button
        self.load_button = tk.Button(master, text="Load the raw CSV", command=self.load_csv) 
        self.load_button.pack()

        # Create the data preview label
        self.data_preview_label = tk.Label(master, text="Data preview:", font=("Arial", 12))
        self.data_preview_label.pack()

        # Create the data preview text box
        self.data_preview_text = tk.Text(master, height=10, width=50)
        self.data_preview_text.pack()

        # Create the treated data label
        self.treated_data_label = tk.Label(master, text="Treated data:", font=("Arial", 12))
        self.treated_data_label.pack()

        # Create the treated data text box
        self.treated_data_text = tk.Text(master, height=10, width=50)
        self.treated_data_text.pack()

        # Create the x variable selection label
        self.x_var_label = tk.Label(master, text="X variable selection:")
        self.x_var_label.pack()

        # Create the x variable selection dropdown menu
        self.x_var_dropdown = tk.OptionMenu(master, self.x_var_var, "Time", "Temperature", "Pressure")
        self.x_var_dropdown.pack()

        # Create the y variable selection label
        self.y_var_label = tk.Label(master, text="Y variable selection:")
        self.y_var_label.pack()

        # Create the y variable selection dropdown menu
        self.y_var_dropdown = tk.OptionMenu(master, self.y_var_var, "Pressure", "Temperature")
        self.y_var_dropdown.pack()

        # Create the x label selection label
        self.x_label_label = tk.Label(master, text="Write the x label:")
        self.x_label_label.pack()

        # Create the x label selection menu
        self.x_label_dropdown = tk.Entry(master, textvariable=self.x_label_var)
        self.x_label_dropdown.pack()

        # Create the y label selection label
        self.y_label_label = tk.Label(master, text="Write the y label:")
        self.y_label_label.pack()

        # Create the y label selection text box
        self.y_label_dropdown = tk.Entry(master, textvariable=self.y_label_var)
        self.y_label_dropdown.pack()

        # Create the DPI selection label
        self.dpi_label = tk.Label(master, text="DPI selection:")
        self.dpi_label.pack()

        # Create the DPI selection text box
        self.dpi_entry = tk.Entry(master, textvariable=self.dpi_var)
        self.dpi_entry.pack()

        # Create the transparency selection box
        self.transparent_label = tk.Label(master, text="Transparent background:")
        self.transparent_label.pack()

        # Create the transparency selection check box
        self.transparent_check = tk.Checkbutton(master, variable=self.transparent_var)
        self.transparent_check.pack()

        # Create the line width selection label
        self.line_width_label = tk.Label(master, text="Line width (Markersize) selection:")
        self.line_width_label.pack()

        # Create the line width selection text box
        self.line_width_entry = tk.Entry(master, textvariable=self.line_width)
        self.line_width_entry.pack()

        # Create the time unit selection label
        self.time_unit_label = tk.Label(master, text="Time unit selection:")
        self.time_unit_label.pack()

        # Create the time unit selection dropdown menu
        self.time_unit_dropdown = tk.OptionMenu(master, self.time_unit_var, "Seconds", "Minutes")
        self.time_unit_dropdown.pack()

        # Create the line or scatter selection label
        self.line_or_scatter_label = tk.Label(master, text="Line or scatter selection:")
        self.line_or_scatter_label.pack()

        # Create the line or scatter selection dropdown menu
        self.line_or_scatter_dropdown = tk.OptionMenu(master, self.line_or_scatter, "Line", "Scatter")
        self.line_or_scatter_dropdown.pack()

        # Create the plot button
        self.plot_button = tk.Button(master, text="Plot data", command=self.plot_data)
        self.plot_button.pack()

        # Create the exit button
        self.exit_button = tk.Button(master, text="Exit", command=master.quit)
        self.exit_button.pack()

        self.time_sec = None
        self.time_min = None
        self.df = None
        self.temperature_sensor_num = None

    def load_csv(self):
        # Open a file dialog to select the CSV file
        file_path = filedialog.askopenfilename()

        try:
            # Load the CSV file
            df = pd.read_csv(file_path, encoding="cp949", header=1)

            # Get the selected pressure and temperature sensor numbers
            self.pressure_sensor_num = int(self.pressure_var.get())
            self.temperature_sensor_num = int(self.temperature_var.get())

            # Get the pressure, temperature, and time data
            pressure = df.iloc[1:, self.pressure_sensor_num + 1].astype(float)
            raw_temp = df.iloc[1:, self.temperature_sensor_num + 3].astype(float)
            temp = raw_temp / 10 # Convert raw temperature to real temperature
            
            # Make time_sec universal
            self.time_sec = df.iloc[1:, 1].astype(float)
            self.time_min = self.time_sec / 60 # Convert time from second to minute

            # Update the data preview text box
            self.data_preview_text.delete('1.0', tk.END)
            self.data_preview_text.insert(tk.END, "Pressure data:\n")
            self.data_preview_text.insert(tk.END, str(pressure.head()) + "\n\n")
            self.data_preview_text.insert(tk.END, "Temperature data:\n")
            self.data_preview_text.insert(tk.END, str(temp.head()))

            pressure_mean = pressure.mean()
            pressure_std = pressure.std()
            temp_mean = temp.mean()
            temp_std = temp.std()

            self.treated_data_text.delete('1.0', tk.END)
            self.treated_data_text.insert(tk.END, "Treated data:\n")
            self.treated_data_text.insert(tk.END, f"Pressure mean: {pressure_mean:.2f}\n")
            self.treated_data_text.insert(tk.END, f"Pressure std: {pressure_std:.2f}\n")
            self.treated_data_text.insert(tk.END, f"Temperature mean: {temp_mean:.2f}\n")
            self.treated_data_text.insert(tk.END, f"Temperature std: {temp_std:.2f}\n")

            # Show a success message
            self.show_message("CSV file loaded successfully.", "blue")

            self.df = df

        except Exception as e:
            # Show an error message
            self.show_message(str(e), "red")

    def show_message(self, message, color):
        # Create a message label
        message_label = tk.Label(self.master, text=message, fg=color)
        message_label.pack()

        # Remove the message after 3 seconds
        self.master.after(3000, message_label.destroy)

    def plot_data(self):
        x_var = self.x_var_var.get()
        y_var = self.y_var_var.get()
        x_label = self.x_label_var.get()
        y_label = self.y_label_var.get()
        dpi = int(self.dpi_var.get())
        transparent = self.transparent_var.get()
        time_unit = self.time_unit_var.get()

        fig, ax = plt.subplots()

        rcparams()

        data_x, data_y = None, None
        if x_var == "Time":
            data_x = self.time_sec if time_unit == "Seconds" else self.time_min
        elif x_var == "Temperature":
            data_x = self.df.iloc[1:, self.temperature_sensor_num + 3] / 10
        elif x_var == "Pressure":
            data_x = self.df.iloc[1:, self.pressure_sensor_num + 1]

        if y_var == "Pressure":
            data_y = self.df.iloc[1:, self.pressure_sensor_num + 1]
        elif y_var == "Temperature":
            data_y = self.df.iloc[1:, self.temperature_sensor_num + 3] / 10 

        if data_x is None or data_y is None:
            self.show_message("Error: Missing Data", "red")
            return

        if self.line_or_scatter.get() == "Line":
            ax.plot(data_x, data_y, color="black", linewidth=self.line_width.get())
        elif self.line_or_scatter.get() == "Scatter":
            ax.scatter(data_x, data_y, color="black", s=self.line_width.get()*2)

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        # Tightly fit the plot
        fig.tight_layout()

        fig.set_dpi(dpi)
        fig.savefig("PLOT.png", dpi=dpi, transparent=transparent, bbox_inches='tight')
        plt.show()
        self.show_message("Plot saved successfully.", "blue")

root = tk.Tk()
gui = DWSPapyrusGUI(root)
root.mainloop()