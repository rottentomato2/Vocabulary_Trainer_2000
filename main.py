# Diese Datei ist nun im GIT-Reposetory


import PyQt5
import os
import sys
from enum import Enum

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from PyQt5.QtCore import QRect, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import *

from PyQt5 import QtCore

import random
import pickle
result_showed = False
import csv

#os.environ["QT_QPA_PLATFORM"] = "wayland"


class VocabularyTrainer2(QWidget):

    def __init__(self):
        super().__init__(windowTitle="Vokabeltrainer", minimumSize=QSize(850, 550))

class VocabularyTrainer(QWidget):

    def __init__(self):
        super().__init__(windowTitle="Vokabeltrainer", minimumSize=QSize(850, 550))
        self.setStyleSheet("background-color: #282828;")

        self.headline1 = QLabel("Vokabel", self)
        self.headline1.setFont(QFont("Arial", 24))
        self.headline1.setStyleSheet("color: whitesmoke;")
        self.headline1.setAlignment(Qt.AlignCenter)

        self.result_label = QLabel("", self)
        self.result_label.setFont(QFont("Arial", 18))
        self.result_label.setStyleSheet("color: whitesmoke;")
        self.result_label.setAlignment(Qt.AlignCenter)

        self.correct_word_label = QLabel("", self)
        self.correct_word_label.setFont(QFont("Arial", 18))
        self.correct_word_label.setStyleSheet("color: whitesmoke;")
        self.correct_word_label.setAlignment(Qt.AlignCenter)

        self.next_word = QPushButton("Next", self)
        self.next_word.clicked.connect(self.next)
        self.next_word.setStyleSheet("QPushButton { color: whitesmoke; }")


        self.input_line = QLineEdit(self)
        self.input_line.returnPressed.connect(self.check_input)
        self.input_line.setStyleSheet("QLineEdit {color: whitesmoke; padding: 8px 5px 8px 5px; border: 1px solid whitesmoke; border-radius: 0.3em;}")

        self.input_a = QLineEdit(self)
        self.input_a.setStyleSheet("QLineEdit {color: whitesmoke; padding: 8px 5px 8px 5px; border: 1px solid whitesmoke; border-radius: 0.3em;}")
        self.input_a.setPlaceholderText("Frage:")
        self.input_a.hide()

        self.input_b = QLineEdit(self)
        self.input_b.setStyleSheet("QLineEdit {color: whitesmoke; padding: 8px 5px 8px 5px; border: 1px solid whitesmoke; border-radius: 0.3em;}")
        self.input_b.setPlaceholderText("Antwort: ")
        self.input_b.returnPressed.connect(self.new_voc)
        self.input_b.hide()

        self.list_of_labels = ["headline1", "result_label", "correct_word_label", "next_word", "input_line"]


        self.h = QVBoxLayout()
        self.h.addWidget(self.headline1, alignment=Qt.AlignCenter) 
        self.h.addWidget(self.result_label)
        self.h.addWidget(self.correct_word_label)
        self.h.addWidget(self.next_word, alignment=Qt.AlignRight)
        self.h.addWidget(self.input_line)
        self.setLayout(self.h)


        self.filename = ""
        self.new_voc = {}
        self.load_voc("vocabulary.csv")
        self.show_word()
        
        #self.save_pickle()

        #self.vocabulary["color"] = "Farbe"


    def hide_all(self):
        empty_layout = QVBoxLayout()
        self.setLayout(empty_layout)

    def load_voc(self, filename):
        self.vocabulary = {}
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                if len(row) == 2:
                    self.vocabulary[row[0]] = row[1]
                    self.next()

    def show_word(self):
        self.current_word = random.choice(list(self.vocabulary.keys()))
        self.headline1.setText(self.current_word)
        self.input_line.clear()
        self.input_line.setFocus(QtCore.Qt.MouseFocusReason)

    def eingabe(self):
        self.input_line.hide()
        self.langauge1_input = QLineEdit(self)
        self.langauge1_input.show()
        self.langauge1_input.setStyleSheet("QLineEdit {color: whitesmoke; padding: 8px 5px 8px 5px; border: 1px solid whitesmoke; border-radius: 0.3em;}")

    def check_input(self):

        global result_showed

        print("check_input(self) wurde aufgerufen")
        input = self.input_line.text()
        print(input)

        if result_showed == True:
            self.next()
        else:
            if input == "eingabe":
                self.eingabe()
            elif input == "abfrage":
                self.abfrage()
            elif input == "ausgabe":
                print("ausgabe")
            elif input == "current_word()":
                self.show_word()
            elif input == "beenden":
                quit() 
            
            else:
                if input == self.vocabulary[self.current_word]:
                    result_showed = True
                    self.result_label.setText("correct")
                    self.result_label.setStyleSheet("color: #50fa7b;")
                else:
                    result_showed = True
                    self.result_label.setText("incorrect")
                    self.result_label.setStyleSheet("color: #ff5555;")
                    correct_word = str(self.vocabulary[self.current_word])
                    self.correct_word_label.setText(f"The correct translation is: {correct_word}")
    
    def next(self):
        self.show_word()
        self.correct_word_label.setText("")
        self.result_label.setText("")
        global result_showed
        result_showed = False

    def keyPressEvent(self, QKeyEvent):
        print("Key pressed!")
        if QKeyEvent.key() == Qt.Key_O:
            print("STR+O wurde gedrückt")
            x = str(QFileDialog.getOpenFileName())
            x = x.replace("', 'All Files (*)')", "")
            x = x.replace("('", "")
            print(x)
            self.load_voc(x)
        elif QKeyEvent.key() == Qt.Key_N:
            self.new_voc_set()
        elif QKeyEvent.key() == Qt.Key_H:
            self.hide_all()
    
    def new_voc_set(self):
        print("STR N")
        self.filename = str(QFileDialog.getSaveFileName())
        self.filename = self.filename.replace("', 'All Files (*)')", "")
        self.filename = self.filename.replace("('", "")
        print(self.filename)

        self.hide_all()

        self.h.removeWidget(self.input_b)
        self.h.removeWidget(self.headline1)
        self.headline1.hide()
        self.h.removeWidget(self.next_word)
        self.next_word.hide()
        self.h.removeWidget(self.input_line)
        self.input_line.hide()

        self.h.addWidget(self.input_a)
        self.h.addWidget(self.input_b)
        self.input_a.show()
        self.input_b.show()
        
    def new_voc(self):
        datei = open(self.filename, "a")
        datei.write(f"\n{self.input_a.text()},{self.input_b.text()}")
        datei.close()
        self.input_a.clear()
        self.input_b.clear()
        self.input_a.setFocus()

    

def main():
    app = QApplication(sys.argv)
    fenster = VocabularyTrainer()
    fenster.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()