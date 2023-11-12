from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QTextEdit, QCheckBox, QLineEdit, QFileDialog, QWidget, QMessageBox, QDialog, QFrame
from PyQt6.QtCore import Qt
from PyQt6 import QtGui, QtCore
from PyQt6.QtGui import QPixmap
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
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)
 
        # Title 
        layout.addWidget(QLabel("DWSPapyrus", font=QtGui.QFont("Arial", 20, QtGui.QFont.Weight.Bold), alignment=QtCore.Qt.AlignmentFlag.AlignCenter))

        # Version 
        layout.addWidget(QLabel("버젼 1.2.2", font=QtGui.QFont("Arial", 12, QtGui.QFont.Weight.Bold), alignment=QtCore.Qt.AlignmentFlag.AlignCenter))

        # Author
        layout.addWidget(QLabel("저자: @wjgoarxiv", font=QtGui.QFont("Arial", 12, QtGui.QFont.Weight.Bold), alignment=QtCore.Qt.AlignmentFlag.AlignCenter))

        # Links
        hlayout = QHBoxLayout()
        self.github_button = QPushButton("DWSPapyrus에 관하여")
        self.github_button.clicked.connect(lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/wjgoarxiv/DWSPapyrus")))
        hlayout.addWidget(self.github_button)

        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        hlayout.addWidget(line)

        self.wjgoarxiv_github_button = QPushButton("저자 GitHub")
        self.wjgoarxiv_github_button.clicked.connect(lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/wjgoarxiv")))
        hlayout.addWidget(self.wjgoarxiv_github_button)

        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        hlayout.addWidget(line)

        self.wjgoarxiv_hp_button = QPushButton("저자 홈페이지")
        self.wjgoarxiv_hp_button.clicked.connect(lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://woojingo.site")))
        hlayout.addWidget(self.wjgoarxiv_hp_button)

        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        hlayout.addWidget(line)

        self.donate_button = QPushButton("저자에게 기부를!")
        self.donate_button.clicked.connect(lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://www.buymeacoffee.com/woojingo")))
        hlayout.addWidget(self.donate_button)

        layout.addLayout(hlayout)

        # Data loading
        self.pressure_dropdown = QComboBox()
        self.pressure_dropdown.addItems(['1', '2'])
        self.temperature_dropdown = QComboBox()
        self.temperature_dropdown.addItems(['1', '2', '3', '4'])
        self.load_button = QPushButton("데이터 불러오기")

        # Add the function to divide pressure by:
        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("압력 센서 값을 다음 숫자로 나누기:"), alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.divide_pressure_by = QLineEdit("1")
        hlayout.addWidget(self.divide_pressure_by)
        layout.addLayout(hlayout)

        # Add the function to divide temp. by:
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("온도 센서 값을 다음 숫자로 나누기:"), alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.divide_temp_by = QLineEdit("10")
        hlayout.addWidget(self.divide_temp_by)
        layout.addLayout(hlayout)

        # Dividing section with line 
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)
        
        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("사용한 압력 센서 번호 선택:"))
        hlayout.addWidget(self.pressure_dropdown)

        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        hlayout.addWidget(line)

        hlayout.addWidget(QLabel("사용한 온도 센서 번호 선택:"))
        hlayout.addWidget(self.temperature_dropdown)
        hlayout.addWidget(self.load_button)
        layout.addLayout(hlayout)

        self.load_button.clicked.connect(self.load_csv)

        # Dividing section with line 
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Create the Data preview section
        self.data_preview_widget = QWidget()
        self.data_preview_layout = QVBoxLayout()
        self.data_preview = QTextEdit()
        self.data_preview_layout.addWidget(QLabel("불러온 데이터 미리보기:"))
        self.data_preview_layout.addWidget(self.data_preview)
        self.data_preview_widget.setLayout(self.data_preview_layout)

        # Create the Treated data section
        self.treated_data_widget = QWidget()
        self.treated_data_layout = QVBoxLayout()
        self.treated_data = QTextEdit()
        self.treated_data_layout.addWidget(QLabel("처리된 데이터 미리보기:"))
        self.treated_data_layout.addWidget(self.treated_data)
        self.treated_data_widget.setLayout(self.treated_data_layout)

        # Add the Data preview and Treated data widgets to a QHBoxLayout
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.data_preview_widget)

        # Dividing section with line  
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        hlayout.addWidget(line)

        hlayout.addWidget(self.treated_data_widget)
        layout.addLayout(hlayout)

        # Plot Configuration
        self.x_var_dropdown = QComboBox()
        self.x_var_dropdown.addItems(['시간', '온도', '압력'])
        self.y_var_dropdown = QComboBox()
        self.y_var_dropdown.addItems(['온도', '압력'])
        self.x_label = QLineEdit("Time")
        self.y_label = QLineEdit("Temperature")
        self.x_scale = QLineEdit("")
        self.y_scale = QLineEdit("")
        self.dpi = QLineEdit("350")
        self.transparent = QCheckBox("그래프 배경 투명화")
        self.line_width = QLineEdit("2")

        # Map variable names to label names
        self.variable_labels = {
            '시간': 'Time',
            '온도': 'Temperature',
            '압력': 'Pressure'
        }

        # Connect dropdowns to label update function
        self.x_var_dropdown.currentTextChanged.connect(self.update_labels)
        self.y_var_dropdown.currentTextChanged.connect(self.update_labels)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("X 변수 선택:"))
        hlayout.addWidget(self.x_var_dropdown)

        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        hlayout.addWidget(line)

        hlayout.addWidget(QLabel("Y 변수 선택:"))
        hlayout.addWidget(self.y_var_dropdown)
        layout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("X 라벨명 작성 (영어로):"))
        hlayout.addWidget(self.x_label)

        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        hlayout.addWidget(line)

        hlayout.addWidget(QLabel("Y 라벨명 작성 (영어로):"))
        hlayout.addWidget(self.y_label)
        layout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("X 값 범위 조정 (최소, 최대):"))
        hlayout.addWidget(self.x_scale)

        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        hlayout.addWidget(line)

        hlayout.addWidget(QLabel("Y 값 범위 조정 (최소, 최대):"))
        hlayout.addWidget(self.y_scale)
        layout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("DPI (그래프 해상도) 입력:"))
        hlayout.addWidget(self.dpi) 

        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        hlayout.addWidget(line)

        hlayout.addWidget(QLabel("체크 시 투명화!"))
        hlayout.addWidget(self.transparent)
        layout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("선 (점) 굵기 (크기) 설정:"))
        hlayout.addWidget(self.line_width)

        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        hlayout.addWidget(line)

        # Time unit selection
        self.time_unit_dropdown = QComboBox()
        self.time_unit_dropdown.addItems(['초', '분', '시간'])

        # Mapping from Korean to English
        self.time_unit_mapping = { 
            '초': 'Time (sec)',
            '분': 'Time (min)',
            '시간': 'Time (hr)'
        }
        
        # Connect the signals
        self.time_unit_dropdown.currentTextChanged.connect(self.update_time_label)

        hlayout.addWidget(QLabel("시간 단위 선택:"))
        hlayout.addWidget(self.time_unit_dropdown)
        
        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        hlayout.addWidget(line)

        # Line or scatter
        self.line_or_scatter = QComboBox()
        self.line_or_scatter.addItems(['선', '점'])
        hlayout.addWidget(QLabel("선 또는 점 선택:"))
        hlayout.addWidget(self.line_or_scatter)
        layout.addLayout(hlayout)

        # Dividing section with line 
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)
      
        # Buttons
        hlayout = QHBoxLayout()
        self.plot_button = QPushButton("플롯!")
        self.plot_button.clicked.connect(self.plot_data)
        hlayout.addWidget(self.plot_button)

        # Dividing section with line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        hlayout.addWidget(line)

        self.exit_button = QPushButton("종료하기")
        self.exit_button.clicked.connect(self.close)
        hlayout.addWidget(self.exit_button)

        layout.addLayout(hlayout)
        central_widget.setLayout(layout)

    def load_csv(self):
      # Open a file dialog to select the CSV file
      file_path, _ = QFileDialog.getOpenFileName(self, "실험 자료 (CSV)를 불러오세요.", "", "CSV Files (*.csv);;All Files (*)")

      try:
          # Load the CSV file
          df = pd.read_csv(file_path, encoding="cp949", header=1)

          # Get the selected pressure and temperature sensor numbers
          self.pressure_sensor_num = int(self.pressure_dropdown.currentText())
          self.temperature_sensor_num = int(self.temperature_dropdown.currentText())

          # Get the pressure, temperature, and time data
          pressure = df.iloc[1:, self.pressure_sensor_num + 1].astype(float)
          pres = pressure / float(self.divide_pressure_by.text())

          raw_temp = df.iloc[1:, self.temperature_sensor_num + 3].astype(float)
          temp = raw_temp / float(self.divide_temp_by.text())

          # Make time_sec universal
          self.time_sec = df.iloc[1:, 1].astype(float)
          self.time_min = self.time_sec / 60 # Convert time from second to minute

          # Update the data preview text box
          self.data_preview.clear()
          self.data_preview.append("압력 데이터:\n")
          self.data_preview.append(str(pres.head()) + "\n\n")
          self.data_preview.append("온도 데이터:\n")
          self.data_preview.append(str(temp.head()))

          pres_mean = pres.mean()
          pres_std = pres.std()
          temp_mean = temp.mean()
          temp_std = temp.std()

          self.treated_data.clear()
          self.treated_data.append("처리된 데이터 미리보기:\n")
          self.treated_data.append(f"Pressure mean: {pres_mean:.2f}\n")
          self.treated_data.append(f"Pressure std: {pres_std:.2f}\n")
          self.treated_data.append(f"Temperature mean: {temp_mean:.2f}\n")
          self.treated_data.append(f"Temperature std: {temp_std:.2f}\n")

          # Show a success message
          QMessageBox.information(self, "Success", "CSV 파일을 성공적으로 불러왔어요.")

          self.df = df

      except Exception as e:
          # Show an error message
          QMessageBox.critical(self, "Error", f"CSV 파일을 불러오는데 실패했어요. 에러: {e}")

    def plot_data(self):
        
        # Warn user if no data is loaded
        if not hasattr(self, "df"):
            QMessageBox.critical(self, "Error", "데이터를 불러오지 못했어요.")
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
        if x_var == "시간":
            data_x = self.time_sec if time_unit == "초" else self.time_min if time_unit == "분" else self.time_min / 60 if time_unit == "시간" else None
        elif x_var == "온도":
            data_x = self.df.iloc[1:, self.temperature_sensor_num + 3] / float(self.divide_temp_by.text())
        elif x_var == "압력":
            data_x = self.df.iloc[1:, self.pressure_sensor_num + 1] / float(self.divide_pressure_by.text())

        if y_var == "압력":
            data_y = self.df.iloc[1:, self.pressure_sensor_num + 1] / float(self.divide_pressure_by.text())
        elif y_var == "온도":
            data_y = self.df.iloc[1:, self.temperature_sensor_num + 3] / float(self.divide_temp_by.text())

        if data_x is None or data_y is None:
            QMessageBox.critical(self, "Error", "데이터를 불러오지 못했어요.")
            return
        
        if self.line_or_scatter.currentText() == "선":
            ax.plot(data_x, data_y, color="black", linewidth=line_width)
        elif self.line_or_scatter.currentText() == "점":
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
        dialog.setWindowTitle("그래프 미리보기")
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(canvas)

        # Add the Confirm and Cancel buttons to the QDialog
        hlayout = QHBoxLayout()
        confirm_button = QPushButton("확인")
        confirm_button.clicked.connect(dialog.accept)
        hlayout.addWidget(confirm_button)
        cancel_button = QPushButton("취소")
        cancel_button.clicked.connect(dialog.close)
        hlayout.addWidget(cancel_button)
        dialog.layout().addLayout(hlayout)

        # Show the plot preview to the user
        if dialog.exec() == QDialog.DialogCode.Accepted:
          # Get the file format from the user
          file_format, _ = QFileDialog.getSaveFileName(self, "그래프를 저장하세요", "", "PNG Files (*.png);;JPG Files (*.jpg);;PDF Files (*.pdf);;SVG Files (*.svg);;All Files (*)")

          if file_format:
              
              # Get the file extension 
              file_ext = file_format.split(".")[-1]

              # Save the plot to the file. 
              fig.savefig(file_format, format=file_ext, dpi=dpi, transparent=transparent, bbox_inches="tight")

              # Show a success message to the user
              QMessageBox.information(self, "Success", "그래프를 {} 확장자로 저장했어요.".format(file_ext.upper()))
          else: 
              # Show an error message to the user
              QMessageBox.critical(self, "Error", "그래프를 저장하지 못했어요.")

    def update_labels(self):
        self.x_label.setText(self.variable_labels.get(self.x_var_dropdown.currentText(), ''))
        self.y_label.setText(self.variable_labels.get(self.y_var_dropdown.currentText(), ''))

    def update_time_label(self):
        if self.x_var_dropdown.currentText() == "시간":
            self.x_label.setText(self.time_unit_mapping.get(self.time_unit_dropdown.currentText(), ''))

# Stylesheet addition
my_stylesheet = """
/* General Styles */
QWidget {
    background-color: #ffffff; /* Light background color */
    color: #094067; /* Dark text color */
    font-family: Helvetica, Arial;
}

/* Custom font for Headlines/Labels with a rounded background */
QLabel {
    font-size: 15px;
    color: #ffffff; /* Assuming white text for contrast */
    background-color: #3da9fc; /* Button background color for visibility */
    font-weight: bold;
    padding: 2px; /* Padding to ensure text doesn't touch the border edge */
    border: None; /* No border */
    border-radius: 6px; 
    margin: 1px; /* Optional margin around the label */
    /* Additional QLabel styles if needed */
}
/* Styles for QPushButton */
QPushButton {
    background-color: #3da9fc; /* Button background color */
    color: #ffffff; /* Light button text color */
    border: None; /* No border */
    border-radius: 4px;
    padding: 5px 10px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #90b4ce; /* Lighter secondary color for hover state */
}

QPushButton:pressed {
    background-color: #ef4565; /* Tertiary color for pressed state */
}

QTextEdit {
    background-color: #ffffff; /* Light background color for text edit */
    border: 1px solid #90b4ce; /* Light secondary color for border */
    border-radius: 4px;
    padding: 4px;
    color: #fffffe; /* Changed to black text color for better visibility */
}

/* Styles for QComboBox */
QComboBox {
    background-color: #fffffe; /* Light background color for better visibility */
    color: #5f6c7b; /* Dark text color for better visibility */
    border: 1px solid #90b4ce; /* Light secondary color for border */
    border-radius: 4px;
    padding: 4px;
    min-width: 6em;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;
    border-left-width: 1px;
    border-left-color: #90b4ce; /* Light secondary color for border */
    border-left-style: solid;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
}

QComboBox::down-arrow {
    image: url(path/to/arrow.png); /* Replace with the actual path to the arrow image */
}

/* Style for QComboBox when it's expanded (showing the dropdown items) */
QComboBox QAbstractItemView {
    border: 1px solid #90b4ce; /* Light secondary color for border */
    selection-background-color: #3da9fc; /* Button background color for the selected item */
    selection-color: #ffffff; /* Light button text color for the selected item */
    background-color: #fffffe; /* Light background color for the dropdown */
    color: #5f6c7b; /* Dark text color for the dropdown items */
}

/* Styles for QFrame used as a line */
QFrame {
    background-color: #094067; /* Dark stroke color for lines */
}

/* Styles for the QMainWindow */
QMainWindow {
    background-color: #ffffff; /* Light background color */
}

/* Additional styling for other widgets like QMenuBar, QStatusBar, QToolBar if they are used */
QMenuBar {
	background-color: #ffffff; /* Light background color */
	color: #094067; /* Dark text color */
	border-bottom: 1px solid #90b4ce; /* Light secondary color for border */
}

QMenuBar::item {
	spacing: 3px; /* spacing between menu bar items */
	padding: 1px 4px;
	background: transparent;
}

QMenuBar::item:selected {
	background: #90b4ce; /* Light secondary color for selected menu bar item */
}

QMenuBar::item:pressed {
	background: #ef4565; /* Tertiary color for pressed menu bar item */
}

/* Styles for QFileDialog */
QFileDialog {
    background-color: #ffffff; /* Light background color */
	color: #094067; /* Dark text color */
    border: 1px solid #90b4ce; /* Light secondary color for border */
    border-radius: 4px;
    padding: 4px;
}

QFileDialog QListView, QFileDialog QTreeView {
	background-color: #ffffff; /* Light background color */
	border: 1px solid #90b4ce; /* Light secondary color for border */
	border-radius: 4px;
	padding: 4px;
}

QFileDialog QListView::item, QFileDialog QTreeView::item {
	background-color: #ffffff; /* Light background color */
	color: #094067; /* Dark text color */
}	

QFileDialog QListView::item:selected, QFileDialog QTreeView::item:selected {
	background-color: #90b4ce; /* Light secondary color for border */
	color: #ffffff; /* Light text color */
}

QStatusBar {
	background-color: #ffffff; /* Light background color */
	color: #094067; /* Dark text color */
	border-top: 1px solid #90b4ce; /* Light secondary color for border */
}

QToolBar {
	background-color: #ffffff; /* Light background color */
	border-bottom: 1px solid #90b4ce; /* Light secondary color for border */
}

QToolBar::separator {
	background-color: #90b4ce; /* Light secondary color for border */
	width: 1px;
	height: 1px;
}

QToolButton {
	background-color: #ffffff; /* Light background color */
	border: 1px solid #90b4ce; /* Light secondary color for border */
	border-radius: 4px;
	padding: 4px;
}

QToolButton:hover {
	background-color: #90b4ce; /* Light secondary color for border */
}

QToolButton:checked {
	background-color: #ef4565; /* Tertiary color for pressed state */
}

QToolButton:pressed {
	background-color: #ef4565; /* Tertiary color for pressed state */
}

QToolButton:disabled {
	background-color: #ffffff; /* Light background color */
	border: 1px solid #90b4ce; /* Light secondary color for border */
	border-radius: 4px;
	padding: 4px;
}

QToolButton:checked:disabled {
	background-color: #ef4565; /* Tertiary color for pressed state */
}

QToolButton:pressed:disabled {
	background-color: #ef4565; /* Tertiary color for pressed state */
}

/* Styles for QTabWidget */

QTabWidget::pane {
	border: 1px solid #90b4ce; /* Light secondary color for border */
	padding: 4px;
}

QTabWidget::tab-bar {
	left: 5px; /* move to the right by 5px */
}
"""
        
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Stylesheet addition
    app.setStyleSheet(my_stylesheet)

    # Create the main window
    gui = DWSPapyrusGUI()
    gui.show()
    sys.exit(app.exec())