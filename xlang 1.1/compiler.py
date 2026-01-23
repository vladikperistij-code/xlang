# compiler.py
import re

# compiler.py
def compile_line(line):
    line = line.strip()
    if not line:
        return ""

    # var x = 5
    if line.startswith("var "):
        return line[4:]

    # print(...)
    if line.startswith("print"):
        inside = line[line.find("(")+1:line.rfind(")")]
        return f"x_print({inside})"

    # sleep
    if line.startswith("sleep"):
        arg = line[5:].strip() or "1"
        return f"x_sleep({arg})"

    # echo
    if line.startswith("echo"):
        return "x_print(x_input())"

    # інше — як є
    return line


def compile_script(src_file, out_file):
    with open(src_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    py = []
    py.append("from runtime import *")
    py.append("")

    i = 0
    while i < len(lines):
        raw = lines[i].rstrip("\n")
        line = raw.strip()

        # func
        if line.startswith("func"):
            name = line[5:line.find("(")]
            args = line[line.find("(")+1:line.find(")")]
            py.append(f"def {name}({args}):")
            i += 1
            while i < len(lines) and lines[i].startswith("    "):
                py.append("    " + compile_line(lines[i][4:]))
                i += 1
            continue

        # if / else
        if line.startswith("if"):
            cond = line[3:].rstrip(":")
            py.append(f"if {cond}:")
            i += 1
            while i < len(lines) and lines[i].startswith("    "):
                py.append("    " + compile_line(lines[i][4:]))
                i += 1

            if i < len(lines) and lines[i].strip().startswith("else"):
                py.append("else:")
                i += 1
                while i < len(lines) and lines[i].startswith("    "):
                    py.append("    " + compile_line(lines[i][4:]))
                    i += 1
            continue

        py.append(compile_line(line))
        i += 1

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(py))
