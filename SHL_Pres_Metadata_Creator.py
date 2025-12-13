import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from From_Spreadsheet import From_Spreadsheet
from From_Input import From_Input
from Metadata_Visualiser import Metadata_Visualiser
from Metadata_Changes_Interface import Metadata_Changes
from ttkthemes import ThemedTk
import webbrowser

def callback(url):
    webbrowser.open_new_tab(url)

# Create window
app = ThemedTk(theme='radiance')
app.title("SHL Preservica Metadata and Folder Structure Creator")
app.minsize(630, 220)
#app.geometry('850x450')
#ttk.Style().theme_use('Breeze')
app.option_add("*Label*Background", "#f5f3f1")
app.option_add("*Radiobutton*Background", "#f5f3f1")
app.option_add('**Background', "#f5f3f1")
app.option_add('*Entry*Background', '#FFFFFF')
app.option_add('*ComboBox*Background', '#FFFFFF')
app['bg'] = "#f5f3f1"
app.configure(bg="#f5f3f1")

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=0)
app.grid_rowconfigure(0, weight=0)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=0)

title_lbl = tk.Label(master=app, text="SHL Metadata Creator", anchor="w", font = (20))
title_lbl.grid(row=0, column = 0, sticky="nw")

app_footer = tk.Label(master=app, text='Created by Arianna Milighetti, Digitisation Coordinator, Senate House Library. Documentation available on SHL Digitisation SharePoint site. Created July 2025.', anchor='w', font=('Arial', 8))
app_footer.grid(row=2, column=0, sticky='nwse')

content_frame = tk.Frame(app)

content_frame.grid(column=0, row=1, sticky='nwe')
content_frame.columnconfigure(0, weight=1)
content_frame.rowconfigure(0, weight=0)
content_frame.rowconfigure(1, weight=1)

instr_lbl = tk.Label(master=content_frame, text="To create a new metadata xml, choose either 'From Spreadsheet' or 'From Input'. \nTo view the current data validation settings, choose 'Data Validation'. \nTo update the data validation choose 'Update Data Validation'.", anchor="nw", justify='left')
instr_lbl.grid(row=0, column= 0, sticky="ew", padx=5)

template_label = tk.Label(master=content_frame, text="Full documentation can be found here:")
link = tk.Label(content_frame, text="SHL Digitisation Sharepoint > Preservica Wiki", fg='blue', cursor="hand2")
template_label.grid(column=0, row=1, sticky="nw", padx=5)
link.grid(column=0, row=2, sticky="nw", padx=5)
link.bind("<Button-1>", lambda e: callback("https://uolonline.sharepoint.com/:u:/r/sites/shl/bd/SitePages/Preservica-Ops.aspx?csf=1&web=1&e=tOpnW7"))

tabs = ttk.Notebook(content_frame)
tabs.grid(row=3, column= 0, sticky="ew", padx=5)

# Create Tabs
ssheet = From_Spreadsheet()
tabs.add(ssheet, text='From Spreadsheet')
data_input = From_Input()
tabs.add(data_input, text='From Input')
metadata_visualiser = Metadata_Visualiser()
tabs.add(metadata_visualiser, text='View Data Validation')
metadata_update_tab = Metadata_Changes(metadata_visualiser)
tabs.add(metadata_update_tab, text="Update Data Validation")

tk.mainloop()