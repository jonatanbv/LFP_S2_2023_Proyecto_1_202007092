import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from analizador import analizar

class ScrollText(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = tk.Text(
            self,
            bg="#f8f9fa",
            foreground="#343a40",
            insertbackground="#3b5bdb",
            selectbackground="blue",
            width=120,
            height=25,
            font=("Courier New", 13),
        )

        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.numberLines = TextLineNumbers(self, width=40, bg="#dee2e6")
        self.numberLines.attach(self.text)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.numberLines.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numberLines.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.text.bind("<MouseWheel>", self.onPressDelay)

    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numberLines.redraw)

    def onScrollRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numberLines.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.numberLines.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        self.numberLines.redraw()


class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        """redraw line numbers"""
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(
                2,
                y,
                anchor="nw",
                text=linenum,
                fill="#868e96",
                font=("Courier New", 13, "bold"),
            )
            i = self.textwidget.index("%s+1line" % i)


class Ventana(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Proyecto 1")
        self.geometry("1000x700")
        self.scroll = ScrollText(self)
        self.scroll.pack()
        self.after(200, self.scroll.redraw())

        self.menu = Menu(self)
        self.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="New")
        self.filemenu.add_command(label="Open...", command=self.open_file)
        self.filemenu.add_command(label="Save file...", command=self.save_file)

        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)
        self.menu.add_command(label="Analizar" )
        self.menu.add_command(label="Ver reporte")
        self.menu.add_command(label="Ver errores")

        btn_analizar = Button(self, text="Analizar entrada", command=self.analizar_texto, bg="red", fg="black", font=(15))
        btn_analizar.pack()
    def open_file(self):
        filepath = askopenfilename(
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        
        self.scroll.delete(1.0,tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.read()
            self.scroll.insert(tk.END, text)
        self.title(f"Proyecto 1 - {filepath}")

    def save_file(self):
        filepath = asksaveasfilename(
            defaultextension="json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = self.scroll.get(1.0, tk.END)
            output_file.write(text)
        self.title(f"Proyecto 1 - {filepath}")

    def analizar_texto(self):
        print("Analizando...")
        text = self.scroll.get(1.0, tk.END) 
        arbol = analizar(text)
        print(arbol.dot.source)
        arbol.dot.view()

app = Ventana()
app.mainloop()