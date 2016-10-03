import sys
import morse
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
#from PyQt5.QObject import QClipboard



class mainMorse(QMainWindow):

	shittymorse = morse.Morse()
	stringbuffer = ""
	morsebuffer = ''
	strBox = None
	morseBox = None

	def __init__(self):
		super(mainMorse, self).__init__()
		self.initUI()


	def initUI(self):

		#Creates main window
		self.setWindowTitle('Morse Code Entry')
		self.setWindowIcon(QIcon('morseIcon.jpg'))
		#self.setWindowFlags(Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_NoSystemBackground, True)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.center()
		self.actions()
		self.createMenus()
		guideBox=self.guide()

		#Quit Button
		qbtn = QPushButton('Quit', self)
		qbtn.setToolTip('Push to <b>Quit</b>')
		qbtn.clicked.connect(QCoreApplication.instance().quit)
		qbtn.resize(100,100)
		qbtn.move(0, 75)

		mbtn = QPushButton('Minimize', self)
		mbtn.setToolTip('Push to <b>Minimize</b> and keep clipboard')
		mbtn.clicked.connect(self.minimize)
		mbtn.resize(100,100)
		mbtn.move(0, 75)

		fbtn = QPushButton('Fullscreen', self)
		fbtn.setToolTip('Push to return to <b>fullscreen</b>')
		fbtn.clicked.connect(self.full)
		fbtn.resize(100,100)
		fbtn.move(0, 75)

		cbtn = QPushButton('Clear', self)
		cbtn.setToolTip('Push to return to <b>clear</b> text')
		cbtn.clicked.connect(self.clear)
		cbtn.resize(100,100)
		cbtn.move(0, 75)


		self.strBox = QLineEdit()
		self.strBox.setDragEnabled(True)
		self.strBox.setReadOnly(True)
		#self.strBox.move(0,0)
		self.strBox.setFrame(True)
		self.strBox.setStyleSheet("background-color: maroon; color: white; font-size: 40px")
		

		self.morseBox = QLineEdit()
		self.morseBox.setDragEnabled(True)
		self.morseBox.setReadOnly(True)
		#self.morseBox.move(50,50)
		self.morseBox.setFrame(True)
		self.morseBox.setStyleSheet("background-color: maroon; color: white; font-size: 40px")
		

		layout = QHBoxLayout()
		layout.addWidget(self.morseBox)
		layout.addWidget(self.strBox)
		layout.addWidget(mbtn)
		layout.addWidget(fbtn)
		layout.addWidget(cbtn)
		layout.addWidget(qbtn)
		layout.addWidget(guideBox)
		centralWidget = QWidget()
		centralWidget.setLayout(layout)
		self.setCentralWidget(centralWidget)

		self.show()

	def minimize(self):
		self.setWindowState(Qt.WindowMinimized)

	def full(self):
		self.showFullScreen()

	def guide(self):
		guideBox= QLabel()
		guideBox.setText("<p> A • -</p>"
		"<p> B - • • • </p>" 
		"<p> C - • - •</p>"
		"<p> D - • •</p>"
		"<p> E •</p>"
		"<p> F • • - •</p>"
		"<p> G - - •</p>"
		"<p> H • • • •</p>"
		"<p> I • •</p>"
		"<p> J • - - -</p>"
		"<p> K - • -</p>"
		"<p> L • - • •</p>"
		"<p> M - -</p>"
		"<p> N - •</p>"
		"<p> O - - -</p>"
		"<p> P • - - •</p>"
		"<p> Q - - • - </p>"
		"<p> R • - •</p>"
		"<p> S • • •</p>"
		"<p> T -</p>"
		"<p> U • • -</p>"
		"<p> V • • • -</p>"
		"<p> W • - -</p>"
		"<p> X - • • -</p>"
		"<p> Y - • - -</p>"
		"<p> Z - - • •</p>")
		guideBox.setStyleSheet("background-color: maroon; color: white; font-size: 20px")
		
		return guideBox

	#Dialogue box if close button is clicked
	def closeEvent(self, event):
		reply = QMessageBox.question(self, 'Really?', 
			"Are you sure you want to quit?", QMessageBox.Yes | 
			QMessageBox.No, QMessageBox.No)		
		
		if(reply == QMessageBox.Yes):
			event.accept()
		else:
			event.ignore()

	#Centers Main window, Scales
	def center(self):
		rect = self.frameGeometry()
		screenSize = QDesktopWidget().availableGeometry().center()
		rectScreenSize = QDesktopWidget().availableGeometry()
		self.setGeometry(rectScreenSize)
		rect.moveCenter(screenSize)
		self.move(rect.topLeft())
	

	def createMenus(self):
		#Creates File in menubar
		fileMenu = QMenu('&Exit',self)
		fileMenu.addAction(self.exitAction)

		helpMenu= QMenu('&Help', self)
		helpMenu.addAction(self.overviewAct)
		helpMenu.addAction(self.learnAct)
		helpMenu.addAction(self.usageAct)

		self.menuBar().addMenu(fileMenu)
		self.menuBar().addMenu(helpMenu)

	def actions(self):
		#Exit
		self.exitAction=QAction(QIcon('close.png'),'&Exit',self)
		self.exitAction.setShortcut('Ctrl+Esc')
		self.exitAction.setStatusTip('Exit Application')
		self.exitAction.triggered.connect(qApp.quit)

		self.overviewAct = QAction("&Overview", self, triggered=self.overview)
		self.learnAct = QAction("&Learn Morse Code", self, triggered=self.learn)
		self.usageAct = QAction("&Usage", self, triggered=self.usage)

	def clear(self):
		strlen = len(self.stringbuffer)
		if strlen > 0:
			self.stringbuffer = self.stringbuffer[:-strlen]
			self.strBox.setText(self.stringbuffer)
			clipboard = QApplication.clipboard()
			clipboard.setText(self.stringbuffer)


	def buttons(self):
		pass			

	def mouseReleaseEvent(self, event):
		if event.button() == Qt.LeftButton: #left button is dot
			print('Dot')
			self.shittymorse.incrementDot()
			self.morsebuffer += self.shittymorse.getCurrentSym()
			self.morseBox.setText(self.morsebuffer+'|')
		if event.button() == Qt.RightButton: #right button is dash
			print('Dash')
			self.shittymorse.incrementDash()
			self.morsebuffer += self.shittymorse.getCurrentSym()
			self.morseBox.setText(self.morsebuffer+'|')
		if event.button() == Qt.MidButton:
			strlen = len(self.stringbuffer)
			if strlen > 0:
				self.stringbuffer = self.stringbuffer[:-1]
				self.strBox.setText(self.stringbuffer+'|')
			print('Backspace')

	def wheelEvent(self, event):
		wheelState=event.angleDelta()
		if(wheelState.y()>0):
			self.stringbuffer += ' '
			self.strBox.setText(self.stringbuffer+'|')
			print("Space")
		if(wheelState.y()<0):
			print("End")
			temp = self.shittymorse.getLetter()
			if temp is not None:
				self.stringbuffer +=temp 
				self.shittymorse.clearArray()
				self.morsebuffer = ''
				self.strBox.setText(self.stringbuffer+'|')
				self.morseBox.setText('')
			else:
				self.shittymorse.clearArray()
				self.morsebuffer = ''
				self.morseBox.setText('')
				
			print(str(self.stringbuffer))
			clipboard = QApplication.clipboard()
			clipboard.setText(self.stringbuffer)

	def overview(self):
		QMessageBox.about(self, "Overview", 
		"<p>The Morse Coding Program was designed as an alternative way for individuals to communicate. "
		"It provides a line of communication that only requires moving two fingers. "
		"This program utilizes Morse Code’s binary set of inputs so the amount of physical movement"
		"is minimized while completely bypassing verbal use.</p>")

	def learn(self):
		QMessageBox.about(self,"What is Morse Code?",
	    "<p>Morse code was created by Samuel Morse as a means of communicating across large distances. "
	    "The language that he developed is comprised of dots “•” and dashes “-”. "
	    "Each letter in the English alphabet corresponds to combination of dots and dashes.</p>" 
		"<p>Here is the alphabet:</p>"

		"<p>A • -</p>"
		"<p>B - • • • </p>" 
		"<p>C - • - •</p>"
		"<p>D - • •</p>"
		"<p>E •</p>"
		"<p>F • • - •</p>"
		"<p>G - - •</p>"
		"<p>H • • • •</p>"
		"<p>I • •</p>"
		"<p>J • - - -</p>"
		"<p>K - • -</p>"
		"<p>L • - • •</p>"
		"<p>M - -</p>"
		"<p>N - •</p>"
		"<p>O - - -</p>"
		"<p>P • - - •</p>"
		"<p>Q - - • - </p>"
		"<p>R • - •</p>"
		"<p>S • • •</p>"
		"<p>T -</p>"
		"<p>U • • -</p>"
		"<p>V • • • -</p>"
		"<p>W • - -</p>"
		"<p>X - • • -</p>"
		"<p>Y - • - -</p>"
		"<p>Z - - • •</p>")

	def usage(self):
		QMessageBox.about(self, "How to type:",
		"<p>-To type a Dot we Left Click on our mouse</p>"
		"<p>-To type a Dash we Right Click on our mouse</p>"
		"<p>-To signal the End of Letter we Scroll Down</p>"
		"<p>-To signal the End of word or a space we Scroll Up</p>"

		"<p>Example "
		'Sentence: <b>"hello world"</b> </p>'
		"<p>First find our Morse translation</p>"
		"(h) • • • •    (e)•     (l)• - • •    (l)• - • •    (o)- - - "   
		"<p>(space)</p>"
		"(w)• - -    (o)- - -    (r)• - •    (l)• - • •     (d)- • •</p>"

		"<p>Next we click and scroll our message!</p>"

		"<p>(h) Left Click, Left Click, Left Click, Left Click, Scroll Down</p>"
		"<p>(e) Left Click, Scroll Down</p>"
		"<p>(l) Left Click, Right Click, Left Click, Left Click, Scroll Down</p>"
		"<p>(l) Left Click, Right Click, Left Click, Left Click, Scroll Down</p>"
		"<p>(o) Right Click, Right Click, Right Click, Scroll Down</p>"

		"<p>(space) Scroll Up</p>"

		"<p>(w) Left Click, Right Click, Right Click, Scroll Down</p>"
		"<p>(o) Right Click, Right Click, Right Click, Scroll Down</p>"
		"<p>(r) Left Click, Right Click, Left Click, Scroll Down</p>"
		"<p>(l) Left Click, Right Click, Left Click, Left Click, Scroll Down</p>"
		"<p>(d) Right Click, Left Click, Left Click, Scroll Down</p>")


#Main Calling
if __name__== '__main__':

	app= QApplication(sys.argv)
	mainWin = mainMorse()
	sys.exit(app.exec_())
