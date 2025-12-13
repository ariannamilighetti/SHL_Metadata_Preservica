# Preservica Ingest Metadata
This program creates a XML file in the OPEX standard to bulk ingest items into [Preservica](https://preservica.com/) as Bookviewer items.

The program takes as input a spreadsheet with the metadata in the format shown in the file "template.xlsx", and a folder of folders, where each subsolfer contains the images relating to one representation and is named with the item's barcode. Alternatively to the Excel file, the data can be input manually item-by-item in the "From Input" tab of the program.

The program rewrites folder in the format required by preservica:
- timestamped folder
  - barcode.opex.xml [metadata file]
  - barcode folder
    - one folder for each image of the representation
      - image
     
## Data Validation
To allow for data validation before ingest, the program contains data validation updates options. These are stored in .txt files within the "validation_files" folder. The validation can be updated within the program in the data validation tabs.
