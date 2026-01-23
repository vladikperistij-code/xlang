# main.py
import os
from compiler import compile_script

src = input("Enter source file: ").strip()

# захист від лапок
if src.startswith(("'", '"')) and src.endswith(("'", '"')):
    src = src[1:-1]

out = "compiled.py"

compile_script(src, out)

print("\n--- COMPILED ---")
print("Running...\n")

os.system(f"python {out}")
