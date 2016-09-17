import os
import json
from input import InputReader

def speak(text):
    assert not '"' in text, "Text cannot contain \""
    os.system("espeak \"{}\"".format(text))

class TwineEngine:
    def __init__(self,filename='story.json'):
        with open(filename):
            self.story = json.loads("story.json")
        self.vars = []
        self.current = self.interpret_text_codes(self.story["passages"][0]["text"])

    def goto(self,name):
        passage = next(x for x in self.story["passages"] if x["name"] == name)
        self.current = self.interpret_text_codes(passage["text"])


    def whereAmI(self):
        self.current.tell()
    def run(self):
        for key in InputReader()():
            if key == ".":
                self.whereAmI()
            elif key in "0123456789":
                self.goto(self.current.get_choice(int(key)))
            elif key == "<":
                return



    def interpret_text_codes(self,text):
        text = text.replace("[[","\n[[").replace("<<","/<<")
        valid_if = True
        s = Situation()
        for line in text.split("\n"):
            if not line:
                continue
            if line.startswith("<<"):
                if line == "<<else>>":
                    valid_if = not valid_if
                elif line == "<<endif>>":
                    valid_if = True
                else:
                    valid_if = self.eval_expression(line[2:-2])
            elif line.startswith("[["):
                if valid_if:
                    s.add_choice(*line[2:-2].split("->"))
            else:
                if valid_if:
                    s.add_text(line)
        return s


    def eval_expression(self,expr):
        code,lexp,expr,rexp = expr.split(" ")
        if code == "set":
            rval = self.strip_rval(rexp)
            if expr == "=":
                self.vars[lexp[1:]] = rval
            elif expr == "+=":
                self.vars[lexp[1:]] += rval
            elif expr == "-=":
                self.vars[lexp[1:]] -= rval
            return True
        elif code == "if":
            lval = self.strip_rval(lexp)
            rval = self.strip_rval(rexp)
            if expr == "==":
                return lval == rval
            elif expr == "<=":
                return lval <= rval
            elif expr == "<":
                return lval < rval
            elif expr == "!=":
                return lval != rval
            elif expr == ">=":
                return lval >= rval
            elif expr == ">":
                return lval > rval

    def strip_rval(self,rexp):
        if rexp.startswith("$"):
            return self.vars[rexp[1:]]
        elif rexp.startswith("\""):
            return rexp[1:-1]
        else:
            return float(rexp)



class Situation():
    def __init__(self):
        self.text = ""
        self.choices = []
    def add_text(self,t):
        self.text = self.text + "\n" + t.strip()
    def tell(self):
        speak(self.text)
        for i,(c,l) in self.choices:
            speak("press {} to {}".format(i,c))
    def add_choice(self,text,to):
        self.choices.append((text.strip(),to.strip()))
    def get_choice(self,index):
        return self.choices[index][1]

if __name__ == "__main__":
    TwineEngine().run()
