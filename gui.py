import tkinter as tk
from tkinter import scrolledtext, messagebox
from compiler.lexer import lexer
from compiler.parser import Parser
from compiler.semantic import analyze
from compiler.codegen import generate_code, write_python_file
import subprocess
import os

class CompilerGUI:
    def __init__(self, root):
        self.root = root
        root.title("Hinglish Compiler")

        # Input Code Area
        self.input_label = tk.Label(root, text="Input (Hinglish Language):")
        self.input_label.pack()
        self.input_text = scrolledtext.ScrolledText(root, width=80, height=20)
        self.input_text.pack()

        # Action Buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.lex_button = tk.Button(self.button_frame, text="Lexical Analysis", command=self.do_lex)
        self.lex_button.grid(row=0, column=0, padx=5)

        self.parse_button = tk.Button(self.button_frame, text="Parse", command=self.do_parse)
        self.parse_button.grid(row=0, column=1, padx=5)

        self.semantic_button = tk.Button(self.button_frame, text="Semantic Analysis", command=self.do_semantic)
        self.semantic_button.grid(row=0, column=2, padx=5)

        self.codegen_button = tk.Button(self.button_frame, text="Generate Code", command=self.do_codegen)
        self.codegen_button.grid(row=0, column=3, padx=5)

        self.run_button = tk.Button(self.button_frame, text="Run", command=self.do_run)
        self.run_button.grid(row=0, column=4, padx=5)

        # Output Area
        self.output_label = tk.Label(root, text="Output / Errors:")
        self.output_label.pack()
        self.output_text = scrolledtext.ScrolledText(root, width=80, height=15, state='disabled')
        self.output_text.pack()

    def clear_output(self):
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state='disabled')

    def append_output(self, text):
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.config(state='disabled')

    def do_lex(self):
        self.clear_output()
        code = self.input_text.get(1.0, tk.END)
        try:
            tokens = list(lexer(code))
            self.append_output("Tokens:")
            for t in tokens:
                self.append_output(str(t))
        except Exception as e:
            self.append_output(f"Lexical error: {e}")

    def do_parse(self):
        self.clear_output()
        code = self.input_text.get(1.0, tk.END)
        try:
            tokens = lexer(code)
            parser = Parser(tokens)
            ast = parser.parse()
            self.append_output("Parsing successful!")
        except Exception as e:
            self.append_output(f"Parse error: {e}")

    def do_semantic(self):
        self.clear_output()
        code = self.input_text.get(1.0, tk.END)
        try:
            tokens = lexer(code)
            parser = Parser(tokens)
            ast = parser.parse()
            analyze(ast)
            self.append_output("Semantic analysis successful!")
        except Exception as e:
            self.append_output(f"Semantic error: {e}")

    def do_codegen(self):
        self.clear_output()
        code = self.input_text.get(1.0, tk.END)
        try:
            tokens = lexer(code)
            parser = Parser(tokens)
            ast = parser.parse()
            generated_code = generate_code(ast)

            write_python_file(generated_code, "output.py")

            self.append_output("Generated Python code written to output.py:")
            self.append_output(generated_code)
        except Exception as e:
            self.append_output(f"Code generation error: {e}")

    def do_run(self):
        self.clear_output()
        try:
            result = subprocess.run(["python", "output.py"], capture_output=True, text=True)
            if result.returncode == 0:
                self.append_output("Program Output:")
                self.append_output(result.stdout.strip())
            else:
                self.append_output("Runtime error:")
                self.append_output(result.stderr.strip())
        except Exception as e:
            self.append_output(f"Execution error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    gui = CompilerGUI(root)
    root.mainloop()
