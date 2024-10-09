# coding:utf-8
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

# Ensure the 'cfg' module is properly configured and 'MainWindow' is defined.
# Assuming they are coming from 'app' module.
from app import cfg
from app import MainWindow

if __name__ == "__main__":
    # Enable DPI scaling based on configuration
    dpi_scale = cfg.get("dpiScale", "Auto")  # Default to 'Auto' if dpiScale is missing
    
    if dpi_scale == "Auto":
        # Set high DPI scaling policy to pass through the scaling factor
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    else:
        # If manual scaling is specified, ensure the value is numeric
        try:
            os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"  # Disable automatic scaling
            os.environ["QT_SCALE_FACTOR"] = str(float(dpi_scale))  # Ensure it's a valid number
        except ValueError:
            # Handle incorrect dpiScale values by falling back to 'Auto' behavior
            print("Invalid dpiScale value in config, falling back to Auto scaling.")
            QApplication.setHighDpiScaleFactorRoundingPolicy(
                Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
            )
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    # Enable high DPI pixmaps for sharp UI elements
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # Create the QApplication object
    app = QApplication(sys.argv)
    
    # Disable creation of native widget siblings
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    # Create the main window
    w = MainWindow()
    w.show()

    # Execute the application and exit cleanly
    sys.exit(app.exec_())
