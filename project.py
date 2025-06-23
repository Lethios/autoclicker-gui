from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QLabel, QComboBox, QHBoxLayout, QFrame, QStackedWidget, QGroupBox, QSpinBox, QCheckBox, QRadioButton, QGridLayout, QButtonGroup, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icons/Lethios.png"))
        self.setWindowTitle("Lethios's Auto Clicker & Macro Tool")
        self.setFixedSize(750, 450)
        self.setStyleSheet("background-color: #2B2B2B;")

        # Create main container and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # ===== SIDEBAR SETUP =====
        sidebar = self.create_sidebar()

        # ===== MAIN CONTENT AREA SETUP =====
        main_content = QFrame()
        main_content.setFrameShape(QFrame.StyledPanel)
        main_content.setStyleSheet("background-color: #333333; border-radius: 10px;")

        # Create stacked widget to hold different pages
        stackedWidget = QStackedWidget()

        # ===== CREATE ALL PAGES =====
        autoclicker_widget = self.create_autoclicker_page()
        macro_widget = self.create_macro_page()
        settings_widget = self.create_settings_page()
        about_widget = self.create_about_page()

        # Add all pages to stacked widget
        stackedWidget.addWidget(autoclicker_widget)
        stackedWidget.addWidget(macro_widget)
        stackedWidget.addWidget(settings_widget)
        stackedWidget.addWidget(about_widget)

        # Set default page
        stackedWidget.setCurrentWidget(autoclicker_widget)

        # Add stacked widget to main content area
        main_content_layout = QVBoxLayout(main_content)
        main_content_layout.setContentsMargins(15, 15, 15, 15)
        main_content_layout.addWidget(stackedWidget)

        # ===== FINAL LAYOUT ASSEMBLY =====
        main_layout.addWidget(sidebar, 1)  # Sidebar takes 1/4 of space
        main_layout.addWidget(main_content, 3)  # Main content takes 3/4 of space

        # ===== CONNECT NAVIGATION BUTTONS =====
        self.sidebar_buttons['autoclicker'].clicked.connect(
            lambda: stackedWidget.setCurrentWidget(autoclicker_widget)
        )
        self.sidebar_buttons['macro'].clicked.connect(
            lambda: stackedWidget.setCurrentWidget(macro_widget)
        )
        self.sidebar_buttons['settings'].clicked.connect(
            lambda: stackedWidget.setCurrentWidget(settings_widget)
        )
        self.sidebar_buttons['about'].clicked.connect(
            lambda: stackedWidget.setCurrentWidget(about_widget)
        )

    def create_sidebar(self):
        """Create and return the sidebar with navigation buttons"""
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.StyledPanel)
        sidebar.setStyleSheet("background-color: #333333; border-radius: 10px;")
        sidebar_layout = QVBoxLayout(sidebar)

        # Application title
        title = QLabel("AutoClicker GUI")
        title.setStyleSheet("color: white; font-size: 18px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(20)

        # Button styling
        button_style = """
            QPushButton {
                background-color: #1197DC;
                border: none;
                color: white;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0E74AA;
            }
        """

        # Navigation buttons
        self.sidebar_buttons = {}
        button_names = [
            ('autoclicker', 'Auto Clicker'),
            ('macro', 'Macro'),
            ('settings', 'Settings')
        ]

        for key, text in button_names:
            button = QPushButton(text)
            button.setStyleSheet(button_style)
            self.sidebar_buttons[key] = button
            sidebar_layout.addWidget(button)
            sidebar_layout.addSpacing(10)

        sidebar_layout.addSpacing(100)

        # Killswitch information
        killswitch_info = QLabel("CTRL + SHIFT + K\nTo kill the application")
        killswitch_info.setStyleSheet("color: white; font-size: 12px;")
        killswitch_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(killswitch_info)

        sidebar_layout.addSpacing(120)

        # About button (separate from navigation)
        about_button = QPushButton("About")
        about_button.setStyleSheet(button_style)
        self.sidebar_buttons['about'] = about_button
        sidebar_layout.addWidget(about_button)
        sidebar_layout.addStretch()  # Push everything to top

        return sidebar

    def create_autoclicker_page(self):
        autoclicker_widget = QWidget()
        autoclicker_layout = QVBoxLayout(autoclicker_widget)

        # ---------- Frame 1: Click Interval ----------
        frame1 = QFrame()
        frame1.setFrameShape(QFrame.StyledPanel)
        frame1.setStyleSheet("background-color: #3A3A3A; border-radius: 10px;")
        frame1.setFixedSize(500, 100)
        frame1_layout = QVBoxLayout(frame1)

        click_label = QLabel("Click Interval:")
        click_label.setStyleSheet("color: white;")

        # SpinBoxes
        ms_box = QSpinBox()
        sec_box = QSpinBox()
        min_box = QSpinBox()
        hour_box = QSpinBox()

        # Set ranges and styles
        spinbox_style = """
                QSpinBox {
                    background-color: #333333;
                    color: white;
                    border: 1px solid #555;
                    border-radius: 4px;
                    padding: 2px 5px;
                }
                QSpinBox::up-button, QSpinBox::down-button {
                    width: 0px;
                    height: 0px;
                    border: none;
                }
        """
        for box in (ms_box, sec_box, min_box, hour_box):
            box.setRange(0, 1000)
            box.setFixedWidth(60)
            box.setStyleSheet(spinbox_style)

        # Layout for time inputs
        time_layout = QHBoxLayout()
        time_layout.setSpacing(8)
        for label_text, box in zip(["Millisecond:", "Second:", "Minute:", "Hour:"], (ms_box, sec_box, min_box, hour_box)):
            label = QLabel(label_text)
            label.setStyleSheet("color: white;")
            time_layout.addWidget(label)
            time_layout.addWidget(box)

        frame1_layout.addWidget(click_label)
        frame1_layout.addSpacing(10)
        frame1_layout.addLayout(time_layout)
        frame1_layout.addStretch()

        # ---------- Frame 2: Click Options ----------
        frame2 = QFrame()
        frame2.setFrameShape(QFrame.StyledPanel)
        frame2.setStyleSheet("background-color: #3A3A3A; border-radius: 10px;")
        frame2.setFixedSize(500, 100)
        frame2_layout = QVBoxLayout(frame2)

        click_option_label = QLabel("Click Options:")
        click_option_label.setStyleSheet("color: white;")

        combobox_style = """
            QComboBox {
                background-color: #333333;
                color: white;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 2px 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #333333;
                color: white;
            }
        """
        mouse_button_dropdown = QComboBox()
        mouse_button_dropdown.addItems(["Left", "Right", "Middle"])
        mouse_button_dropdown.setStyleSheet(combobox_style)

        click_type_dropdown = QComboBox()
        click_type_dropdown.addItems(["Single", "Double"])
        click_type_dropdown.setStyleSheet(combobox_style)

        hold_label = QLabel("Hold Duration (s):")
        hold_label.setStyleSheet("color: white;")

        hold_spinbox = QSpinBox()
        hold_spinbox.setRange(0, 60)
        hold_spinbox.setFixedWidth(60)
        hold_spinbox.setStyleSheet(spinbox_style)

        hold_layout = QHBoxLayout()
        hold_layout.setSpacing(5)
        hold_layout.addWidget(hold_label)
        hold_layout.addWidget(hold_spinbox)
        hold_layout.setContentsMargins(0, 0, 0, 0)

        row_layout = QHBoxLayout()
        row_layout.setSpacing(10)
        row_layout.addWidget(mouse_button_dropdown)
        row_layout.addWidget(click_type_dropdown)
        row_layout.addLayout(hold_layout)

        frame2_layout.addWidget(click_option_label)
        frame2_layout.addSpacing(10)
        frame2_layout.addLayout(row_layout)
        frame2_layout.addStretch()

        # ----------- Frame 3: Cursor Position -----------
        frame3 = QFrame()
        frame3.setFrameShape(QFrame.StyledPanel)
        frame3.setStyleSheet("background-color: #3A3A3A; border-radius: 10px;")
        frame3.setMinimumHeight(100)  # Let it expand as needed
        frame3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Allow horizontal stretch

        frame3_layout = QVBoxLayout(frame3)
        frame3_layout.setContentsMargins(10, 10, 10, 10)
        frame3_layout.setSpacing(8)

        cursor_label = QLabel("Cursor Position:")
        cursor_label.setStyleSheet("color: white;")
        cursor_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Checkboxes
        current_checkbox = QCheckBox("Current")
        custom_checkbox = QCheckBox("Custom")
        for checkbox in (current_checkbox, custom_checkbox):
            checkbox.setStyleSheet("color: white;")

        # SpinBoxes
        x_spinbox = QSpinBox()
        y_spinbox = QSpinBox()
        for spin in (x_spinbox, y_spinbox):
            spin.setRange(0, 9999)
            spin.setFixedWidth(60)
            spin.setStyleSheet(spinbox_style)

        # Tight X/Y Layouts
        x_layout = QHBoxLayout()
        x_label = QLabel("X:")
        x_label.setStyleSheet("color: white;")
        x_layout.addWidget(x_label)
        x_layout.addWidget(x_spinbox)
        x_layout.setSpacing(4)
        x_layout.setContentsMargins(0, 0, 0, 0)

        y_layout = QHBoxLayout()
        y_label = QLabel("Y:")
        y_label.setStyleSheet("color: white;")
        y_layout.addWidget(y_label)
        y_layout.addWidget(y_spinbox)
        y_layout.setSpacing(4)
        y_layout.setContentsMargins(0, 0, 0, 0)

        # Combine custom layout row
        custom_layout = QHBoxLayout()
        custom_layout.addWidget(custom_checkbox)
        custom_layout.addLayout(x_layout)
        custom_layout.addLayout(y_layout)
        custom_layout.addStretch()
        custom_layout.setSpacing(12)

        # Final assemble
        frame3_layout.addWidget(cursor_label)
        frame3_layout.addWidget(current_checkbox)
        frame3_layout.addLayout(custom_layout)

        # ----------- Frame 4: Repeat Options -----------
        frame4 = QFrame()
        frame4.setFrameShape(QFrame.StyledPanel)
        frame4.setStyleSheet("background-color: #3A3A3A; border-radius: 10px;")
        frame4.setMinimumHeight(100)
        frame4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        frame4_layout = QVBoxLayout(frame4)
        frame4_layout.setContentsMargins(10, 10, 10, 10)
        frame4_layout.setSpacing(8)

        repeat_label = QLabel("Repeat Options:")
        repeat_label.setStyleSheet("color: white;")
        repeat_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Toggle checkbox (centered vertically left)
        toggle_checkbox = QCheckBox("Toggle")
        toggle_checkbox.setStyleSheet("color: white;")
        toggle_row = QHBoxLayout()
        toggle_row.addWidget(toggle_checkbox)
        toggle_row.addStretch()

        # Repeat checkbox + spinbox
        repeat_checkbox = QCheckBox("Repeat")
        repeat_checkbox.setStyleSheet("color: white;")

        repeat_spinbox = QSpinBox()
        repeat_spinbox.setRange(1, 9999)
        repeat_spinbox.setFixedWidth(60)
        repeat_spinbox.setStyleSheet(spinbox_style)

        repeat_row = QHBoxLayout()
        repeat_row.setSpacing(10)
        repeat_row.addWidget(repeat_checkbox)
        repeat_row.addWidget(repeat_spinbox)
        repeat_row.addStretch()

        # Final frame layout
        frame4_layout.addWidget(repeat_label)
        frame4_layout.addLayout(toggle_row)
        frame4_layout.addLayout(repeat_row)

        # --- Button Row at Bottom ---
        bottom_button_layout = QHBoxLayout()
        bottom_button_layout.setSpacing(20)
        bottom_button_layout.setContentsMargins(0, 10, 0, 10)
        bottom_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        start_button = QPushButton("Start")
        stop_button = QPushButton("Stop")

        for button in (start_button, stop_button):
            button_style = """
                QPushButton {
                    background-color: #1197DC;
                    border: none;
                    color: white;
                    padding: 10px;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #0E74AA;
                }
            """
            button.setFixedWidth(200)
            button.setStyleSheet(button_style)

        bottom_button_layout.addWidget(start_button)
        bottom_button_layout.addWidget(stop_button)

        # ---------- Add Frames to Main Layout ----------
        autoclicker_layout.addWidget(frame1)
        autoclicker_layout.addSpacing(15)

        autoclicker_layout.addWidget(frame2)
        autoclicker_layout.addSpacing(15)

        row_layout = QHBoxLayout()
        row_layout.addWidget(frame3)
        row_layout.addSpacing(15)
        row_layout.addWidget(frame4)
        autoclicker_layout.addLayout(row_layout)
        autoclicker_layout.addSpacing(15)
        autoclicker_layout.addLayout(bottom_button_layout)

        autoclicker_layout.addStretch()

        return autoclicker_widget


    def create_macro_page(self):
        """Create and return the macro page"""
        macro_widget = QWidget()
        macro_layout = QVBoxLayout(macro_widget)
        
        # Placeholder content
        label = QLabel("Macro Page - Under Construction")
        label.setStyleSheet("color: white; font-size: 16px;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        macro_layout.addWidget(label)
        
        return macro_widget

    def create_settings_page(self):
        """Create and return the settings page"""
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        
        # Placeholder content
        label = QLabel("Settings Page - Under Construction")
        label.setStyleSheet("color: white; font-size: 16px;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings_layout.addWidget(label)
        
        return settings_widget

    def create_about_page(self):
        """Create and return the about page"""
        about_widget = QWidget()
        about_layout = QVBoxLayout(about_widget)
        about_layout.setContentsMargins(20, 20, 20, 20)

        # About page content
        title = QLabel("AutoClicker GUI")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        
        description = QLabel("A lightweight tool for automating clicks and macros.")
        description.setStyleSheet("color: white;")
        
        author = QLabel("Developed by Lethios")
        author.setStyleSheet("color: white;")
        
        github = QLabel(
            "<a href='https://github.com/Lethios/autoclicker-gui' "
            "style='color:#1197DC; text-decoration:none;'>GitHub Repository</a>"
        )
        github.setOpenExternalLinks(True)
        
        license_info = QLabel("This project is licensed under the MIT License.")
        license_info.setStyleSheet("color: white;")

        # Add all content to layout
        about_layout.addWidget(title)
        about_layout.addSpacing(10)
        about_layout.addWidget(description)
        about_layout.addSpacing(10)
        about_layout.addWidget(author)
        about_layout.addWidget(github)
        about_layout.addWidget(license_info)
        about_layout.addStretch()  # Push content to top

        return about_widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
