import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._initialize_ui()
        self._connect_navigation()

    def _setup_window(self):
        self.setWindowIcon(QIcon("icons/Lethios.png"))
        self.setWindowTitle("Lethios's Auto Clicker & Macro Tool")
        self.setFixedSize(750, 450)
        self.setStyleSheet("background-color: #2B2B2B;")

    def _initialize_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        sidebar = self._create_sidebar()
        main_content = self._create_main_content()

        main_layout.addWidget(sidebar, 1)
        main_layout.addWidget(main_content, 3)

    def _create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.StyledPanel)
        sidebar.setStyleSheet("background-color: #333333; border-radius: 10px;")
        sidebar_layout = QVBoxLayout(sidebar)

        title = QLabel("AutoClicker GUI")
        title.setStyleSheet("color: white; font-size: 18px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(20)

        self.sidebar_buttons = {}
        self._create_navigation_buttons(sidebar_layout)

        self._add_killswitch_info(sidebar_layout)

        self._add_about_button(sidebar_layout)

        return sidebar

    def _create_navigation_buttons(self, layout):
        button_style = self._get_button_style()
        
        button_configs = [
            ('autoclicker', 'Auto Clicker'),
            ('macro', 'Macro'),
            ('settings', 'Settings')
        ]

        for key, text in button_configs:
            button = QPushButton(text)
            button.setStyleSheet(button_style)
            self.sidebar_buttons[key] = button
            layout.addWidget(button)
            layout.addSpacing(10)

    def _add_killswitch_info(self, layout):
        layout.addSpacing(100)
        
        killswitch_info = QLabel("CTRL + SHIFT + K\nTo kill the application")
        killswitch_info.setStyleSheet("color: white; font-size: 12px;")
        killswitch_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(killswitch_info)
        layout.addSpacing(120)

    def _add_about_button(self, layout):
        about_button = QPushButton("About")
        about_button.setStyleSheet(self._get_button_style())
        self.sidebar_buttons['about'] = about_button
        layout.addWidget(about_button)
        layout.addStretch()

    def _create_main_content(self):
        main_content = QFrame()
        main_content.setFrameShape(QFrame.StyledPanel)
        main_content.setStyleSheet("background-color: #333333; border-radius: 10px;")

        self.stacked_widget = QStackedWidget()

        pages = {
            'autoclicker': self._create_autoclicker_page(),
            'macro': self._create_macro_page(),
            'settings': self._create_settings_page(),
            'about': self._create_about_page()
        }

        for page in pages.values():
            self.stacked_widget.addWidget(page)

        self.stacked_widget.setCurrentWidget(pages['autoclicker'])

        main_content_layout = QVBoxLayout(main_content)
        main_content_layout.setContentsMargins(15, 15, 15, 15)
        main_content_layout.addWidget(self.stacked_widget)

        self.pages = pages

        return main_content

    def _connect_navigation(self):
        navigation_map = {
            'autoclicker': self.pages['autoclicker'],
            'macro': self.pages['macro'],
            'settings': self.pages['settings'],
            'about': self.pages['about']
        }

        for key, page in navigation_map.items():
            self.sidebar_buttons[key].clicked.connect(
                lambda checked, p=page: self.stacked_widget.setCurrentWidget(p)
            )

    def _create_autoclicker_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        frames = [
            self._create_click_interval_frame(),
            self._create_click_options_frame(),
            self._create_position_and_repeat_frames(),
            self._create_control_buttons()
        ]

        for i, frame in enumerate(frames[:-2]):
            layout.addWidget(frame)
            layout.addSpacing(20)

        layout.addLayout(frames[2])
        layout.addSpacing(20)
        layout.addStretch()
        layout.addSpacing(15)

        layout.addLayout(frames[3])

        return widget

    def _create_click_interval_frame(self):
        frame = self._create_styled_frame(500, 100)
        layout = QVBoxLayout(frame)

        title = QLabel("Click Interval:")
        title.setStyleSheet("color: white;")
        layout.addWidget(title)
        layout.addSpacing(10)

        time_layout = self._create_time_inputs()
        layout.addLayout(time_layout)
        layout.addStretch()

        return frame

    def _create_time_inputs(self):
        layout = QHBoxLayout()
        layout.setSpacing(8)

        spinbox_style = self._get_spinbox_style()
        time_units = [
            ("Millisecond:", 0, 1000),
            ("Second:", 0, 60),
            ("Minute:", 0, 60),
            ("Hour:", 0, 24)
        ]

        for label_text, min_val, max_val in time_units:
            label = QLabel(label_text)
            label.setStyleSheet("color: white;")
            
            spinbox = QSpinBox()
            spinbox.setRange(min_val, max_val)
            spinbox.setFixedWidth(60)
            spinbox.setStyleSheet(spinbox_style)
            
            layout.addWidget(label)
            layout.addWidget(spinbox)

        return layout

    def _create_click_options_frame(self):
        frame = self._create_styled_frame(500, 100)
        layout = QVBoxLayout(frame)

        title = QLabel("Click Options:")
        title.setStyleSheet("color: white;")
        layout.addWidget(title)
        layout.addSpacing(10)

        options_layout = self._create_click_option_controls()
        layout.addLayout(options_layout)
        layout.addStretch()

        return frame

    def _create_click_option_controls(self):
        layout = QHBoxLayout()
        layout.setSpacing(10)

        combobox_style = self._get_combobox_style()

        mouse_button_dropdown = QComboBox()
        mouse_button_dropdown.addItems(["Left", "Right", "Middle"])
        mouse_button_dropdown.setStyleSheet(combobox_style)

        click_type_dropdown = QComboBox()
        click_type_dropdown.addItems(["Single", "Double"])
        click_type_dropdown.setStyleSheet(combobox_style)

        hold_control = self._create_hold_duration_control()

        layout.addWidget(mouse_button_dropdown)
        layout.addWidget(click_type_dropdown)
        layout.addLayout(hold_control)

        return layout

    def _create_hold_duration_control(self):
        layout = QHBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("Hold Duration (s):")
        label.setStyleSheet("color: white;")

        spinbox = QSpinBox()
        spinbox.setRange(0, 60)
        spinbox.setFixedWidth(60)
        spinbox.setStyleSheet(self._get_spinbox_style())

        layout.addWidget(label)
        layout.addWidget(spinbox)

        return layout

    def _create_position_and_repeat_frames(self):
        layout = QHBoxLayout()
        
        position_frame = self._create_cursor_position_frame()
        repeat_frame = self._create_repeat_options_frame()
        
        layout.addWidget(position_frame)
        layout.addWidget(repeat_frame)
        
        return layout

    def _create_cursor_position_frame(self):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("background-color: #3A3A3A; border-radius: 10px;")
        frame.setMinimumHeight(100)
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        title = QLabel("Cursor Position:")
        title.setStyleSheet("color: white;")
        layout.addWidget(title)

        current_checkbox = QCheckBox("Current")
        current_checkbox.setStyleSheet("color: white;")
        layout.addWidget(current_checkbox)

        custom_layout = self._create_custom_position_controls()
        layout.addLayout(custom_layout)

        return frame

    def _create_custom_position_controls(self):
        layout = QHBoxLayout()
        layout.setSpacing(12)

        custom_checkbox = QCheckBox("Custom")
        custom_checkbox.setStyleSheet("color: white;")

        x_layout = self._create_coordinate_input("X:", 0, 9999)
        
        y_layout = self._create_coordinate_input("Y:", 0, 9999)

        layout.addWidget(custom_checkbox)
        layout.addLayout(x_layout)
        layout.addLayout(y_layout)
        layout.addStretch()

        return layout

    def _create_coordinate_input(self, label_text, min_val, max_val):
        layout = QHBoxLayout()
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(label_text)
        label.setStyleSheet("color: white;")

        spinbox = QSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setFixedWidth(60)
        spinbox.setStyleSheet(self._get_spinbox_style())

        layout.addWidget(label)
        layout.addWidget(spinbox)

        return layout

    def _create_repeat_options_frame(self):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("background-color: #3A3A3A; border-radius: 10px;")
        frame.setMinimumHeight(100)
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        title = QLabel("Repeat Options:")
        title.setStyleSheet("color: white;")
        layout.addWidget(title)

        toggle_layout = QHBoxLayout()
        toggle_checkbox = QCheckBox("Toggle")
        toggle_checkbox.setStyleSheet("color: white;")
        toggle_layout.addWidget(toggle_checkbox)
        toggle_layout.addStretch()
        layout.addLayout(toggle_layout)

        repeat_layout = self._create_repeat_count_control()
        layout.addLayout(repeat_layout)

        return frame

    def _create_repeat_count_control(self):
        layout = QHBoxLayout()
        layout.setSpacing(10)

        repeat_checkbox = QCheckBox("Repeat")
        repeat_checkbox.setStyleSheet("color: white;")

        repeat_spinbox = QSpinBox()
        repeat_spinbox.setRange(1, 9999)
        repeat_spinbox.setFixedWidth(60)
        repeat_spinbox.setStyleSheet(self._get_spinbox_style())

        layout.addWidget(repeat_checkbox)
        layout.addWidget(repeat_spinbox)
        layout.addStretch()

        return layout

    def _create_control_buttons(self):
        layout = QHBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button_style = self._get_button_style()
        buttons = ["Start", "Stop"]

        for button_text in buttons:
            button = QPushButton(button_text)
            button.setFixedWidth(200)
            button.setStyleSheet(button_style)
            layout.addWidget(button)

        return layout

    def _create_macro_page(self):
        return self._create_placeholder_page("Macro Page - Under Construction")

    def _create_settings_page(self):
        return self._create_placeholder_page("Settings Page - Under Construction")

    def _create_about_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        content_items = [
            ("AutoClicker GUI", "font-size: 20px; font-weight: bold; color: white;"),
            ("A lightweight tool for automating clicks and macros.", "color: white;"),
            ("Developed by Lethios", "color: white;"),
            ("<a href='https://github.com/Lethios/autoclicker-gui' "
             "style='color:#1197DC; text-decoration:none;'>GitHub Repository</a>", None),
            ("This project is licensed under the MIT License.", "color: white;")
        ]

        for i, (text, style) in enumerate(content_items):
            label = QLabel(text)
            
            if style:
                label.setStyleSheet(style)
            
            if "github.com" in text.lower():
                label.setOpenExternalLinks(True)
            
            layout.addWidget(label)
            
            if i in [0, 1]:
                layout.addSpacing(10)

        layout.addStretch()

        return widget

    def _create_placeholder_page(self, text):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        label = QLabel(text)
        label.setStyleSheet("color: white; font-size: 16px;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        return widget

    def _create_styled_frame(self, width=None, height=None):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("background-color: #3A3A3A; border-radius: 10px;")
        
        if width and height:
            frame.setFixedSize(width, height)
        
        return frame

    @staticmethod
    def _get_button_style():
        return """
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

    @staticmethod
    def _get_spinbox_style():
        return """
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

    @staticmethod
    def _get_combobox_style():
        return """
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


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
