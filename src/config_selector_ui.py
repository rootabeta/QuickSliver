from PyQt5.QtWidgets import (
    QComboBox,
    QMainWindow,
    QApplication,
    QWidget,
    QGridLayout,
    QPushButton,
)
from PyQt5.QtGui import QIcon


class ConfigSelector(QMainWindow):
    def __init__(self, configs):
        super().__init__()

        self.setWindowTitle("Select config")

        self.selector = QComboBox()

        confirm = QPushButton("Select")
        confirm.clicked.connect(self.makeSelection)

        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.closeWindow)

        for config_name in configs.keys():
            self.selector.addItem(config_name)

        layout = QGridLayout()

        layout.addWidget(self.selector, 0, 0, 0, 2)
        layout.addWidget(cancel, 1, 0)
        layout.addWidget(confirm, 1, 1)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def makeSelection(self, _):
        # print(self.selector.currentText()) # Config chosen
        self.close()

    def closeWindow(self, _):
        self.selector.clear()
        self.close()


def selectConfig(configs):
    app = QApplication([])
    configSelector = ConfigSelector(configs)
    configSelector.show()
    app.exec_()

    # Return the item that was selected when the app was closed
    return configSelector.selector.currentText()
