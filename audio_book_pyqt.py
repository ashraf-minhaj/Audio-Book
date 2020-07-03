"""Audio Book - PDF reader 

python version: 3.7.1
"""
"""
author: Ashraf Minhaj
mail  : ashraf_minhaj@yahoo.com
site  : ashrafminhajfb.blogspot.com
"""
"""
 STILL SOME BUGS HERE
 1. next page read
 2. stop and start again
 3. pause
"""
import PyQt5
from PyQt5.QtCore import Qt #needed
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon, QImage, QFont
import sys
import pyttsx3
import PyPDF2              #to extract text from pdf file


class Window(QWidget):
    """class that contains everything"""
    def __init__(self):
        super().__init__()
        self.eng = pyttsx3.init()           #initialize pyttsx3
        self.setGeometry(0, 0, 500, 104)  
        
        self.READ = True
        self.ui()

    def ui(self):
        """our UI here"""
        self.setWindowTitle("Audio book - Personal Document Reader")
        self.setStyleSheet("Background-color: black")

        #file path entry edit box
        self.filePathEdit = QLineEdit(self)
        self.filePathEdit.setStyleSheet("background-color: black; color: white")
        self.filePathEdit.setPlaceholderText(" File Name or Path")
        self.filePathEdit.setFont(QFont('SimHei', 10, 10))
        self.filePathEdit.setGeometry(10, 10, 420, 20)

        #file browse button
        self.browse_button = QPushButton(self)
        self.browse_button.setText(" Browse ")
        self.browse_button.setGeometry(435, 10, 60, 20)
        self.browse_button.setStyleSheet("Background-color: black; color: white; border-style: outset; border-width: 1px")
        self.browse_button.setFont(QFont('SimHei', 10, 10))
        self.browse_button.clicked.connect(self.select_file)
        
        #speed_label
        self.speed_label = QLabel(self)
        self.speed_label.setGeometry(10 , 35, 100, 20)
        self.speed_label.setFont(QFont('SimHei', 10, 10))
        self.speed_label.setStyleSheet("background-color: black; color: white")
        self.speed_label.setText("Reading Speed")

        #speed indicator
        self.speed_indicator = QLabel(self)
        self.speed_indicator.setGeometry(370 , 35, 50, 20)
        self.speed_indicator.setFont(QFont('SimHei', 10, 10))
        self.speed_indicator.setStyleSheet("background-color: black; color: white")
        self.speed_indicator.setText("100")

        #slider
        self.speed_slider = QSlider(Qt.Horizontal, self)
        self.speed_slider.setMinimum(50)
        self.speed_slider.setMaximum(120)
        self.speed_slider.setValue(100)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setTickInterval(5)
        self.speed_slider.setGeometry(120, 40, 200, 15)
        self.speed_slider.valueChanged[int].connect(self.speed_val_change)

        #reading start button
        self.read_button = QPushButton(self)
        self.read_button.setText(" Start ")
        self.read_button.setGeometry(10, 60, 60, 20)
        self.read_button.setStyleSheet("Background-color: black; color: yellow; border-style: outset; border-width: 1px")
        self.read_button.setFont(QFont('SimHei', 10, 10))
        self.read_button.clicked.connect(self.read)

        #next button
        self.next_button = QPushButton(self)
        self.next_button.setText(" Next Page ")
        self.next_button.setGeometry(80, 60, 75, 20)
        self.next_button.setStyleSheet("Background-color: black; color: green; border-style: outset; border-width: 1px")
        self.next_button.setFont(QFont('SimHei', 10, 10))
        self.next_button.clicked.connect(lambda : self.eng.stop())
  
        #stop button
        self.stop_button = QPushButton(self)
        self.stop_button.setText(" Stop ")
        self.stop_button.setGeometry(165, 60, 60, 20)
        self.stop_button.setStyleSheet("Background-color: black; color: red; border-style: outset; border-width: 1px")
        self.stop_button.setFont(QFont('SimHei', 10, 10))
        self.stop_button.clicked.connect(self.stop)


        self.show()

    def select_file(self):
        self.file_name, _ = QFileDialog.getOpenFileName(self, 'OpenFile', filter="pdf(*.pdf)")
        print(self.file_name)
        self.filePathEdit.setText(self.file_name)
        
        try:
            self.fileObj = open(self.file_name, 'rb')  #open the file in read and binary mode
            self.pdfReader = PyPDF2.PdfFileReader(self.fileObj)   #create a file object
            self.pages_num = self.pdfReader.numPages
        except:
            pass

    def talk(self, pageNum, words, voice_id=1):
        #self.eng = pyttsx3.init()           #initialize pyttsx3
        try:
            voices = self.eng.getProperty('voices')
            self.eng.setProperty('voice', voices[voice_id].id)
            #speak the page number, then the text 
            self.eng.say(f"Page {pageNum + 1}" + ", -" + words)    #convert the text into speech (,- used to create a delay)
            self.eng.setProperty('rate', 100) 
            self.eng.runAndWait()
        except:
            self.eng.connect()
            voices = self.eng.getProperty('voices')
            self.eng.setProperty('voice', voices[voice_id].id)
            #speak the page number, then the text 
            self.eng.say(f"Page {pageNum + 1}" + ", -" + words)    #convert the text into speech (,- used to create a delay)
            self.eng.setProperty('rate', 100) 
            self.eng.runAndWait()

    def speed_val_change(self, value):
        print(value)
        self.speed_indicator.setText(str(value))

    def read(self):
        try:
            page_num = self.pages_num
            print(page_num)
        except:
            print("No file or Error Occured")
            return

        for i in range(page_num):
            if self.READ == False:
                break
            pageObj = self.pdfReader.getPage(i)
            text = pageObj.extractText()
            self.talk(pageNum=i, words=text)
        
        self.READ = True

    def stop(self):
        self.READ = False
        self.eng.stop()
        #self.eng.endLoop()


#main section here
def main():
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()