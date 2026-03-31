import metadata_creator
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class From_Input(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.scrollFrame = tk.Frame(self)
        self.scrollFrame.pack(fill='both', anchor='center', expand=True)
        self.selection_frm = ttk.LabelFrame(self.scrollFrame, text="Items details")
        self.selection_frm.pack(fill="x", padx=5, pady=5)
        self.row_count = 0
        
        reference = self.input_fields('Input item(s) reference') # barcode
        title = self.input_fields( 'Title') # Title
        classmark = self.input_fields('Classmark') # Classmark
        cat_number = self.input_fields('Catalogue Number') # Catalogue Number
        collection = self.dropdown_field('Collection', 'validation_files/collections_validation.txt') # Collection
        digitiser = self.dropdown_field('Digitiser', 'validation_files/digitiser_validation.txt') # Digitiser
        digi_date = self.input_fields('Digitisation Date, yyyy-mm-dd') # Digitisation Date
        acc_condition = self.dropdown_field('Access Conditions', 'validation_files/access_validation.txt') # Access Conditions
        restriction = self.dropdown_field('Restriction Reason', 'validation_files/restriction_validation.txt') # Restriction Reason
        restriction_exp = self.input_fields('Restriction Expiry Date, yyyy-mm-dd') # Restriction Exp Date
        copyright = self.dropdown_field('Copyright Status', 'validation_files/copyright_status.txt') # Copyright Status
        r_statements = self.dropdown_field('Rights Statements', 'validation_files/rights_statements.txt') # Copyright Statement
        licence = self.input_fields('Licence Details') # Licence Details

        self.all_fields = [reference, title, classmark, cat_number, collection, digitiser, digi_date, acc_condition, restriction, restriction_exp, copyright, r_statements, licence]
        self.folder_fileds()
        self.run_button()
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight =1)
        self.selection_frm.columnconfigure(0, weight = 1)
        self.selection_frm.columnconfigure(1, weight = 0)
        self.selection_frm.columnconfigure(2, weight = 2)

    def input_fields(self, title):
        label = tk.Label(master=self.selection_frm, text=title, anchor='nw')
        input = tk.Entry(master=self.selection_frm, width = 50)
        label.grid(column=0, row=self.row_count, columnspan=1, sticky="nsew", padx=5, pady=5)
        input.grid(column=2, row=self.row_count, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.row_count += 1
        return input
  
    def dropdown_field(self, title, file):
        label = tk.Label(master=self.selection_frm, text=title, anchor='nw')
        entry = ttk.Combobox(master=self.selection_frm, state="readonly",
                             width = 50, values = self.list_box_contents(file))
        label.grid(column=0, row=self.row_count, columnspan=1, sticky="nsew", padx=5, pady=5)
        entry.grid(column=2, row=self.row_count, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.row_count += 1
        entry.unbind_class("TCombobox", "<MouseWheel>")
        return entry

    def input_metadata(self):
        metadata_array = []
        for item in self.all_fields:
            metadata_array.append(item.get())
        folder = self.folder_dir_label.get()
        row = 0
        outcome_frame = tk.Frame(self.scrollFrame)
        outcome_frame.pack(fill='both', expand=True)
        barcode_l = tk.Label(outcome_frame, text='Barcode')
        barcode_l.grid( row=row, column = 0, padx=8, pady=5)
        collection_l = tk.Label(outcome_frame, text='Collection')
        collection_l.grid(row=row, column = 1, padx=8, pady=5)
        digitised_by_l = tk.Label(outcome_frame, text='Digitised By')
        digitised_by_l.grid(row=row, column = 2, padx=8, pady=5)
        access_cond_l = tk.Label(outcome_frame, text='Access Conditions')
        access_cond_l.grid(row=row, column = 3, padx=8, pady=5)
        restr_reason_l = tk.Label(outcome_frame, text='Restriction Reason')
        restr_reason_l.grid(row=row, column = 4, padx=8, pady=5)
        cop_status_l = tk.Label(outcome_frame,  text='Copyright Status')
        cop_status_l.grid(row=row, column = 5, padx=8, pady=5)
        rights_stat_l = tk.Label(outcome_frame, text='Rights Statement')
        rights_stat_l.grid(row=row, column = 6, padx=8, pady=5)
        folder_l = tk.Label(outcome_frame, text='Folder')
        folder_l.grid(row=row, column = 7, padx=8, pady=5)
        succ_l = tk.Label(outcome_frame, text='Overall Success')
        succ_l.grid(row=row, column = 8, padx=8, pady=5)

        column = 0
        row += 1
        labels = metadata_creator.create_metadata(folder, metadata_array, self)
        barcode_label = tk.Label(outcome_frame, text=metadata_array[0])
        barcode_label.grid(row=row, column = column)
        for i in labels:
            column += 1
            label = tk.Label(outcome_frame,  text=i[0], wraplength=100, background=i[1])
            label.grid(row=row, column=column, padx=8, pady=5)


    def list_box_contents(self, file):
        data = []
        f = open(file,"r")
        for x in f:
            data.append(x)
        f.close()
        return data

    def folder_fileds(self):
        # Folder Fields
        dir_label = tk.Label(master=self.selection_frm, text="Select item(s) parent folder", anchor='nw')
        dir_button = tk.Button(self.selection_frm, text='Open', command=self.askDirectory_ss, bg='#ff8962')
        self.folder_dir_label = tk.Entry(master=self.selection_frm)
        dir_label.grid(column=0, row=13, columnspan=1, sticky="nsew", padx=5, pady=5)
        dir_button.grid(column=1, row=13, columnspan=1, sticky="nsew", padx=5, pady=5)
        self.folder_dir_label.grid(column=2, row=13, columnspan=3, sticky="nsew", padx=5, pady=5)

    def askDirectory_ss(self, event=None):
        global end_directory
        end_directory = filedialog.askdirectory()
        self.folder_dir_label.delete(0, "end")
        self.folder_dir_label.insert(0, end_directory)
   
    def run_button(self):
        run_button = tk.Button(self.scrollFrame, text="Run", command=
                               lambda: self.input_metadata(), bg='#7fd1ae')
        run_button.pack(fill="x", padx=5, pady=5)

    def complete_label(self, label) :
        complete_label = tk.Label(self, text=label)
        complete_label.pack(fill="x", padx=5, pady=5)


# to test this class
def __main__():
    app = tk.Tk()
    tabs = ttk.Notebook(app)
    tabs.grid(row=1, column= 0, sticky="nsew")
    # Create Tabs
    data_input = From_Input(master=tabs)
    tabs.add(data_input, text='From Input')
    tk.mainloop()

if __name__ == '__main__':
    __main__()