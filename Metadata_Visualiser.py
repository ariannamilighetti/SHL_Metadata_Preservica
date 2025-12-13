import tkinter as tk
from tkinter import ttk

class Metadata_Visualiser(tk.Frame):
    def __init__(self):
        super().__init__()

        self.frame = tk.Frame(self, bg='#f5f3f1')
        self.frame.pack(fill="both")
        
        self.table_titles_rows = 1
        self.search_button_row = 2
        self.list_row = 4
        self.instructions = tk.Label(master=self.frame, text='Use this page to check the data validation in the metadata creator. Select an item in the lists and ctrl+C to copy it. \nUse the search bar to search the collections list.', anchor="nw", justify='left')
        self.instructions.grid(row=0,column=0, columnspan=10, sticky='nw')
        self.refresh()

        self.frame.grid_columnconfigure(0, weight=0)
        self.frame.grid_columnconfigure(1, weight=0)
        self.frame.grid_columnconfigure(3, weight=0)
        self.frame.grid_columnconfigure(4, weight=0)
        self.frame.grid_columnconfigure(5, weight=0)
        self.frame.grid_columnconfigure(6, weight=0)
        self.frame.grid_columnconfigure(7, weight=0)
        self.frame.grid_columnconfigure(8, weight=0)
        self.frame.grid_columnconfigure(9, weight=0)
        self.frame.grid_columnconfigure(10, weight=0)

        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_rowconfigure(1, weight=0)
        self.frame.grid_rowconfigure(2, weight=0)
        self.frame.grid_rowconfigure(3, weight=1)
    
    def refresh(self):
        self.create_list("Digitised by", 'validation_files/digitiser_validation.txt', 2)
        self.create_list("Access Restriction", 'validation_files/access_validation.txt', 4)
        self.create_list("Restriction Type", 'validation_files/restriction_validation.txt', 6)
        self.create_list("Copyright Status", 'validation_files/copyright_status.txt', 8)
        self.create_list("Rights Statement", 'validation_files/rights_statements.txt', 10)
        self.create_collections("Collections", 'validation_files/collections_validation.txt', 0)

    def create_collections(self, title, file, column):
        self.coll_lb = tk.Listbox(self.frame, width=30, height=30)
        self.coll_lb.grid(column=column, row=self.list_row, columnspan=2)
        coll_label = tk.Label(master=self.frame, text=title, anchor='nw')
        coll_label.grid(column=column, row=self.table_titles_rows, columnspan=2)
        self.coll_data = self.list_box_contents(file)
        self.fill_listbox(self.coll_data, self.coll_lb)
        if title == "Collections":
            self.search_str = tk.StringVar()
            search_label = tk.Label(master=self.frame, text="Search", anchor='nw')
            search = tk.Entry(self.frame, textvariable=self.search_str)
            search_label.grid(column=column,row=self.search_button_row)
            search.grid(column=column+1,row=self.search_button_row)
            search.bind('<Return>', self.cb_search)

    def create_list(self, title, file, column):
        self.Lb = tk.Listbox(self.frame, height=30)
        self.Lb.grid(column=column, row=self.list_row, columnspan=2)
        coll_label = tk.Label(master=self.frame, text=title, anchor='nw')
        coll_label.grid(column=column, row=self.table_titles_rows, columnspan=2)
        self.coll_data = self.list_box_contents(file)
        self.fill_listbox(self.coll_data, self.Lb)


    def cb_search(self, event):
        sstr = self.search_str.get()
        self.coll_lb.delete(0, 'end')

        # If filter removed show all data
        if sstr == "":
            self.fill_listbox(self.coll_data, self.coll_lb)
            return
    
        filtered_data = list()
        for item in self.coll_data:
            if item.lower().find(sstr.lower())>= 0:
                filtered_data.append(item)
    
        self.fill_listbox(filtered_data, self.coll_lb)   

    def fill_listbox(self, item_list, lb):
        lb.delete(0,'end')
        for item in item_list:
            lb.insert('end', item)

    def list_box_contents(self, file):
        data = []
        f = open(file,"r", encoding='utf-8')
        for x in f:
            data.append(x)
        f.close()
        return data

# to test this class
def __main__():
    app = tk.Tk()
    tabs = ttk.Notebook(app)
    tabs.grid(row=1, column= 0, sticky="nsew")
    # Create Tabs
    data_input = Metadata_Visualiser()
    tabs.add(data_input, text='From Input')
    tk.mainloop()

if __name__ == '__main__':
    __main__()
