from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QTextEdit, QCheckBox, QLineEdit, QFileDialog, QWidget, QMessageBox, QDialog, QFrame
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
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

# Create the main window class
class DWSPapyrusGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("DWSPapyrus")
        
        # Initialize UI components
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()

        # Dividing section with line 
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        # Title 
        layout.addWidget(QLabel("DWSPapyrus", font=QtGui.QFont("Arial", 20, QtGui.QFont.Bold), alignment=Qt.AlignCenter))

        # Version 
        layout.addWidget(QLabel("Version 1.2", font=QtGui.QFont("Arial", 12, QtGui.QFont.Bold), alignment=Qt.AlignCenter))

        # Author
        layout.addWidget(QLabel("Author: @wjgoarxiv", font=QtGui.QFont("Arial", 12, QtGui.QFont.Bold), alignment=Qt.AlignCenter))

        # Links
        hlayout = QHBoxLayout()
        self.github_button = QPushButton("About DWSPapyrus")
        self.github_button.clicked.connect(lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/wjgoarxiv/DWSPapyrus")))
        hlayout.addWidget(self.github_button)

        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        hlayout.addWidget(line)

        self.wjgoarxiv_github_button = QPushButton("My GitHub")
        self.wjgoarxiv_github_button.clicked.connect(lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/wjgoarxiv")))
        hlayout.addWidget(self.wjgoarxiv_github_button)

        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        hlayout.addWidget(line)

        self.wjgoarxiv_hp_button = QPushButton("My Homepage")
        self.wjgoarxiv_hp_button.clicked.connect(lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://woojingo.site")))
        hlayout.addWidget(self.wjgoarxiv_hp_button)

        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        hlayout.addWidget(line)

        self.donate_button = QPushButton("Donate me!")
        self.donate_button.clicked.connect(lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://www.buymeacoffee.com/woojingo")))
        hlayout.addWidget(self.donate_button)

        layout.addLayout(hlayout)

        # Data loading
        self.pressure_dropdown = QComboBox()
        self.pressure_dropdown.addItems(['1', '2'])
        self.temperature_dropdown = QComboBox()
        self.temperature_dropdown.addItems(['1', '2', '3', '4'])
        self.load_button = QPushButton("Load the raw CSV")

        # Dividing section with line 
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Pressure sensor selection:"))
        hlayout.addWidget(self.pressure_dropdown)

        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        hlayout.addWidget(line)

        hlayout.addWidget(QLabel("Temperature sensor selection:"))
        hlayout.addWidget(self.temperature_dropdown)
        hlayout.addWidget(self.load_button)
        layout.addLayout(hlayout)

        self.load_button.clicked.connect(self.load_csv)

        # Create the Data preview section
        self.data_preview_widget = QWidget()
        self.data_preview_layout = QVBoxLayout()
        self.data_preview = QTextEdit()
        self.data_preview_layout.addWidget(QLabel("Data preview:"))
        self.data_preview_layout.addWidget(self.data_preview)
        self.data_preview_widget.setLayout(self.data_preview_layout)

        # Create the Treated data section
        self.treated_data_widget = QWidget()
        self.treated_data_layout = QVBoxLayout()
        self.treated_data = QTextEdit()
        self.treated_data_layout.addWidget(QLabel("Treated data:"))
        self.treated_data_layout.addWidget(self.treated_data)
        self.treated_data_widget.setLayout(self.treated_data_layout)

        # Add the Data preview and Treated data widgets to a QHBoxLayout
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.data_preview_widget)

        # Dividing section with line  
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        hlayout.addWidget(line)

        hlayout.addWidget(self.treated_data_widget)
        layout.addLayout(hlayout)

        # Plot Configuration
        self.x_var_dropdown = QComboBox()
        self.x_var_dropdown.addItems(['Time', 'Temperature', 'Pressure'])
        self.y_var_dropdown = QComboBox()
        self.y_var_dropdown.addItems(['Pressure', 'Temperature'])
        self.x_label = QLineEdit("Time")
        self.y_label = QLineEdit("Pressure")
        self.x_scale = QLineEdit("")
        self.y_scale = QLineEdit("")
        self.dpi = QLineEdit("300")
        self.transparent = QCheckBox("Transparent background")
        self.line_width = QLineEdit("2")
        
        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("X variable selection:"))
        hlayout.addWidget(self.x_var_dropdown)

        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        hlayout.addWidget(line)

        hlayout.addWidget(QLabel("Y variable selection:"))
        hlayout.addWidget(self.y_var_dropdown)
        layout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Write the X label:"))
        hlayout.addWidget(self.x_label)

        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        hlayout.addWidget(line)

        hlayout.addWidget(QLabel("Write the Y label:"))
        hlayout.addWidget(self.y_label)
        layout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("X scale adjustment (min, max):"))
        hlayout.addWidget(self.x_scale)

        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        hlayout.addWidget(line)

        hlayout.addWidget(QLabel("Y scale adjustment (min, max):"))
        hlayout.addWidget(self.y_scale)
        layout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("DPI selection:"))
        hlayout.addWidget(self.dpi) 

        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        hlayout.addWidget(line)

        hlayout.addWidget(QLabel("Transparent background:"))
        hlayout.addWidget(self.transparent)
        layout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Line width selection:"))
        hlayout.addWidget(self.line_width)

        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        hlayout.addWidget(line)

        # Time unit selection
        self.time_unit_dropdown = QComboBox()
        self.time_unit_dropdown.addItems(['Seconds', 'Minutes', 'Hours'])
        hlayout.addWidget(QLabel("Time unit selection:"))
        hlayout.addWidget(self.time_unit_dropdown)
        
        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        hlayout.addWidget(line)

        # Line or scatter
        self.line_or_scatter = QComboBox()
        self.line_or_scatter.addItems(['Line', 'Scatter'])
        hlayout.addWidget(QLabel("Line or scatter:"))
        hlayout.addWidget(self.line_or_scatter)
        layout.addLayout(hlayout)

        # Dividing section with line 
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
      
        # Buttons
        hlayout = QHBoxLayout()
        self.plot_button = QPushButton("Plot data")
        self.plot_button.clicked.connect(self.plot_data)
        hlayout.addWidget(self.plot_button)

        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        hlayout.addWidget(line)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        hlayout.addWidget(self.exit_button)

        layout.addLayout(hlayout)
        central_widget.setLayout(layout)

    def load_csv(self):
      # Open a file dialog to select the CSV file
      file_path, _ = QFileDialog.getOpenFileName(self, "Load the raw CSV", "", "CSV Files (*.csv);;All Files (*)")

      try:
          # Load the CSV file
          df = pd.read_csv(file_path, encoding="cp949", header=1)

          # Get the selected pressure and temperature sensor numbers
          self.pressure_sensor_num = int(self.pressure_dropdown.currentText())
          self.temperature_sensor_num = int(self.temperature_dropdown.currentText())

          # Get the pressure, temperature, and time data
          pressure = df.iloc[1:, self.pressure_sensor_num + 1].astype(float)
          raw_temp = df.iloc[1:, self.temperature_sensor_num + 3].astype(float)
          temp = raw_temp / 10 # Convert raw temperature to real temperature

          # Make time_sec universal
          self.time_sec = df.iloc[1:, 1].astype(float)
          self.time_min = self.time_sec / 60 # Convert time from second to minute

          # Update the data preview text box
          self.data_preview.clear()
          self.data_preview.append("Pressure data:\n")
          self.data_preview.append(str(pressure.head()) + "\n\n")
          self.data_preview.append("Temperature data:\n")
          self.data_preview.append(str(temp.head()))

          pressure_mean = pressure.mean()
          pressure_std = pressure.std()
          temp_mean = temp.mean()
          temp_std = temp.std()

          self.treated_data.clear()
          self.treated_data.append("Treated data:\n")
          self.treated_data.append(f"Pressure mean: {pressure_mean:.2f}\n")
          self.treated_data.append(f"Pressure std: {pressure_std:.2f}\n")
          self.treated_data.append(f"Temperature mean: {temp_mean:.2f}\n")
          self.treated_data.append(f"Temperature std: {temp_std:.2f}\n")

          # Show a success message
          QMessageBox.information(self, "Success", "CSV file loaded successfully.")

          self.df = df

      except Exception as e:
          # Show an error message
          QMessageBox.critical(self, "Error", f"Error loading CSV file: {str(e)}")

    def plot_data(self):
        
        # Warn user if no data is loaded
        if not hasattr(self, "df"):
            QMessageBox.critical(self, "Error", "No data loaded.")
            return
        
        x_var = self.x_var_dropdown.currentText()
        y_var = self.y_var_dropdown.currentText()
        x_label = self.x_label.text()
        y_label = self.y_label.text()
        dpi = int(self.dpi.text())
        transparent = self.transparent.isChecked()
        time_unit = self.time_unit_dropdown.currentText() 
        line_width = int(self.line_width.text())

        fig, ax = plt.subplots()

        rcparams()

        data_x, data_y = None, None
        if x_var == "Time":
            data_x = self.time_sec if time_unit == "Seconds" else self.time_min if time_unit == "Minutes" else self.time_min / 60 if time_unit == "Hours" else None
        elif x_var == "Temperature":
            data_x = self.df.iloc[1:, self.temperature_sensor_num + 3] / 10
        elif x_var == "Pressure":
            data_x = self.df.iloc[1:, self.pressure_sensor_num + 1]

        if y_var == "Pressure":
            data_y = self.df.iloc[1:, self.pressure_sensor_num + 1]
        elif y_var == "Temperature":
            data_y = self.df.iloc[1:, self.temperature_sensor_num + 3] / 10 

        if data_x is None or data_y is None:
            QMessageBox.critical(self, "Error", "Missing Data")
            return
        
        if self.line_or_scatter.currentText() == "Line":
            ax.plot(data_x, data_y, color="black", linewidth=line_width)
        elif self.line_or_scatter.currentText() == "Scatter":
            ax.scatter(data_x, data_y, color="black", s = line_width * 2)

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        # Adjust the x and y scale 
        x_scale = self.x_scale.text()
        y_scale = self.y_scale.text()

        if x_scale != "":
            x_scale = x_scale.split(",")
            ax.set_xlim(float(x_scale[0]), float(x_scale[1]))
        if y_scale != "":
            y_scale = y_scale.split(",")
            ax.set_ylim(float(y_scale[0]), float(y_scale[1]))

        # Tightly fit the plot
        fig.tight_layout()

        # Preview the plot to the user
        canvas = FigureCanvas(fig)

        # Create a new QDialog object to act as the parent widget for the canvas
        dialog = QDialog(self)
        dialog.setWindowTitle("Plot Preview")
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(canvas)

        # Add the Confirm and Cancel buttons to the QDialog
        hlayout = QHBoxLayout()
        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(dialog.accept)
        hlayout.addWidget(confirm_button)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(dialog.reject)
        hlayout.addWidget(cancel_button)
        dialog.layout().addLayout(hlayout)

        # Show the plot preview to the user
        if dialog.exec_() == QDialog.Accepted:
          # Get the file format from the user
          file_format, _ = QFileDialog.getSaveFileName(self, "Save the plot", "", "PNG Files (*.png);;JPG Files (*.jpg);;PDF Files (*.pdf);;SVG Files (*.svg);;All Files (*)")

          if file_format:
              
              # Get the file extension 
              file_ext = file_format.split(".")[-1]

              # Save the plot to the file. 
              fig.savefig(file_format, format=file_ext, dpi=dpi, transparent=transparent, bbox_inches="tight")

              # Show a success message to the user
              QMessageBox.information(self, "Success", "Plot saved successfully as {} file.".format(file_ext.upper()))
          else: 
              # Show an error message to the user
              QMessageBox.critical(self, "Error", "Error saving the plot.")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = DWSPapyrusGUI()
    gui.show()
    sys.exit(app.exec_())