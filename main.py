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

# ansi escape sequences guide:
# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797

class TypingTest:
    def print_text(self, text, _end="\n"):
        print("\r", end="")
        # move from where the cursor was while typing, to the beginning of the lines
        print("\033[F" * (self.currentline), end="\r")
        for pos, char in enumerate(text):
            if self.inputted[pos] == 1:
                print(green(char), end="")
            elif self.inputted[pos] == -1 and ord(char) == 0x20:
                print(red("·"), end="")
            elif self.inputted[pos] == -1:
                print(red(char), end="")
            elif self.inputted[pos] == 0:
                print(char, end="")
        
        # move from bottom to beginning of lines
        # self.pos // self.CLI_WIDTH = current line number
        print("\033[F" * (self.WRAP_COUNT - self.pos // self.CLI_WIDTH), end="\r")
        # move right `pos` times
        print("\033[C" * (self.pos % self.CLI_WIDTH), end="")
        print(_end, end="")

    def __init__(self, text):
        self.text = text
        self.inputted = [0 for _ in text] # correctness of the text inputted; 1=correct, -1=wrong, 0=not yet inputted
        self.pos = 0 # cursor position

        self.CLI_WIDTH, _ = os.get_terminal_size()
        
        # number of lines that the text spans
        self.WRAP_COUNT = len(text) // self.CLI_WIDTH + text.count("\n")
        print("\n" * self.WRAP_COUNT, end="")
        
        self.loop()
    
    def loop(self):
        wrong = False # incorrect text is currently present
        errors = 0 # number of errors recorded
        starttime = None
        self.currentline = 0
        # since currentline begins at 0, there'll be a bunch of newlines at the beginning
        print("\033[F" * (self.WRAP_COUNT + 1))
        while True:
            # print text
            self.print_text(self.text, _end="")
            sys.stdout.flush()
            newchar = getch()
            self.currentline = self.pos // self.CLI_WIDTH

            if starttime is None: # start after the first character is entered
                starttime = time.time()
            
            if ord(newchar) == 0x3:
                print("\033[B" * (self.WRAP_COUNT - self.currentline))
                return
            elif ord(newchar) == 0x7F:
                self.pos = max(self.pos - 1, 0) # move left but not out of bounds
                self.inputted[self.pos] = 0
                if all([x >= 0 for x in self.inputted]):
                    wrong = False
            elif self.pos >= len(self.text):
                continue
            elif ord(newchar) == ord(self.text[self.pos]):
                self.inputted[self.pos] = 1
                self.pos += 1
            elif ord(newchar) != ord(self.text[self.pos]):
                self.inputted[self.pos] = -1
                self.pos += 1
                if wrong == False:
                    wrong = True
                    errors += 1
            
            if all([x == 1 for x in self.inputted]):
                break
        
        endtime = time.time()
        self.print_text(self.text, _end="\n\n")
        
        wordcount = len(self.text.split())
        avg_wordlen = len([*filter(lambda a: a != " ", self.text)]) / wordcount
        elapsed_mins = (endtime - starttime) / 60
        wpm = (len(self.text) / avg_wordlen) / elapsed_mins
        wpm_approx = (len(self.text) / 5) / elapsed_mins
        average_error = errors / elapsed_mins
        
        print(f"words: {wordcount}")
        print(f"avg word length: {avg_wordlen}\n")
        print(f"wpm: {wpm_approx - average_error}")
        print(f"wpm (by avg wordlen): {wpm - average_error}")
        print(f"raw wpm: {wpm_approx}")
        print(f"errors: {errors}\n")

if __name__ == "__main__":
    if "--random" in sys.argv:
        words = []
        with open("words.txt", "r") as f:
            for word in f.readlines():
                if not word.strip():
                    continue
                words.append(word.strip())
        
        mediumwords = list(filter(lambda a: 4 < len(a) < 7, words[:500]))
        longwords = list(filter(lambda a: len(a) > 6, words[:500]))

        text = []
        for i in range(30):
            text.append(random.choice(mediumwords))
        
        TypingTest(" ".join(text))
    else:
        texts = []
        with open("texts.txt", "r") as f:
            for line in f.read().split("\n\n"):
                if not line.strip():
                    continue
                texts.append(line.strip())
        TypingTest(random.choice(texts))
