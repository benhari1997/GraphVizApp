import gensim 

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

class TextEditor(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.editor = QPlainTextEdit()  
        self.tools = QGroupBox("Tools :")
        toolsBoxLayout = QVBoxLayout()
        
        # create informations group
        self.infos = QGroupBox("Additionnal Infos :")
        infoBoxLayout = QVBoxLayout()

        embMethod = QLabel("<b>Embedding method : Word2Vec</b>")
        infoBoxLayout.addWidget(embMethod)

        lookUpTable = QLabel("<b>Prediction : Synonyms </b>")
        infoBoxLayout.addWidget(lookUpTable)

        self.infos.setLayout(infoBoxLayout)
        toolsBoxLayout.addWidget(self.infos)

        # create predictions group
        self.predictors = QGroupBox("Predictors :")
        synBoxLayout = QVBoxLayout()
        
        choiceLabel = QLabel("<b>Choose a word :</b>")
        synBoxLayout.addWidget(choiceLabel)

        self.searchBar = QLineEdit()
        synBoxLayout.addWidget(self.searchBar)

        self.searchSynonyms = QPushButton("Search synonyms:")
        synBoxLayout.addWidget(self.searchSynonyms)
        self.searchSynonyms.clicked.connect(self.setSynonyms)

        self.resultLabel = QLabel("<b>Results :</b>")
        synBoxLayout.addWidget(self.resultLabel)
        
        self.resultList = QListWidget()
        synBoxLayout.addWidget(self.resultList)
        self.resultList.itemClicked.connect(self.getSynonym)

        self.predictors.setLayout(synBoxLayout)
        toolsBoxLayout.addWidget(self.predictors)

        # setting layout
        self.tools.setLayout(toolsBoxLayout)

        self.tl = QGridLayout()
        self.tl.addWidget(self.tools, 0, 0, 2, 2)
        self.tl.addWidget(self.editor, 0, 3, 1, 1)

        # Setting up the QTextEdit editor configuration
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)
    
    #
    # Text Tab trigger functions :
    #

    def setSynonyms(self):
        """ Updates the results list with
            the chosen word's synonyms.
        """
        # load the word2vec pre-trained model
        modelPath = "ML/models/word2vecModel"
        model = gensim.models.Word2Vec.load(modelPath)

        # get synonym results 
        chosenWord = self.searchBar.text()
        results = list()
        try:
            results = model.wv.most_similar(positive=chosenWord, topn=10)
        except:
            None

        # update the results list
        self.resultList.clear()
        if results:
            for result in results:
                self.resultList.addItem(
                    "\032 {0}  ::> {1}".format(result[0], result[1]))

    def getSynonym(self):
        """ writes the selected synonym at
            the end of the current text.
        """
        # get selected synonym
        synonym = self.resultList.selectedItems()[0].text()

        # add selected synonym to text
        self.editor.appendPlainText(' ' + synonym.split(" ",2)[1])

