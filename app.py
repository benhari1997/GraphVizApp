import vtk

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

from interface.mainWindow import TableWidget

import os
import sys

class App(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        # Esthetics
        self.title = 'VTK - Graph visualisation'
        self.left = 0
        self.top = 0
        self.width = 1400
        self.height = 900
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('data/images/main-icon.png'))
        self.setGeometry(self.left, self.top, self.width, self.height)


        # Default prameters 
        self.path = "data/docs/mytext.txt"
        self.networkData = None
        
        # setting the central widget (the main window)
        self.tableWidget = TableWidget(self)
        self.setCentralWidget(self.tableWidget)
        
        self.editor = self.tableWidget.tab1.editor 

        # Menubar settings
        # == File bar
        fileMenu = self.menuBar().addMenu("&File")

        ## open file
        openFAction = QAction(
            QIcon(
                os.path.join('data/images','blue-folder-open-document.png')
                ),
            "Open file...",self)
        openFAction.setStatusTip("Open file")
        openFAction.triggered.connect(self.fileOpen)
        fileMenu.addAction(openFAction)

        ## save file
        saveFAction = QAction(
            QIcon(
                os.path.join('data/images', 'disk.png')
                ),
            "Save", self)
        saveFAction.setStatusTip("Save current page")
        saveFAction.triggered.connect(self.fileSave)
        fileMenu.addAction(saveFAction)

        ## Save file with specific name
        saveAsFAction = QAction(
            QIcon(
                os.path.join('data/images', 'disk--pencil.png')
                ),
            "Save As...", self)
        saveAsFAction.setStatusTip("Save current page to specified file")
        saveAsFAction.triggered.connect(self.fileSaveAs)
        fileMenu.addAction(saveAsFAction)
        # == Visualisation bar
        visMenu = self.menuBar().addMenu("&Visualisation")

        ## export visualisation
        exportAction = QAction(
            QIcon(
                os.path.join('data/images', 'arrow-curve.png')
                ),
            "Export..", self)
        exportAction.setStatusTip("Export visualisation as vtp file")
        exportAction.triggered.connect(self.saveNetwork)
        visMenu.addAction(exportAction)

        ## reset visualisation
        resetAction = QAction(
            QIcon(
                os.path.join('data/images', 'arrow-continue.png')
                ),
                "Reset..", self)
        resetAction.setStatusTip("Reselt all changes")
        resetAction.triggered.connect(self.editor.redo)
        visMenu.addAction(resetAction)

        # Display app 
        self.show()

    #
    # Main window trigger functions :
    #

    def dialogCritical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def fileOpen(self):
        """ Gets the path of the chosen file
            to open and displays its text.
        """
        path, _ = QFileDialog.getOpenFileName(
                    self, "Open file", "", "Text documents (*.txt)")
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
        """ Saves the file if existent and
            runs the saveAs function if not.
        """
        if self.path is None:
            # uses save as if the path doesn t exist.
            return self.fileSaveAs()

        self._save_to_path(self.path)

    def fileSaveAs(self):
        """ Allows the user to choose a
            path where to save the file.
        """
        path, _ = QFileDialog.getSaveFileName(
                    self, "Save file", "", "Text documents (*.txt)")

        if not path:
            # If dialog is cancelled, will return ''
            return

        self._save_to_path(path)

    def _save_to_path(self, path):
        """ Saves the file in the chosen
            path.
        """
        text = self.editor.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialogCritical(str(e))

        else:
            self.path = path

    def saveNetwork(self):
        """ Saves the network as a ".vtp"
            for further analysis (Exp.Paraview).
        """
        if self.networkData:
            # a default name
            net = "network"

            # setting a vtk writer
            writer = vtk.vtkXMLPolyDataWriter()
            writer.SetFileName('data/networks/'+net+'.vtp')
            writer.SetInputData(self.networkData)

            # writing on file
            writer.Write()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #app.setStyle('Fusion')
    window = App()
    app.exec_()