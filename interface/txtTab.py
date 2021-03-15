from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

class TextEditor(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.editor = QPlainTextEdit()  # Could also use a QTextEdit and set self.editor.setAcceptRichText(False)
        self.tools = QGroupBox("Tools :")
        toolsBoxLayout = QVBoxLayout()
        
        ##
        self.infos = QGroupBox("Statistical Infos :")
        infoBoxLayout = QVBoxLayout()

        nbrWords = QLabel("<b>Number of distinct words :</b>  <i>12</i>")
        infoBoxLayout.addWidget(nbrWords)

        nbrEdges = QLabel("<b>Number of edges found :</b>  <i>6</i>")
        infoBoxLayout.addWidget(nbrEdges)

        self.infos.setLayout(infoBoxLayout)
        toolsBoxLayout.addWidget(self.infos)

        ##
        self.predictors = QGroupBox("Predictors :")
        predictBoxLayout = QVBoxLayout()
        
        choiceLabel = QLabel("<b>Choose a word :</b>")
        predictBoxLayout.addWidget(choiceLabel)

        searchBar = QLineEdit()
        predictBoxLayout.addWidget(searchBar)

        resultLabel = QLabel("<b>Results :</b>")
        predictBoxLayout.addWidget(resultLabel)
        
        resultList = QListWidget()
        predictBoxLayout.addWidget(resultList)
        
        self.predictors.setLayout(predictBoxLayout)
        toolsBoxLayout.addWidget(self.predictors)

        ##
        self.tools.setLayout(toolsBoxLayout)

        self.tl = QGridLayout()
        self.tl.addWidget(self.tools, 0, 0, 2, 2)
        self.tl.addWidget(self.editor, 0, 3, 1, 1)

        # Setup the QTextEdit editor configuration
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)
