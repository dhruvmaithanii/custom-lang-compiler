🧠 Hinglish Compiler – Custom Language to Python Translator

> A complete compiler pipeline that translates Hinglish-based programming syntax into executable Python code — featuring a GUI, AST visualization, and error reporting.

---

## 📌 Project Overview

This project is a **custom language compiler** built in Python that lets users write code in a **Hinglish-style syntax** (Hindi-English blend) and compiles it into valid Python code. It covers all phases of compilation:

- **Lexical Analysis** – using regular expressions
- **Parsing** – recursive descent parser
- **AST Construction** – custom node-based tree
- **Semantic Analysis** – undeclared variables, logic issues
- **Code Generation** – Python output
- **Graphical Interface** – Tkinter-based GUI
- **Parse Tree Visualization** – via Graphviz

---

###Project Structure

The project structure is a follows:
custom-lang-compiler/
│
├── compiler/
├── lexer.py              # Tokenizes Hinglish input
├── parser.py             # Builds parse tree from tokens
├── ast_nodes.py          # Defines all AST node types
├── custom_ast_generator.py  # Converts parse tree into AST
├── semantic.py           # Checks for semantic errors
├── codegen.py            # Generates Python code from AST
├── compiler.py           # Driver script combining all phases
├── gui.py                # Tkinter GUI for input/output
├── testcodes.txt         # Sample Hinglish programs
├── wrongcodes.txt        # Deliberate error cases
├── output.py             # Stores generated Python output
└── README.md             # You’re here!
