import sys

from PyQt5 import QtWidgets, QtPrintSupport, QtGui, QtCore, QtWinExtras


class Window(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.resize(400, 350)
		self.setWindowTitle('Печать')
		self.vbox = QtWidgets.QVBoxLayout(self)
		self.textedit = QtWidgets.QTextEdit()
		self.hbox = QtWidgets.QHBoxLayout()
		self.btn1 = QtWidgets.QPushButton('&Загрузить')
		self.btn2 = QtWidgets.QPushButton('&Печать')
		self.hbox.addWidget(self.btn1)
		self.hbox.addWidget(self.btn2)
		self.vbox.addWidget(self.textedit)
		self.vbox.addLayout(self.hbox)

		self.btn1.clicked.connect(self.load_data)
		self.btn2.clicked.connect(self.print_text)
		self.printer = QtPrintSupport.QPrinter()
		self.printer.setOutputFileName("output.pdf")
		self.printer.setPageOrientation(QtGui.QPageLayout.Orientation.Landscape)

		jumpList = QtWinExtras.QWinJumpList(parent=self)
		jumpList.clear()
		recent = jumpList.recent()
		item1 = QtWinExtras.QWinJumpListItem(
			QtWinExtras.QWinJumpListItem.Link
		)
		item1.setFilePath(r"C:\Windows\notepad.exe")
		item1.setTitle('Лицензия Python')
		item1.setArguments(
			[r"C:\Users\Сергей\AppData\Local\Programs\Python\Python311\LICENSE.txt"]
		)
		recent.addItem(item1)
		recent.setVisible(True)
		frequent = jumpList.frequent()
		frequent.addLink(
			"Новости Python",
			r"C:\Users\Сергей\AppData\Local\Programs\Python\Python311\NEWS.txt"
		)
		frequent.setVisible(True)
		tasks = jumpList.tasks()
		tasks.addLink("Блокнот", r"C:\Windows\notepad.exe")
		tasks.addSeparator()
		tasks.addLink("Write", r"C:\Windows\write.exe")
		tasks.setVisible(True)
		otherCat = QtWinExtras.QWinJumpListCategory()
		otherCat.setTitle("Дополнительно")
		otherCat.addLink(
			"Python Shell",
			r"C:\Users\Сергей\AppData\Local\Programs\Python\Python311\python.exe"
		)
		otherCat.setVisible(True)
		jumpList.addCategory(otherCat)

		self.settings = QtCore.QSettings("Print Homework", "PrintApp")
		self.load_settings()

	def load_settings(self):
		if self.settings.contains("Окно/Местоположение"):
			self.setGeometry(self.settings.value("Окно/Местоположение"))
		if self.settings.contains("Поле/Текст"):
			self.textedit.setText(self.settings.value("Поле/Текст"))

	def save_settings(self):
		self.settings.beginGroup('Поле')
		self.settings.setValue('Текст', self.textedit.toPlainText())
		self.settings.endGroup()

		self.settings.beginGroup("Окно")
		self.settings.setValue("Местоположение", self.geometry())
		self.settings.endGroup()

	def closeEvent(self, evt: QtGui.QCloseEvent):
		self.save_settings()
		evt.accept()


	def load_data(self):
		file_dialog = QtWidgets.QFileDialog()
		file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.AnyFile)
		file_dialog.setNameFilter('Текстовый документ, (*.txt)')
		file_dialog.exec()
		file = file_dialog.selectedFiles()[0]
		with open(file) as f:
			text = f.read()
		self.textedit.setText(text)

	def print_text(self):
		print_dialog = QtPrintSupport.QPrintDialog(self.printer)
		print_dialog.setOption(QtPrintSupport.QPrintDialog.PrintDialogOption.PrintSelection)
		painter = QtGui.QPainter()
		painter.begin(self.printer)
		painter.drawText(10, self.printer.height() // 2 - 100, self.printer.width() - 20, 50,
		                 QtCore.Qt.AlignCenter | QtCore.Qt.TextDontClip,
		                 self.textedit.toPlainText())
		painter.end()


if __name__ == '__main__':
	app = QtWidgets.QApplication([])
	window = Window()
	window.show()
	sys.exit(app.exec_())

