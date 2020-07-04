""" *** Python E-Audio Book *** 
This downloads a pdf file from internet and reads it out for you.

author: ashraf minhaj
mail: ashraf_minhaj@yahoo.com
"""
"""We import only what is needed"""
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter     #resource manager and interpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO                                                   #read write string buffer
import pyttsx3                                                            #text to speech
import requests                                                           #for web request (post/get)

pdf_url = "http://codex.cs.yale.edu/avi/db-book/db4/slide-dir/ch1-2.pdf"  #link of the pdf file
#file name with folder path where the downloaded file will be saved.
#in windows directory/folder path is a must, however, not in linux.
file_name = "D:\\Audio Book\\saved_pdf.pdf"     
reading_speed = 100      #words per minute
voice_id = 1             #1 -female voice, 0 -male voice

eng = pyttsx3.init()     #initialize speech engine /API


def pdf_to_text(file_name):
    """Converts pdf to text. Argument file name"""
    resourceManager = PDFResourceManager()     #to store shared resources such as fonts or images
    retstr = StringIO()                        #reads and writes a string buffer
    device = TextConverter(resourceManager, retstr, laparams=LAParams())  #Create a PDF device object.

    f = open(file_name, 'rb')                                 #open the file in read and binary mode
    interpreter = PDFPageInterpreter(resourceManager, device) #Interpreter to process the page contents
    #pagenos = set()                                          #store in a set pagenos,

    for page in PDFPage.get_pages(f, maxpages=0, caching=True, check_extractable=True):
        interpreter.process_page(page)

    f.close()                  #close the file after reading
    device.close()             #close the device
    text = retstr.getvalue()   #extract text
    retstr.close()
    return text                #return the extracted text

def read_out(text, voice, speed):
    """Read out the text. Argument text-to read, voice-0/1, speed-words per minute"""
    voices = eng.getProperty('voices')            #get the voices
    eng.setProperty('voice', voices[voice].id)    #select voice
    eng.say(text)                                 #convert the text into speech 
    eng.setProperty('rate', speed)                #words per minute
    eng.runAndWait()                              #run


def audio_book(url):
    """1.downloads a pdf file from given url
       2.converts into text
       3.reads it out
    """
    try:                                              #try getting 
        response = requests.get(url, stream=True)     #get web request
    except:                                           #in case of an error, close the program
        print("There might be an issue with the internet or url.")
        return

    if response.status_code != 200:               #200 means ok, if not close the program
        print("Get request fail, check internet connection or provide a valid url")
        return

    with open(file_name,"wb") as pdf:                         #open in write and binary mode
        for chunk in response.iter_content(chunk_size=1024): 
            if chunk:                                         # writing one chunk at a time to pdf file 
                pdf.write(chunk)
  
    text = pdf_to_text(file_name=file_name)                   #convert pdf to text
    read_out(text=text, voice=voice_id, speed=reading_speed)  #read the text 


"""run"""
print("Press CTRL+C to stop!")
audio_book(url=pdf_url)