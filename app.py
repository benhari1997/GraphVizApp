from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from interface.mainWindow import TableWidget
from tools.txtToVtk import saveNetwork 
import os
import sys

class App(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.title = 'PyQt5 App - Graph visualisation'
        self.left = 0
        self.top = 0
        self.width = 1400
        self.height = 900
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.path = "//filer-2/Students/abdessalam.benhari/Bureau/notepad/notepad/mytext.txt"
        
        self.table_widget = TableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        self.editor = self.table_widget.tab1.editor  # Could also use a QTextEdit and set self.editor.setAcceptRichText(False)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        
        fileMenu = self.menuBar().addMenu("&File")

        openFAction = QAction(QIcon(os.path.join('data/images', 'blue-folder-open-document.png')), "Open file...", self)
        openFAction.setStatusTip("Open file")
        openFAction.triggered.connect(self.fileOpen)
        fileMenu.addAction(openFAction)

        saveFAction = QAction(QIcon(os.path.join('data/images', 'disk.png')), "Save", self)
        saveFAction.setStatusTip("Save current page")
        saveFAction.triggered.connect(self.fileSave)
        fileMenu.addAction(saveFAction)

        saveAsFAction = QAction(QIcon(os.path.join('data/images', 'disk--pencil.png')), "Save As...", self)
        saveAsFAction.setStatusTip("Save current page to specified file")
        saveAsFAction.triggered.connect(self.fileSaveAs)
        fileMenu.addAction(saveAsFAction)

        visMenu = self.menuBar().addMenu("&Visualisation")

        exportAction = QAction(QIcon(os.path.join('data/images', 'arrow-curve.png')), "Export..", self)
        exportAction.setStatusTip("Export visualisation as vtp file")
        exportAction.triggered.connect(saveNetwork)
        visMenu.addAction(exportAction)

        resetAction = QAction(QIcon(os.path.join('data/images', 'arrow-continue.png')), "Reset..", self)
        resetAction.setStatusTip("Reselt all changes")
        resetAction.triggered.connect(self.editor.redo)
        visMenu.addAction(resetAction)

        self.show()

    def dialogCritical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def fileOpen(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt)")
        if path:
            try:
                with open(path, 'r') as f:
                    text = f.read()

            except Exception as e:
                self.dialogCritical(str(e))

            else:
                self.path = path
                self.editor.setPlainText(text)

    def fileSave(self):
        if self.path is None:
            # If we do not have a path, we need to use Save As.
            return self.file_saveas()

        self._save_to_path(self.path)

    def fileSaveAs(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt)")

        if not path:
            # If dialog is cancelled, will return ''
            return

        self._save_to_path(path)

    def _save_to_path(self, path):
        text = self.editor.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    app.exec_()