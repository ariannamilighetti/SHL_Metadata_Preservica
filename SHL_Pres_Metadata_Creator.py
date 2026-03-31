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
#app.grid_columnconfigure(1, weight=0)
app.grid_rowconfigure(0, weight=0)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=0)

title_lbl = tk.Label(master=app, text="SHL Metadata Creator", anchor="w", font = (20))
title_lbl.grid(row=0, column = 0, sticky="nw")

app_footer = tk.Label(master=app, text='Created by Arianna Milighetti, Digitisation Coordinator, Senate House Library. Documentation available on SHL Digitisation SharePoint site. Created July 2025.', anchor='w', font=('Arial', 8))
app_footer.grid(row=2, column=0, sticky='nwse')

frame = ttk.Frame(app)
frame.grid(row=1, column=0, sticky='nwse')
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=0)
frame.rowconfigure(0, weight=1)
frame.rowconfigure(1, weight=0)

canvas = tk.Canvas(frame)
scrollbarv = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollbarh = ttk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
#canvas.columnconfigure(0, weight=1)
#canvas.rowconfigure(0, weight=1)

content_frame = ttk.Frame(canvas)
content_frame.bind("<Configure>", lambda e : canvas.configure(
    width=e.width, scrollregion=canvas.bbox('all')))

canvas.create_window((0, 0), window=content_frame, anchor="center")
canvas.configure(yscrollcommand=scrollbarv.set)
canvas.configure(xscrollcommand=scrollbarh.set)
canvas.grid(row=0, column=0, sticky="nsew")
scrollbarv.grid(row=0, column=1, sticky="ns")
scrollbarh.grid(row=1, column=0, sticky="ew")

content_frame.grid(column=0, row=0, sticky='nwse')
content_frame.columnconfigure(0, weight=1)
content_frame.rowconfigure(0, weight=0)
content_frame.rowconfigure(1, weight=0)
content_frame.rowconfigure(2, weight=0)
content_frame.rowconfigure(3, weight=1)
frame.update()

instr_lbl = tk.Label(master=content_frame, text="To create a new metadata xml, choose either 'From Spreadsheet' or 'From Input'. To view the current data validation settings, choose 'Data Validation'. To update the data validation choose 'Update Data Validation'.", anchor="nw", justify='left')
instr_lbl.bind('<Configure>', lambda e: instr_lbl.config(wraplength=(frame.winfo_width())-20))
instr_lbl.grid(row=0, column= 0, sticky="ew", padx=5)

template_label = tk.Label(master=content_frame, text="Full documentation can be found here:")
link = tk.Label(content_frame, text="SHL Digitisation Sharepoint > Preservica Wiki", fg='blue', cursor="hand2")
template_label.grid(column=0, row=1, sticky="nw", padx=5)
link.grid(column=0, row=2, sticky="nw", padx=5)
link.bind("<Button-1>", lambda e: callback("https://uolonline.sharepoint.com/:u:/r/sites/shl/bd/SitePages/Preservica-Ops.aspx?csf=1&web=1&e=tOpnW7"))

'''tab_frame = ttk.Frame(master=content_frame)
tab_frame.grid(row=3, column= 0, sticky="ew", padx=5)
tab_frame.columnconfigure(0,weight=1)
tab_frame.rowconfigure(0,weight=1)'''

tabs = ttk.Notebook(content_frame)
tabs.grid(row=0, column= 0, sticky="ew", padx=5)
tabs.columnconfigure(0, weight=1)
tabs.rowconfigure(0,weight=1)

# Create Tabs
ssheet = From_Spreadsheet(master=tabs)
tabs.add(ssheet, text='From Spreadsheet')
data_input = From_Input(master=tabs)
tabs.add(data_input, text='From Input')
metadata_visualiser = Metadata_Visualiser(master=tabs)
tabs.add(metadata_visualiser, text='View Data Validation')
metadata_update_tab = Metadata_Changes(metadata_visualiser,master=tabs)
tabs.add(metadata_update_tab, text="Update Data Validation")

def _on_mousewheel(event):
   canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

tk.mainloop()