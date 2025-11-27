import re, time

variables = {}
functions = {}

def run_line(line):
    line = line.strip()
    if not line:
        return

    # --- VAR ---
    if line.startswith("var") and "=" in line:
        parts = line[4:].split("=", 1)
        name = parts[0].strip()
        value = parts[1].strip()

        # input()
        if value.startswith("input"):
            start = value.find("(") + 1
            end = value.find(")")
            prompt = value[start:end].strip().strip('"')
            value = input(prompt)

        # рядок у лапках
        elif value.startswith('"') and value.endswith('"'):
            value = value[1:-1]

        # арифметика
        elif any(op in value for op in ['+', '-', '*', '/']):
            try:
                for var in variables:
                    value = value.replace(var, str(variables[var]))
                value = eval(value)
            except Exception as e:
                print(f"Error evaluating expression: {e}")

        # число
        elif value.isdigit():
            value = int(value)

        # інша змінна
        elif value in variables:
            value = variables[value]

        variables[name] = value
        return

    # --- PRINT ---
    if line.startswith("print"):
        start = line.find("(") + 1
        end = line.rfind(")")
        content = line[start:end].strip()

        # розбиваємо на рядки у лапках, змінні та числа
        parts = re.findall(r'"[^"]*"|[a-zA-Z_][a-zA-Z0-9_]*|\d+', content)

        out_text = ""
        for part in parts:
            part = part.strip()
            if not part:
                continue
            if part.startswith('"') and part.endswith('"'):
                out_text += part[1:-1]
            elif part in variables:
                out_text += str(variables[part])
            elif part.isdigit():
                out_text += part
        print(out_text)
        return

    # --- ECHO ---
    if line.startswith("echo"):
        print(input())
        return

    # --- SLEEP ---
    if line.startswith("sleep"):
        args = line[5:].strip()
        sec = int(args) if args.isdigit() else 1
        time.sleep(sec)
        return

    # --- ВИКЛИК ФУНКЦІЇ ---
    if "(" in line and ")" in line:
        name = line[:line.find("(")].strip()
        if name in functions:
            args_vals = line[line.find("(")+1:line.find(")")].split(",")
            args_vals = [eval(v) if v.isdigit() else variables.get(v,v) for v in args_vals]
            args_names, func_lines = functions[name]
            local_vars = dict(zip(args_names, args_vals))
            old_vars = variables.copy()
            variables.update(local_vars)
            for l in func_lines:
                run_line(l)
            variables.clear()
            variables.update(old_vars)
        return

def run_script(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip("\n")
        stripped = line.strip()

        # --- FUNC ---
        if stripped.startswith("func"):
            start = stripped.find(" ") + 1
            end = stripped.find("(")
            name = stripped[start:end].strip()
            args = stripped[end+1:stripped.find(")")].split(",")
            args = [a.strip() for a in args]
            func_lines = []
            i += 1
            while i < len(lines) and lines[i].startswith("    "):
                func_lines.append(lines[i][4:].rstrip("\n"))
                i += 1
            functions[name] = (args, func_lines)
            continue

        # --- IF ---
        elif stripped.startswith("if"):
            cond = stripped[3:].strip(": ")
            for var in variables:
                cond = cond.replace(var, str(variables[var]))
            block_lines = []
            i += 1
            while i < len(lines) and lines[i].startswith("    "):
                block_lines.append(lines[i][4:].rstrip("\n"))
                i += 1
            if eval(cond):
                for l in block_lines:
                    run_line(l)
            else:
                if i < len(lines) and lines[i].strip().startswith("else"):
                    i += 1
                    else_lines = []
                    while i < len(lines) and lines[i].startswith("    "):
                        else_lines.append(lines[i][4:].rstrip("\n"))
                        i += 1
                    for l in else_lines:
                        run_line(l)
            continue

        run_line(stripped)
        i += 1

# --- ГОЛОВНА ЧАСТИНА ---
fille = input("Enter the filename: ")
run_script(fille)
