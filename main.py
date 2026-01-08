import sys
from PyQt5 import QtWidgets

from views.login_window import LoginWindow


def load_stylesheet(app: QtWidgets.QApplication):
	try:
		with open("assets/style.qss", "r", encoding="utf-8") as f:
			app.setStyleSheet(f.read())
	except Exception:
		# Style is optional; ignore if missing
		pass


def main():
	app = QtWidgets.QApplication(sys.argv)
	load_stylesheet(app)
	win = LoginWindow()
	win.show()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()
