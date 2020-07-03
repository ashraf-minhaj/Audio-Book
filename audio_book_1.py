"""Audio book in python

python version: 3.7.1
author: ashraf minhaj
mail: ashraf_minhaj@yahoo.com
"""

"""import necessary libraries"""
import PyPDF2              #to extract text from pdf file
import pyttsx3             #to convert text into speech

#name of the file you want to read out (with path)
file_name = "D:\\Audio Book\\sample.pdf"
reading_speed = 100      #100 words per minute
voice_id = 1             #1 -female voice, 0 -male voice

engine = pyttsx3.init()          #initialize pyttsx3 engine
fileObj = open(file_name, 'rb')  #open the file in read and binary mode

pdfReader = PyPDF2.PdfFileReader(fileObj)   #create a file object
pages_num = pdfReader.numPages              #get num of pages in our file

print("Press CTRL+C to stop!")

for num in range(pages_num):
    """This runs through all pages (one after another)"""
    pageObj = pdfReader.getPage(num)  #select a page by number (We count from 0, mind it)
    text = pageObj.extractText()      #get the text from our file
     
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)
    #speak the page number, then the text 
    engine.say(f"Page {num + 1}" + ", -" + text)    #convert the text into speech (,- used to create a delay)
    engine.setProperty('rate', reading_speed) 
    engine.runAndWait()                             #run untill finish

fileObj.close()  #close the file we opened before finishing