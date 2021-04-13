from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox,QFileDialog
from PIL import ImageQt
from PIL import Image as imagePIL
from App import *
def browseImage(ob_lb_image):
	fname = QFileDialog.getOpenFileName(ui,"Opent File image","../Watermark_With_DWT/pyqt5","Image files (*.jpg)")
	imagePath = fname[0]
	pixmap = QPixmap(imagePath)
	ob_lb_image.setPixmap(pixmap)
	ob_lb_image.setToolTip(imagePath)
##save file
def saveImage():
	buttonReply = QMessageBox.question(ui, 'Thông báo', "Bạn có muốn lưu lại?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
	if buttonReply == QMessageBox.Yes:
		fname = QFileDialog.getSaveFileName(ui, 'Save File image',"../Watermark_With_DWT/pyqt5","Image files (*.jpg)")
		if fname[0] != "":
			imgFile = Image.open("temp.jpg")
			imgFile.save(fname[0])
			print("Save success!!")
			QMessageBox.question(ui, 'Thông Báo', "Đã lưu lại", QMessageBox.Close, QMessageBox.Close)
##convert image
def convert_image(img,mode):
	img = img.convert(mode,palette=Image.ADAPTIVE)
	return img
##process image
def process_image(): 
	img_ori=None
	img_mark=None
	imgPath = ui.lb_original.toolTip()
	if imgPath != "":
		img_ori = cv2.imread(imgPath)
	imgPath =ui.lb_mark.toolTip()
	if imgPath != "":
		img_mark = cv2.imread(imgPath,0)
	return img_ori,img_mark
##bottom embedding clicked
def btn_embedding():
	QMessageBox.information(ui, "Thông Báo","bấm OK để thực hiện nhúng và đợi trong giây lát!")
	img_ori,img_mark = process_image()
	if img_ori.any()!=None and img_mark.any()!=None:	
		Watermarking_DCT(img_ori, img_mark)
		pixmap = QPixmap("watermarked.jpg")
		ui.lb_watermark.setPixmap(QPixmap(pixmap))
		QMessageBox.question(ui, 'Thông Báo', "Đã nhúng thành công!!", QMessageBox.Close, QMessageBox.Close)
		
	else:
		QMessageBox.question(ui, 'Cảnh Báo', "Không thể nhúng. Xin kiểm tra lại dữ liệu đầu vào!!", QMessageBox.Close, QMessageBox.Close)
##bottom exacting clicked
def btn_exacting():
	QMessageBox.information(ui, "Thông Báo","bấm OK để thực hiện tách và đợi trong giây lát!")
	imgPath = "watermarked.jpg"
	
	img_mark = cv2.imread(imgPath)
	if img_mark.any()!=None:
		#image = imagePIL.fromarray()
		Extract_DCT(img_mark)
		#image.save("temp.jpg")
		pixmap = QPixmap("signature.jpg")
		ui.lb_watermark_2.setPixmap(pixmap)
		QMessageBox.question(ui, 'Thông Báo', "Tách thành công!!", QMessageBox.Close, QMessageBox.Close)
	else:
		QMessageBox.question(ui, 'Cảnh Báo', "Không thể tách. Xin kiểm tra lại dữ liệu đầu vào!!", QMessageBox.Close, QMessageBox.Close)
app = QtWidgets.QApplication([])
ui = uic.loadUi("UI_DCT.ui")
##append / running here
ui.btn_image_ori.clicked.connect(lambda: browseImage(ui.lb_original))
ui.btn_image_mark.clicked.connect(lambda: browseImage(ui.lb_mark))
ui.btn_embedding.clicked.connect(btn_embedding)
ui.btn_exacting.clicked.connect(btn_exacting)
ui.btn_save.clicked.connect(saveImage)
##end code
ui.show()
app.exec()
