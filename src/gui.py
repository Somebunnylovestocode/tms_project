import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QComboBox, QLabel, QLineEdit, QPushButton,
                           QGroupBox, QFormLayout, QMessageBox, QSplitter)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from .materials import Material
from .capacitance import calculate_capacitance

class CapacitanceCalculatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plate Capacitance Calculator")
        self.setGeometry(100, 100, 1200, 700)
        
        # Create the main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # Create a splitter for control panel and plots
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # Create left panel for controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setMaximumWidth(400)
        
        # Create input groups
        geometry_group = self.create_geometry_group()
        material_group = self.create_material_group()
        parameters_group = self.create_parameters_group()
        
        # Add groups to left panel
        left_layout.addWidget(geometry_group)
        left_layout.addWidget(material_group)
        left_layout.addWidget(parameters_group)
        
        # Create calculate button
        calculate_button = QPushButton("Calculate")
        calculate_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        calculate_button.clicked.connect(self.calculate_and_plot)
        left_layout.addWidget(calculate_button)
        
        # Add stretch to push everything up
        left_layout.addStretch()
        
        # Create right panel for plots
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Create matplotlib figures
        self.figure1 = Figure(figsize=(6, 4))
        self.canvas1 = FigureCanvas(self.figure1)
        self.figure2 = Figure(figsize=(6, 4))
        self.canvas2 = FigureCanvas(self.figure2)
        
        right_layout.addWidget(self.canvas1)
        right_layout.addWidget(self.canvas2)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        
        # Apply stylesheet to the main window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 6px;
                margin-top: 6px;
                padding-top: 10px;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
        """)

    def create_geometry_group(self):
        group = QGroupBox("Geometry")
        layout = QFormLayout()
        
        # Shape selection
        self.shape_combo = QComboBox()
        self.shape_combo.addItems(['circular', 'rectangular'])
        self.shape_combo.currentTextChanged.connect(self.on_shape_changed)
        
        # Boundary condition
        self.boundary_combo = QComboBox()
        self.boundary_combo.addItems(['simply_supported', 'clamped'])
        
        # Dimension inputs
        self.dim_a = QLineEdit('0.001')  # 1mm default
        self.dim_b = QLineEdit('0.001')  # 1mm default
        self.thickness = QLineEdit('0.0001')  # 0.1mm default
        
        layout.addRow("Shape:", self.shape_combo)
        layout.addRow("Boundary:", self.boundary_combo)
        layout.addRow("Length/Radius (m):", self.dim_a)
        layout.addRow("Width (m):", self.dim_b)
        layout.addRow("Thickness (m):", self.thickness)
        
        group.setLayout(layout)
        return group

    def create_material_group(self):
        group = QGroupBox("Material")
        layout = QFormLayout()
        
        # Material selection
        self.material_combo = QComboBox()
        self.material_combo.addItems(list(Material.PREDEFINED_MATERIALS.keys()))
        
        layout.addRow("Material:", self.material_combo)
        group.setLayout(layout)
        return group

    def create_parameters_group(self):
        group = QGroupBox("Parameters")
        layout = QFormLayout()
        
        self.gap = QLineEdit('1e-6')  # 1µm default
        self.pressure_min = QLineEdit('0')
        self.pressure_max = QLineEdit('1000')
        self.pressure_points = QLineEdit('50')
        
        layout.addRow("Initial Gap (m):", self.gap)
        layout.addRow("Min Pressure (Pa):", self.pressure_min)
        layout.addRow("Max Pressure (Pa):", self.pressure_max)
        layout.addRow("Number of Points:", self.pressure_points)
        
        group.setLayout(layout)
        return group

    def on_shape_changed(self, shape):
        # Enable/disable width input based on shape
        self.dim_b.setEnabled(shape == 'rectangular')
        if shape == 'circular':
            self.dim_a.setPlaceholderText("Radius (m)")
        else:
            self.dim_a.setPlaceholderText("Length (m)")

    def calculate_and_plot(self):
        try:
            # Get input values
            shape = self.shape_combo.currentText()
            boundary = self.boundary_combo.currentText()
            material = self.material_combo.currentText()
            thickness = float(self.thickness.text())
            d0 = float(self.gap.text())
            
            # Create pressure array
            p_min = float(self.pressure_min.text())
            p_max = float(self.pressure_max.text())
            n_points = int(self.pressure_points.text())
            pressures = np.linspace(p_min, p_max, n_points)
            
            # Calculate capacitances
            capacitances = []
            for p in pressures:
                if shape == 'circular':
                    a = float(self.dim_a.text())
                    cap = calculate_capacitance(shape, boundary, p, material, 
                                             thickness, a, d0=d0)
                else:
                    a = float(self.dim_a.text())
                    # b = float(self.dim_b.text())
                    b = 0.001
                    cap = calculate_capacitance(shape, boundary, p, material, 
                                             thickness, a, b, d0)
                capacitances.append(cap)
            
            # Convert to numpy array
            capacitances = np.array(capacitances)
            
            # Plot capacitance vs pressure
            self.figure1.clear()
            ax1 = self.figure1.add_subplot(111)
            ax1.plot(pressures, capacitances * 1e12, 'b-', linewidth=2)
            ax1.set_xlabel('Pressure (Pa)')
            ax1.set_ylabel('Capacitance (pF)')
            ax1.set_title('Capacitance vs Pressure')
            ax1.grid(True)
            self.figure1.tight_layout()
            self.canvas1.draw()
            
            # Plot percentage change
            self.figure2.clear()
            ax2 = self.figure2.add_subplot(111)
            c0 = capacitances[0]
            percent_change = ((capacitances - c0) / c0) * 100
            ax2.plot(pressures, percent_change, 'r-', linewidth=2)
            ax2.set_xlabel('Pressure (Pa)')
            ax2.set_ylabel('Capacitance Change (%)')
            ax2.set_title('Relative Capacitance Change vs Pressure')
            ax2.grid(True)
            self.figure2.tight_layout()
            self.canvas2.draw()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))