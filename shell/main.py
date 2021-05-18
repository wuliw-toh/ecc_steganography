import tkinter as tk


class Main(tk.Frame):

    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        #пара параметров для настройки
        step_x = 20
        step_y = 20

        self.big_title = tk.Label(self, text="Демонстрационная модель",
                                  font=('Times New Roman', 16, "bold"))
        self.big_title.grid(row=0, column=0,columnspan=3)

        self.btn_stat_start = tk.Button(self,text="stst",font=('Times New Roman', 14),
                                        height=3,width=8, command=self.open_stst_config)
        self.btn_stat_start.grid(row=2, column=0, padx=step_x, pady=step_y)

        self.btn_ecc_box = tk.Button(self,text="ecc_box",font=('Times New Roman', 14),height=3,width=8)
        self.btn_ecc_box.grid(row=1,column=1, padx=step_x, pady=step_y)

        self.btn_ecc_mail = tk.Button(self,text="ecc_mail",font=('Times New Roman', 14),height=3,width=8)
        self.btn_ecc_mail.grid(row=3,column=1, padx=step_x, pady=step_y)

        self.btn_secret_blok = tk.Button(self,text="secret_blok",font=('Times New Roman', 14),height=3,width=10)
        self.btn_secret_blok.grid(row=2,column=2, padx=step_x, pady=step_y)

        self.btn_communication_line = tk.Button(self,text="communication_line",
                                                font=('Times New Roman', 14),height=3,width=20)
        self.btn_communication_line.grid(row=2,column=3, padx=step_x, pady=step_y)

        self.btn_attack = tk.Button(self,text="attack",font=('Times New Roman', 14),height=3,width=10)
        self.btn_attack.grid(row=3,column=3, padx=step_x, pady=step_y)

        self.btn_secret_blok_out = tk.Button(self,text="secret_blok_out",
                                             font=('Times New Roman', 14),height=3,width=15)
        self.btn_secret_blok_out.grid(row=2,column=4, padx=step_x, pady=step_y)

        self.btn_ecc_box_out = tk.Button(self,text="ecc_box_out",font=('Times New Roman', 14),height=3,width=15)
        self.btn_ecc_box_out.grid(row=1,column=5, padx=step_x, pady=step_y)

        self.btn_ecc_mail_out = tk.Button(self,text="ecc_mail_out",font=('Times New Roman', 14),height=3,width=15)
        self.btn_ecc_mail_out.grid(row=3,column=5, padx=step_x, pady=step_y)

    def open_stst_config(self):
        self.config_win = stat_config(self)

class stat_config(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        #self.geometry("480x500")
        self.resizable(False,False)
        self.init_gui()

    def init_gui(self):
        self.main_text = tk.Label(self,text="Текст",font=('Times New Roman', 16, "bold"))
        self.main_text.grid(row=0, column=0,columnspan=2)

        self.p_text = tk.Label(self,text="Вероятность \nошибки",font=('Times New Roman', 12))
        self.p_text.grid(row=1, column=0)

        self.p_ent = tk.Entry(self,width=20,font=('Times New Roman', 16, "bold"))
        self.p_ent.grid(row=1, column=1)

        self.btn_work = tk.Button(self,text="work",font=('Times New Roman', 14),
                                        height=2,width=25)
        self.btn_work.grid(row=2, column=0,columnspan=2)

        self.txt_log = tk.Text(self,width=40, height=30)
        self.txt_log.grid(row=3, column=0,columnspan=2)




if __name__ == '__main__':
    root = tk.Tk()
    app = Main(root)
    app.pack()

    root.title("Главное окно")
    root.geometry("1500x500")
    root.resizable(False, False)
    root.mainloop()
