
import tkinter as tk
from tkinter import scrolledtext

def run_kori_code(code, output_box):
    lines = code.strip().split('\n')
    variables = {}
    output = ""

    def eval_expr(expr):
        try:
            for var in variables:
                expr = expr.replace(var, str(variables[var]))
            return eval(expr)
        except:
            return expr.strip('"').strip("'")

    def execute_line(line):
        nonlocal output
        if line.startswith("ছাপাও"):
            expr = line[6:].strip("() ")
            result = eval_expr(expr)
            output += str(result) + "\n"
        elif "=" in line:
            var, expr = line.split("=", 1)
            variables[var.strip()] = eval_expr(expr.strip())

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # যদি Block
        if line.startswith("যদি"):
            condition = line[4:].strip("(): ")
            condition_result = bool(eval_expr(condition))

            i += 1
            if i < len(lines):
                true_block = lines[i].strip()
                if condition_result:
                    execute_line(true_block)
                    i += 1
                    # Skip নইলে block and its line
                    if i < len(lines) and lines[i].strip().startswith("নইলে"):
                        i += 2
                else:
                    # Check for নইলে
                    if true_block.startswith("নইলে"):
                        i += 1
                        if i < len(lines):
                            execute_line(lines[i].strip())
                            i += 1
                    elif i < len(lines) and lines[i].strip().startswith("নইলে"):
                        i += 1
                        if i < len(lines):
                            execute_line(lines[i].strip())
                            i += 1
        else:
            execute_line(line)
            i += 1

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, output if output else "→ কোনো আউটপুট নেই")

# GUI Setup
def create_gui():
    window = tk.Tk()
    window.title("Chinta (চিন্তা) - বাংলা কোড রানার")
    window.geometry("800x600")

    label = tk.Label(window, text="বাংলা কোড লেখো:", font=("Arial", 14))
    label.pack()

    code_input = scrolledtext.ScrolledText(window, width=90, height=18, font=("Consolas", 12))
    code_input.pack(pady=10)

    run_button = tk.Button(window, text="▶ রান করো", font=("Arial", 12, "bold"),
                           command=lambda: run_kori_code(code_input.get("1.0", tk.END), output_box))
    run_button.pack(pady=5)

    output_label = tk.Label(window, text="আউটপুট:", font=("Arial", 14))
    output_label.pack()

    output_box = scrolledtext.ScrolledText(window, width=90, height=10, font=("Consolas", 12), bg="#f4f4f4")
    output_box.pack(pady=10)

    window.mainloop()

# Run
create_gui()
