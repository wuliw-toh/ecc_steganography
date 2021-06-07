import tkinter as tk

from module import stat_treak as st



class Main(tk.Frame):

    def __init__(self, root):
        super().__init__(root)
        self.fr_1 = tk.Frame(self)
        self.init_main(self.fr_1)
        self.fr_1.pack()


    def init_main(self,root):
        root.ent_p = tk.Entry(root, font='Times 18')
        root.ent_p.grid(column=0, row=0)

        butt_p = tk.Button(root, text="Ввод",font='Times 18')
        butt_p.grid(column=1, row=0)

        out_text_main = tk.Text(root, font='Times 10')
        out_text_main.grid(column=0, row=1, columnspan=2)

    def stat_work_first(self):
        pass
        #p = self.


if __name__ == '__main__':
    root = tk.Tk()
    app = Main(root)
    app.pack()

    root.title("Главное окно")
    root.geometry("600x800")
    root.resizable(False, False)
    root.mainloop()