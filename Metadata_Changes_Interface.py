import tkinter as tk
from tkinter import ttk
from Update_Validation import Update_Validation as UV
from Add_Validation import Add_Validation as AV
from Remove_Validation import Remove_Validation as RV

class Metadata_Changes(ttk.Frame):
    def __init__(self, metadata_visualiser):
        super().__init__()
        self.instructions_label = 0
        self.table_titles_rows = 1
        self.search_button_row = 2
        self.list_row = 4

        self.instructions = tk.Label(master=self, text='Use this tab to add an entry to the data validation in the metadata creator. \nUse the search bar to search the collections list.', anchor="w", justify='left')
        self.instructions.grid(column=0, row=0, sticky='nw')

        options = ttk.Notebook(self)
        options.grid(column=0, row=1, sticky='nw', padx=5, pady=5)

        update = UV(metadata_visualiser)
        options.add(update, text="Update Validation Value")
        adder = AV(metadata_visualiser)
        options.add(adder, text='Add New Validation Option')
        remover = RV(metadata_visualiser)
        options.add(remover, text='Remove A Value')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=0)
        self.grid_rowconfigure(6, weight=0)
        self.grid_rowconfigure(7, weight=0)
        self.grid_rowconfigure(8, weight=0)
        self.grid_rowconfigure(9, weight=0)
    

def __main__():
    app = tk.Tk()
    tabs = ttk.Notebook(app)
    tabs.grid(row=1, column= 0, sticky="nsew", padx=5, pady=5)
    # Create Tabs
    data_input = Metadata_Changes()
    tabs.add(data_input, text='From Input')
    tk.mainloop()

if __name__ == '__main__':
    __main__()