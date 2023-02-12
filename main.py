from getch import getch
import sys
import time
import os
import random

def red(s):
    cch = "\033[91m" + s + "\033[0m"
    return cch

def green(s):
    cch = "\033[92m" + s + "\033[0m"
    return cch

def gray(s):
    cch = "\033[90m" + s + "\033[0m"
    return cch

class TypingTest:
    def print_text(self, text, _end="\n"):
        print("\033[F" * self.WRAP_COUNT, end="\r")
        for pos, char in enumerate(text):
            if self.inputted[pos] == 1:
                print(green(char), end="")
            elif self.inputted[pos] == -1 and ord(char) == 0x20:
                print(red("·"), end="")
            elif self.inputted[pos] == -1:
                print(red(char), end="")
            elif self.inputted[pos] == 0:
                print(gray(char), end="")
        print(_end, end="")

    def __init__(self, text):
        self.text = text
        self.inputted = [0 for _ in text]

        CLI_WIDTH, _ = os.get_terminal_size()
        self.WRAP_COUNT = len(text) // CLI_WIDTH
        print("\n" * self.WRAP_COUNT, end="")
        
        self.loop()
    
    def loop(self):
        wrong = False
        errors = 0
        pos = 0
        starttime = None
        while True:
            # print text
            self.print_text(self.text, _end="")
            sys.stdout.flush()
            newchar = getch()
            
            if starttime is None:
                starttime = time.time()
            
            if ord(newchar) == 0x3:
                print()
                return
            elif ord(newchar) == 0x7F:
                pos = max(pos - 1, 0) # move left but not out of bounds
                self.inputted[pos] = 0
                if all([x >= 0 for x in self.inputted]):
                    wrong = False
            elif ord(newchar) == ord(self.text[pos]):
                self.inputted[pos] = 1
                pos += 1
            elif ord(newchar) != ord(self.text[pos]):
                self.inputted[pos] = -1
                pos += 1
                if wrong == False:
                    wrong = True
                    errors += 1
            
            if all([x == 1 for x in self.inputted]):
                break
        
        self.print_text(self.text, _end="\n\n")

        endtime = time.time()
        wordcount = len(self.text.split())
        avg_wordlen = len(self.text) / wordcount
        elapsed_mins = (endtime - starttime) / 60
        wpm = (len(self.text) / avg_wordlen) / elapsed_mins
        average_error = errors / elapsed_mins
        
        print(f"words: {wordcount}")
        print(f"avg word length: {avg_wordlen}\n")
        print(f"wpm: {wpm - average_error}")
        print(f"raw wpm: {wpm}")
        print(f"errors: {errors}\n")

if __name__ == "__main__":
    if "--random" in sys.argv:
        words = []
        with open("words.txt", "r") as f:
            for word in f.readlines():
                if not word.strip():
                    continue
                words.append(word.strip())
        
        mediumwords = list(filter(lambda a: 4 < len(a) < 7, words[500:]))
        longwords = list(filter(lambda a: len(a) > 6, words[500:]))

        text = []
        for i in range(30):
            text.append(random.choice(mediumwords))
        
        TypingTest(" ".join(text))
    else:
        texts = []
        with open("texts.txt", "r") as f:
            for line in f.readlines():
                if not line.strip():
                    continue
                texts.append(line.strip())
        TypingTest(random.choice(texts))