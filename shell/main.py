import tkinter as tk


class Main(tk.Frame):

    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        big_title = tk.Label(text="Демонстрационная модель", font="20")
        #big_title.grid(row=0, column=0)
        #big_title.place(self.)
        big_title.pack()



if __name__ == '__main__':
    root = tk.Tk()
    app = Main(root)
    app.pack()

    root.title("Главное окно")
    root.geometry("1000x500")
    root.resizable(False, False)
    root.mainloop()
