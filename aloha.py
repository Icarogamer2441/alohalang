import sys
import time
import subprocess as sb
from random import randint

functions = {}
variables = {}
running_while = {"TrueOrFalse": False}

def interpret(code):
    lines = code.split("\n")
    in_func = False
    in_while = False
    in_for = False
    in_if = False
    funcname = ""
    varname1 = ""
    varname2 = ""
    ifname = ""
    forname = ""
    whilename = ""
    condition_type = ""
    lineslist = []
    times = 0
    linenum = 1

    for line in lines:
        tokens = line.split() or line.split("\t")
        linenum +=1

        if tokens:
            token = tokens[0]

            if in_func == False and in_while == False and in_for == False and in_if == False:
                if token == "put":
                    if tokens[1] == "\"":
                        if tokens[-1] == "\"":
                            msg = tokens[2:len(tokens) - 1]
                            print(" ".join(msg))
                    else:
                        varname = tokens[1]
                        print(variables.get(varname))
                elif token == "var":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        value = tokens[3]
                        if value == "\"":
                            if tokens[-1] == "\"":
                                string = tokens[4:len(tokens) - 1]
                                variables[varname] = " ".join(string)
                        else:
                            try:
                                floating = float(value)
                                variables[varname] = floating
                            except ValueError:
                                pass

                            try:
                                integer = int(value)
                                variables[varname] = integer
                            except ValueError:
                                pass
                    else:
                        print(f"Error at line: {linenum}. Illegal token: {tokens[2]}")
                        break
                elif token == "fnc":
                    funcname = tokens[1]
                    if tokens[2] == "{":
                        in_func = True
                        lineslist = []
                    else:
                        print(f"Error at line: {linenum}. Illegal token: {tokens[2]}")
                        break
                elif token == "call":
                    name = tokens[1]
                    interpret(functions.get(name))
                elif token == "" or token == "&&" or token == "}":
                    pass
                elif token == "if":
                    varname1 = tokens[1]
                    condition_type = tokens[2]
                    varname2 = tokens[3]
                    ifname = tokens[4]
                    if tokens[5] == "{":
                        in_if = True
                        lineslist = []
                    else:
                        print(f"Error at line: {linenum}. Illegal token: {tokens[5]}")
                        break
                elif token == "for":
                    times = tokens[1]
                    forname = tokens[2]
                    if tokens[3] == "{":
                        in_for = True
                        lineslist = []
                    else:
                        print(f"Error at line: {linenum}. Illegal token: {tokens[3]}")
                        break
                elif token == "num":
                    varname11 = tokens[1]
                    if tokens[2] == ">":
                        varname22 = tokens[3]
                        variables[varname22] += variables.get(varname11)
                    else:
                        print(f"Error at line: {linenum}. Illegal token: {tokens[2]}")
                        break
                elif token == "while":
                    whilename = tokens[1]
                    if tokens[2] == "{":
                        in_while = True
                        lineslist = []
                    else:
                        print(f"Error at line: {linenum}. Illegal token: {tokens[2]}")
                        break
                elif token == "stop":
                    running_while["TrueOrFalse"] = False
                elif token == "wait":
                    waittime = tokens[1]
                    time.sleep(float(waittime))
                elif token == "#import":
                    file = tokens[1]
                    with open(file + ".alo", "r") as fi:
                        content = fi.read()
                    interpret(content)
                elif token == "sys":
                    if tokens[1] == "\"":
                        if tokens[-1] == "\"":
                            command = tokens[2:len(tokens) - 1]
                            finalcmd = " ".join(command)
                            sb.run(finalcmd, shell=True)
                        else:
                            print(f"Error at line: {linenum}. Illegal token: {tokens[-1]}")
                            break
                    else:
                        varname = tokens[1]
                        sb.run(variables.get(varname), shell=True)
                elif token == "joinvar":
                    varname11 = tokens[1]
                    if tokens[2] == ">>":
                        varname22 = tokens[3]
                        if tokens[4] == ":":
                            varname33 = tokens[5]
                            variables[varname33] = variables.get(varname22) + " " + variables.get(varname11)
                    else:
                        print(f"Error at line: {linenum}. Illegal token: {tokens[2]}")
                        break
                elif token == "puts":
                    if tokens[1] == "\"":
                        if tokens[-1] == "\"":
                            msg = tokens[2:len(tokens) - 1]
                            print(" ".join(msg), end="")
                    elif tokens[1] == "space":
                        print(" ", end="")
                    elif tokens[1] == "newline":
                        print("")
                    else:
                        varname = tokens[1]
                        print(variables.get(varname), end="")
                elif token == "input":
                    inputtype = tokens[1]
                    if inputtype == "int":
                        varname = tokens[2]
                        variables[varname] = int(input())
                    elif inputtype == "float":
                        varname = tokens[2]
                        variables[varname] = float(input())
                    elif inputtype == "string":
                        varname = tokens[2]
                        variables[varname] = input()
                    else:
                        print(f"Error at line: {linenum}. Illegal token: {tokens[inputtype]}")
                        break
                elif token == "randnum":
                    num1 = tokens[1]
                    if tokens[2] == ":":
                        num2 = tokens[3]
                        if tokens[4] == ">>":
                            varname = tokens[5]
                            variables[varname] = randint(int(num1),int(num2))
                        else:
                            print(f"Error at line: {linenum}. Illegal token: {tokens[4]}")
                            break
                    else:
                        print(f"Error at line: {linenum}. Illegal token: {tokens[2]}")
                        break
                else:
                    print(f"Error at line: {linenum}. Illegal token: {token}")
                    break

            if in_func:
                if token == "}" and tokens[1] == funcname:
                    funcname = tokens[1]
                    codee = "\n".join(lineslist)
                    functions[funcname] = codee
                    in_func = False
                elif token == "fnc" and tokens[1] == funcname:
                    pass
                else:
                    lineslist.append(" ".join(tokens[0:]))
            
            if in_if:
                if token == "}" and tokens[1] == ifname:
                    in_if = False
                    codee = "\n".join(lineslist)
                    if condition_type == "==":
                        if variables.get(varname1) == variables.get(varname2):
                            interpret(codee)
                    if condition_type == "!=":
                        if variables.get(varname1) != variables.get(varname2):
                            interpret(codee)
                    if condition_type == "<=":
                        if variables.get(varname1) <= variables.get(varname2):
                            interpret(codee)
                    if condition_type == ">=":
                        if variables.get(varname1) >= variables.get(varname2):
                            interpret(codee)
                    if condition_type == "<":
                        if variables.get(varname1) < variables.get(varname2):
                            interpret(codee)
                    if condition_type == ">":
                        if variables.get(varname1) > variables.get(varname2):
                            interpret(codee)
                elif token == "if" and tokens[4] == ifname:
                    pass
                else:
                    lineslist.append(" ".join(tokens))

            if in_for:
                if token == "}" and tokens[1] == forname:
                    in_for = False
                    codee = "\n".join(lineslist)
                    for i in range(int(times)):
                        interpret(codee)
                elif token == "for" and tokens[2] == forname:
                    pass
                else:
                    lineslist.append(" ".join(tokens))

            if in_while:
                if token == "}" and tokens[1] == whilename:
                    in_while = False
                    running_while["TrueOrFalse"] = True
                    codee = "\n".join(lineslist)
                    while running_while["TrueOrFalse"]:
                        interpret(codee)
                elif token == "while" and tokens[1] == whilename:
                    pass
                else:
                    lineslist.append(" ".join(tokens))

if __name__ == "__main__":
    version = "1.2.0"
    if len(sys.argv) == 1:
        print(f"usage: {sys.argv[0]} <command>")
        print("commands:")
        print("-v               language version")
        print("<file>           executes your .alo file")
    else:
        command = sys.argv[1]

        if command == "-v":
            print(f"alohalang Version: {version}")
            print("aloha comes from 'love' (idk why i made the name of the language be 'love')")
        else:
            if command.endswith(".alo"):
                with open(command, "r") as f:
                    interpret(f.read())
            else:
                print("Use a .alo file extension")
