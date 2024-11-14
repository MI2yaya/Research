import sys
import os
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import pyttsx3
import traceback, sys
import speech_recognition as sr
from autocorrect import Speller
from deepmultilingualpunctuation import PunctuationModel

#https://openai.com/index/whisper/ - OpenAI TTS/STT

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

class ChatBox(QMainWindow):
    def __init__(self):
        super().__init__()

        self.recognizer = sr.Recognizer()
        self.spell = Speller(lang='en')
        self.punctuation_model = PunctuationModel()

        self.threadpool = QThreadPool()

        # Set up the TTS engine
        self.tts_engine = pyttsx3.init()

        # Set up the main window
        self.setWindowTitle("Chatbox")
        self.setGeometry(300, 300, 400, 500)

        # Layout for the widgets
        layout = QVBoxLayout()

        # Text display area (for chat history)
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        layout.addWidget(self.text_display)

        # Input field for user messages
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message here...")
        layout.addWidget(self.input_field)

        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        layout.addWidget(self.send_button)

        # Record Button
        self.record_button = QPushButton("Record")
        self.record_button.clicked.connect(self.start_recording)
        layout.addWidget(self.record_button)
        
        # Set the main widget and layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        

    def send_message(self):

        user_message = self.input_field.text()

        if user_message:
            self.text_display.append(f"User: {user_message}")

            bot_response = self.generate_response(user_message)

            self.text_display.append(f"Bot: {bot_response}")

            self.tts_engine.say(bot_response)
            self.tts_engine.runAndWait()
            self.input_field.clear()

    def generate_response(self, message):
        # Placeholder
        return f"Echo: {message}"
    
    def start_recording(self):
        # Change button text to "Recording..." and disable it
        self.record_button.setText("Recording...")
        self.record_button.setEnabled(False)
        
        worker = Worker(self.record,
                    recognizer=self.recognizer,
                    spell=self.spell,
                    punctuation_model=self.punctuation_model)
        
        worker.signals.result.connect(self.display_recognition_result)  # Connect the finished signal
        worker.signals.error.connect(self.handle_error)  # Handle any error

        self.threadpool.start(worker)
    
    def record(self,progress_callback, recognizer, spell, punctuation_model):
        
        try:
            with sr.Microphone() as source:
                # Calibrate and record audio
                print("Calibrating microphone...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Recording...")
                audio = recognizer.listen(source)

                # Convert audio to text
                print("Converting speech to text...")
                recognized_text = recognizer.recognize_google(audio)

                # Apply autocorrect and punctuation restoration
                corrected_text = spell(recognized_text)
                
                punctuated_text = punctuation_model.restore_punctuation(corrected_text)

                punctuated_text=punctuated_text[0].upper()+punctuated_text[1:]
                
                return punctuated_text  

        except sr.RequestError as e:
            return(f"STT Request Error: {e}")
        except sr.UnknownValueError:
            return("STT could not understand the audio")
    
    def display_recognition_result(self, result_text):
        # Show the recognized and processed text
        self.input_field.setText(result_text)

        # Reset the button state
        self.record_button.setText("Record")
        self.record_button.setEnabled(True)

    def handle_error(self, error_message):
        # Display error message if speech recognition fails
        self.text_display.append(f"Error: {error_message}")

        # Reset the button state
        self.record_button.setText("Record")
        self.record_button.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    chatbox = ChatBox()
    chatbox.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
