<<<<<<< HEAD
🧠 Hinglish Compiler – Custom Language to Python Translator
=======
# 🧠 Hinglish Compiler – Custom Language to Python Translator
>>>>>>> 375c1b9 (Add README.md with project documentation)

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
<<<<<<< HEAD
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
=======

---

## 🧪 Sample Hinglish Code

```hinglish
shuru karo
    rakho x barabar 5 ardhaviram
    agar kholo x bada hai 0 band shuru bhai
        dikhao kholo "Positive" band ardhaviram
    band karo
khatam karo
```

**Python Output:**
```python
x = 5
if x > 0:
    print("Positive")
```

---

## 🗂️ Project Structure

```
custom-lang-compiler/
│
├── compiler/
│   ├── lexer.py              # Tokenizes Hinglish input
│   ├── parser.py             # Builds parse tree from tokens
│   ├── ast_nodes.py          # Defines all AST node types
│   ├── custom_ast_generator.py  # Converts parse tree into AST
│   ├── semantic.py           # Checks for semantic errors
│   ├── codegen.py            # Generates Python code from AST
│   ├── compiler.py           # Driver script combining all phases
>>>>>>> 375c1b9 (Add README.md with project documentation)
├── gui.py                # Tkinter GUI for input/output
├── testcodes.txt         # Sample Hinglish programs
├── wrongcodes.txt        # Deliberate error cases
├── output.py             # Stores generated Python output
<<<<<<< HEAD
└── README.md             # You’re here!
=======
└── README.md             
```

---

## 💻 How to Run

### 1. Clone the Repo

```bash
git clone https://github.com/dhruvmaithanii/custom-lang-compiler.git
cd custom-lang-compiler
```

### 2. (Optional) Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Launch GUI

```bash
python gui.py
```

---

## 🖼️ Features

✅ Hinglish syntax support  
✅ Full compiler pipeline (lex → parse → semantic → AST → codegen)  
✅ AST and parse tree visualization using Graphviz  
✅ GUI for easy interaction  
✅ Inline error reporting and code preview  
✅ Educational and beginner-friendly compiler structure

---

## 📚 Dependencies

- Python 3.8+
- `tkinter` (comes with Python)
- `re` (standard library)

## 🤝 Collaborators

- Dhruv Maithani  
- Pranav Chamoli  
- Priyanshu Bisht
- Animesh Mamgain

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Contributing

Pull requests are welcome! If you have suggestions for Hinglish syntax extensions or want to improve the parsing logic, feel free to open an issue or PR.

---
>>>>>>> 375c1b9 (Add README.md with project documentation)
