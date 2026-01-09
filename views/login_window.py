from views.dashboard_window import DashboardWindow
from PyQt5 import QtWidgets
from controllers.auth_controller import AuthController


class LoginWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Kütüphane Giriş")
		self.controller = AuthController()
		self._build_ui()

	def _build_ui(self):
		central = QtWidgets.QWidget(self)
		layout = QtWidgets.QVBoxLayout(central)

		form = QtWidgets.QFormLayout()
		self.username_input = QtWidgets.QLineEdit()
		self.password_input = QtWidgets.QLineEdit()
		self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
		form.addRow("Kullanıcı Adı", self.username_input)
		form.addRow("Şifre", self.password_input)

		self.login_btn = QtWidgets.QPushButton("Giriş")
		self.login_btn.clicked.connect(self.on_login)

		layout.addLayout(form)
		layout.addWidget(self.login_btn)

		self.setCentralWidget(central)

	def on_login(self):
		username = self.username_input.text().strip()
		password = self.password_input.text()

		ok, message = self.controller.login(username, password)

		if ok:
			QtWidgets.QMessageBox.information(self, "Başarılı", message)
			
			self.dashboard = DashboardWindow(username)
			self.dashboard.show()
			self.close()

		else:
			QtWidgets.QMessageBox.warning(self, "Hata", message)
