"""Audio book in python

python version: 3.8.1

author: ashraf minhaj
mail: ashraf_minhaj@yahoo.com
"""

"""import necessary libraries"""
import PyPDF2              #to extract text from pdf file
import pyttsx3             #to convert text into speech

#name of the file you want to read out
file = "/home/ashraf/Documents/pycodes/python_course/sample.pdf"
reading_speed = 100    #100 words per minute

engine = pyttsx3.init()    #initialize pyttsx3 engine
fileObj = open(file, 'rb')  #open the file in read and binary mode

pdfReader = PyPDF2.PdfFileReader(fileObj)

pages_num = pdfReader.numPages

for num in range(pages_num):      #search for all queries
    pageObj = pdfReader.getPage(num)
    text = pageObj.extractText()

    #sepak the query first, then the topic
    engine.say(f"Page {num + 1}" + ", -" + text)    #convert the text into speech (,- used to create a delay)
    engine.setProperty('rate', reading_speed)       #words per minute
    engine.runAndWait()                   #run untill finish