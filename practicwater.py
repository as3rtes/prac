import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QSlider,QProgressBar, QPushButton, QLCDNumber,QTextEdit)
from PySide6.QtCore import Qt, QTimer, QTime


class TankControl(QWidget):
    def __init__(self):
        super().__init__()
        self.current_level = 0.0
        self.init_ui()
        self.connect_signals()
        self.setup_timer()

    def init_ui(self):
        self.setWindowTitle("Пульт управления резервуаром")
        self.resize(700, 800)

        self.title_label = QLabel("РЕЗЕРВУАР A-1")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.status_label = QLabel("Статус: НОРМА")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(
            "font-size: 14px; padding: 6px; background-color: #27ae60; "
            "color: white; border-radius: 4px;"
        )
        slider_label = QLabel("Клапан подачи:")
        self.input_slider = QSlider(Qt.Horizontal)
        self.input_slider.setRange(0, 100)
        self.input_slider.setValue(0)


        level_label = QLabel("Уровень:")
        self.level_bar = QProgressBar()
        self.level_bar.setRange(0, 100)
        self.level_bar.setValue(0)
        self.level_bar.setMaximumHeight(20)



        self.lcd_display = QLCDNumber()
        self.lcd_display.setDigitCount(4)
        self.lcd_display.setMinimumHeight(20)





        self.drain_btn = QPushButton("Сброс")
        self.reset_btn = QPushButton("Аварийный сброс")
        self.reset_btn.setStyleSheet(
            "background-color: #e74c3c; color: white; font-weight: bold; padding: 8px;"
        )

        log_label = QLabel("Журнал событий:")
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(120)


        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.status_label)


        slider_row = QHBoxLayout()
        slider_row.addWidget(slider_label)
        slider_row.addWidget(self.input_slider)
        main_layout.addLayout(slider_row)

        level_row = QHBoxLayout()
        level_row.addWidget(level_label)
        level_row.addWidget(self.level_bar)
        main_layout.addLayout(level_row)

        main_layout.addWidget(self.lcd_display)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.drain_btn)
        btn_row.addWidget(self.reset_btn)
        main_layout.addLayout(btn_row)

        main_layout.addWidget(log_label)
        main_layout.addWidget(self.log_text)

        self.setLayout(main_layout)

    def connect_signals(self):

        self.drain_btn.clicked.connect(self.drain_tank)
        self.reset_btn.clicked.connect(self.emergency_reset)

    def setup_timer(self):
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_level)
        self.timer.start()
        self.log_event("Система запущена")

    def update_level(self):
        inflow = self.input_slider.value() * 0.3
        leak = 1.0
        self.current_level += (inflow - leak) * 0.1

        if self.current_level < 0:
            self.current_level = 0
        if self.current_level > 100:
            self.current_level = 100

        level_int = int(self.current_level)
        self.level_bar.setValue(level_int)
        self.lcd_display.display(level_int)

        self.update_alarm_status(level_int)

    def update_alarm_status(self, level):
        old_level = getattr(self, '_last_alarm_level', 0)

        if level > 90:
            self.status_label.setText("КРИТИЧЕСКИЙ УРОВЕНЬ")
            self.status_label.setStyleSheet(
                "font-size: 14px; padding: 6px; background-color: #e74c3c; "
                "color: white; font-weight: bold; border-radius: 4px;"
            )
            self.level_bar.setStyleSheet(
                "QProgressBar::chunk { background-color: #e74c3c; }"
            )
        elif level > 80 and level < 91:
            self.status_label.setText("ВНИМАНИЕ: высокий уровень")
            self.status_label.setStyleSheet(
                "font-size: 14px; padding: 6px; background-color: #f39c12; "
                "color: white; border-radius: 4px;"
            )
            self.level_bar.setStyleSheet(
                "QProgressBar::chunk { background-color: #f39c12; }"
            )
        else:
            self.status_label.setText("Статус: НОРМА")
            self.status_label.setStyleSheet(
                "font-size: 14px; padding: 6px; background-color: #27ae60; "
                "color: white; border-radius: 4px;"
            )
            self.level_bar.setStyleSheet("")

        if old_level <= 80 < level:
            self.log_event("Уровень превысил 80%")
        elif old_level <= 90 < level:
            self.log_event("КРИТИЧЕСКИЙ УРОВЕНЬ! 90%")
        self._last_alarm_level = level

    def drain_tank(self):
        self.input_slider.setValue(0)
        self.log_event("Оператор нажал 'Сброс'")

    def emergency_reset(self):
        self.input_slider.setValue(0)
        self.level_bar.setValue(0)
        self.lcd_display.display(0)
        self.current_level = 0.0
        self.log_event("АВАРИЙНЫЙ СБРОС активирован")

    def log_event(self, message):
        time_str = QTime.currentTime().toString("hh:mm:ss")
        self.log_text.append(f"[{time_str}] {message}")

    def closeEvent(self, event):
        self.log_event("Система остановлена")
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = TankControl()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
