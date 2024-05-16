import sys

htmlfile = {"file": "index.html"}

class Lexer:
    def __init__(self,linenum,tokens):
        self.tokens = tokens
        self.linenum = linenum
    
    def printtokens(self):
        print(f"tokens: {self.tokens}. line: {self.linenum}")

def interpret(code):
    linenum = 0
    lines = code.split("\n")

    for line in lines:
        linenum += 1
        tokens = line.split(" ") or line.split("\t")

        if tokens:
            token = tokens[0]
            
            if token == "htmlfile":
                htmlfile["file"] = tokens[1]
                with open(htmlfile["file"], "w") as fi:
                    fi.write("")
                print(f"Created html file: {htmlfile['file']}")
            else:
                htmlcode = " ".join(tokens)
                with open(htmlfile["file"], "a") as fi:
                    fi.write(htmlcode + "\n")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f"usage: {sys.argv[0]} <command>")
        print("commands:")
        print("-v               version")
        print("<file>           executes your file")
    else:
        command = sys.argv[1]

        if command == "-v":
            print("haloha (aloha but for html)")
            print("version: 1.0.0")
        else:
            if command.endswith(".halo"):
                with open(command, "r") as f:
                    content = f.read()
                interpret(content)
            else:
                print("Use a .halo file extension!")
