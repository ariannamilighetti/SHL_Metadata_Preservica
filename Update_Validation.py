import tkinter as tk
from tkinter import ttk
from Metadata_Visualiser import Metadata_Visualiser

class Update_Validation(ttk.Frame):
    def __init__(self, metadata_visualiser):
        super().__init__()
        self.update_command()
        restart_button = tk.Button(self,text="Restart",width=25,command=lambda: self.restart(), bg='#ff8962')
        restart_button.grid(column=1, row=9, sticky='ew', padx=5, pady=5)
        self.metadata_visualiser = metadata_visualiser


    def get_file(self, list_option):
        if list_option == "Collections List":
            file = 'validation_files/collections_validation.txt'
        elif list_option == "Digitiser List":
            file = 'validation_files/digitiser_validation.txt'
        elif list_option == "Access List":
            file = 'validation_files/access_validation.txt'
        elif list_option == "Copyright Status List":
            file = 'validation_files/copyright_status.txt'
        elif list_option == "Rights Statements List" :
            file = 'validation_files/rights_statements.txt'
        elif list_option == "Restrictions List":
            file = 'validation_files/restriction_validation.txt'
        else:
            file = 'validation_files/empty.txt'
        
        return file

    def show_current_list(self, eventObject):
        list_option = eventObject.widget.get()  
        file = self.get_file(list_option) 
        self.data = self.list_box_contents(file)
        self.fill_listbox(self.data, self.current_list)
        return file 
        
    def get_selection(self):
        index = self.current_list.curselection()
        self.selected_item = self.current_list.get(index)
        self.update_value_entry.delete(0, 'end')
        self.update_value_entry.insert(0, self.selected_item)

    def show_options(self):
        options_label = tk.Label(self, text="Select the validation set to update")
        options_label.grid(column=0, row = 3, padx=5, pady=5, sticky='ew')
        choose_validation= tk.StringVar()
        options = ("Collections List", "Digitiser List", "Access List", "Copyright Status List", "Rights Statements List","Restrictions List")
        self.drop_menu= ttk.Combobox(self, textvariable=choose_validation)
        self.drop_menu['values']= options
        self.drop_menu['state']= 'readonly'
        self.drop_menu.grid(column=1, row=3, columnspan=2, sticky='ew', padx=5, pady=5)
        self.drop_menu.bind("<<ComboboxSelected>>", self.show_current_list)  
        self.current_list = tk.Listbox(self, width=60, height=5,selectmode=tk.SINGLE)
        self.current_list.grid(column=1, row=4, columnspan=2, rowspan=2, sticky='ew', padx=5, pady=5)
        self.search_str = tk.StringVar()
        search_label = tk.Label(master=self, text="Search", anchor='nw')
        search = tk.Entry(self, textvariable=self.search_str)
        search_label.grid(column=0,row=4, sticky='sew', padx=5, pady=5)
        search.grid(column=0,row=5, sticky='new', padx=5, pady=5)
        search.bind('<Return>', self.cb_search)
        
    def update_command(self):
        self.show_options()
        update_value_label = tk.Label(self, text="Value to update")
        self.update_value_entry = tk.Entry(self, width = 60)
        get_selection_button = tk.Button(self,text="Get from box", width=25, command=self.get_selection, bg = '#c9b8d2')    
        update_value_label.grid(column=0, row=7, sticky='e', padx=5, pady=5)
        self.update_value_entry.grid(column=1, row=7,sticky='ew', padx=5, pady=5)
        get_selection_button.grid(column = 2, row = 7, sticky= 'ew', padx=5, pady=5)
        value_updated_label = tk.Label(self, text="Enter updated value")
        self.value_updated_entry = tk.Entry(self, width = 60)
        value_updated_button = tk.Button(self,text="Confirm",width=25,command=lambda: self.update_file(self.update_value_entry.get(), self.value_updated_entry.get()), bg='#7fd1ae')  
        value_updated_label.grid(column=0, row=8, sticky='e', padx=5, pady=5)
        self.value_updated_entry.grid(column=1, row=8, columnspan=2, sticky='ew', padx=5, pady=5)
        value_updated_button.grid(column=2, row=9, sticky= 'ew', padx=5, pady=5)


    def update_file(self, old, new):
        selected_entry = self.drop_menu.get()
        file = self.get_file(selected_entry)
        filedata = []
        file_r = open(file, 'r', encoding='utf-8')
        for x, entry in enumerate(file_r):
            filedata.append(entry)
            if entry.replace("\n",'') == old.replace("\n",''):
                filedata[x] = (new + '\n')
            
        file_w = open(file, 'w')
        
        for i in filedata:
            file_w.write(i)
        file_w.close()
        self.success_label = tk.Label(self, text="Validation Updated")
        self.success_label.grid(column=2, row=10)
        self.metadata_visualiser.refresh()
        self.show_options()

    def restart(self):
        self.value_updated_entry.delete(0, 'end')
        self.update_value_entry.delete(0, 'end')
        self.success_label.destroy()

    def cb_search(self, event):
        sstr = self.search_str.get()
        self.current_list.delete(0, 'end')

        # If filter removed show all data
        if sstr == "":
            self.fill_listbox(self.data, self.current_list)
            return
    
        filtered_data = list()
        for item in self.data:
            if item.lower().find(sstr.lower())>= 0:
                filtered_data.append(item)
    
        self.fill_listbox(filtered_data, self.current_list)   

    def fill_listbox(self, item_list, lb):
        lb.delete(0,'end')
        for item in item_list:
            lb.insert('end', item)

    def list_box_contents(self, file):
        data = []
        f = open(file,"r")
        for x in f:
            data.append(x)
        f.close()
        return data
