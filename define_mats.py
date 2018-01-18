import tkinter as tk
import os

class gui(tk.Frame):
    def __init__(self,master):       
        tk.Frame.__init__(self,master)
        self.master = master
        self.frame_lb = tk.Frame(self.master)
        
        self.label_domains = tk.Label(self.frame_lb,text='Domains')
        self.lb_domains = tk.Listbox(
                self.frame_lb,
                height=20,
                width=30,
                exportselection=0,
                selectmode='extended',
                activestyle='none')
        self.label_materials = tk.Label(self.frame_lb,text='Materials')
        self.lb_materials = tk.Listbox(
                self.frame_lb,
                height=20,
                width=30,
                activestyle='none')
        
        self.lb_domains_scrollbar = tk.Scrollbar(self.frame_lb)
        self.lb_domains_scrollbar.config(command=self.lb_domains.yview)
        self.lb_materials_scrollbar = tk.Scrollbar(self.frame_lb)
        self.lb_materials_scrollbar.config(command=self.lb_materials.yview)
        
        self.button_import = tk.Button(self.frame_lb,text='Import',height=2)
        self.button_write = tk.Button(self.frame_lb,text='Write',height=2)
        
class AppDefineMats(tk.Frame):
    def __init__(self,master):       
        tk.Frame.__init__(self,master)
        self.master = master
        self.master.option_add("*Font", "Arial 12")
        
        self.lb = gui(self)
        self.lb.frame_lb.pack(fill='both',expand=1,padx=5,pady=5)
        self.lb.label_domains.grid(row=1,column=1,sticky='W')
        self.lb.lb_domains.grid(row=2,column=1,sticky='NSEW')
        self.lb.lb_domains_scrollbar.grid(row=2,column=2,sticky='NSEW')
        self.lb.label_materials.grid(row=1,column=3,sticky='W')
        self.lb.lb_materials.grid(row=2,column=3,sticky='NSEW')
        self.lb.lb_materials_scrollbar.grid(row=2,column=4,sticky='NSEW')
        
        self.lb.button_import.grid(row=3,column=1,columnspan=4,sticky='NSEW')
        self.lb.button_write.grid(row=4,column=1,columnspan=4,sticky='NSEW')
        
        self.lb.button_import.config(command=self.cmd_select_file)
        self.lb.button_write.config(command=self.cmd_export_data)
        self.lb.button_write.config(state='disabled')
        
        self.lb.lb_domains.bind('<<ListboxSelect>>',self.cmd_select_dom)
        
    def cmd_select_file(self):
        selected = tk.filedialog.askopenfilename(
                title='Choose the .ccl file',
                filetypes=(("CFX Command file", "*.ccl"),("All files", "*.*")))
        
        if selected:
            self.inputfile_fullpath = selected
            self.inputfile_name = os.path.basename(self.inputfile_fullpath)
            self.inputfile_dir_name = os.path.dirname(self.inputfile_fullpath)
            self.inputfile_ext = os.path.splitext(self.inputfile_fullpath)[1]
            self.get_data()
        else:
            return
    
    def get_data(self):
        self.raw_data = []
        self.domains = []
        self.materials = []
        self.df = {}
        self.lb.lb_domains.delete(0,'end')
        self.lb.lb_materials.delete(0,'end')
        
        with open(self.inputfile_fullpath) as f:
            for line in f:
                line = line.strip()
                self.raw_data.append(line)
        
        for idx,line in enumerate(self.raw_data):
            if 'DOMAIN:' in line:
                fidx = idx
                dom = line.split(': ')[1]
                self.domains.append(dom)
                for idx,line in enumerate(self.raw_data[fidx:]):
                    if 'Material = ' in line:
                        self.df[dom] = line.split(' = ')[1]
                        self.materials.append(line.split(' = ')[1])
                        break
                        
        self.materials = set(self.materials)  
        for dom in self.domains:
            self.lb.lb_domains.insert('end',dom)
        for mat in self.materials:
            self.lb.lb_materials.insert('end',mat)
    
    def cmd_select_dom(self,*args):
        self.lb.lb_materials.selection_clear(0,'end') 
        if len(self.lb.lb_domains.curselection()) == 1:
            self.lb.lb_materials.selection_clear(0,'end')  
            selected_dom = self.domains[self.lb.lb_domains.curselection()[0]]
            selected_mat = self.df[selected_dom]
            
            for idx,mat in enumerate(self.materials):
                if mat == selected_mat:
                    self.lb.lb_materials.select_set(idx)
        else:    
            return
      
    def cmd_export_data(self):
        pass
              
        
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Define material for domains')
    AppDefineMats(root).pack()
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()