import tkinter as tk

class gui(tk.Frame):
    def __init__(self,master):       
        tk.Frame.__init__(self,master)
        self.master = master
        self.frame_lb = tk.Frame(self.master)
        
        self.label_domains = tk.Label(self.frame_lb,text='Domains')
        self.lb_domains = tk.Listbox(self.frame_lb,height=20,width=30)
        self.label_materials = tk.Label(self.frame_lb,text='Materials')
        self.lb_materials = tk.Listbox(self.frame_lb,height=20,width=30)


class AppDefineMats(tk.Frame):
    def __init__(self,master):       
        tk.Frame.__init__(self,master)
        self.master = master
        self.master.option_add("*Font", "Arial 12")
        
        self.lb = gui(self)
        self.lb.frame_lb.pack(fill='both',expand=1)
        self.lb.label_domains.grid(row=1,column=1)
        self.lb.lb_domains.grid(row=2,column=1)
        self.lb.label_materials.grid(row=1,column=2)
        self.lb.lb_materials.grid(row=2,column=2)
              
        
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Define material for domains')
    AppDefineMats(root).pack()
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()