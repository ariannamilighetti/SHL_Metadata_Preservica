import os
from datetime import datetime
from lxml import etree

def read_file(file):
    metadata_file = open(file, 'r', encoding='utf-8')
    validations = metadata_file.readlines()
    metadata_file.close()
    return validations

def check_validation(text, file):
    validations = read_file(file)
    found = False
    for entry in validations:
        if str(text).lower().rstrip() in str(entry).lower().rstrip():
            found = True
            return [found, entry]
    
    if not found:
        return [found, text + " is not validated."]
    
def validate_access_rights(text, cop_status, file):
    validations = read_file(file)
    found = False
    if cop_status.rstrip() == "No known copyright":
        applied_validations = [validations[0]]
    elif cop_status.rstrip() == "In copyright - UoL":
        applied_validations = [validations[1], validations[2], validations[3], validations[4], validations[5],validations[12]]
    elif cop_status.rstrip() == "In copyright - third party":
        applied_validations = [validations[1], validations[2], validations[3], validations[4], validations[5],validations[6], validations[7], validations[8], validations[12], validations[13]]
    elif cop_status.rstrip() == "Copyright undetermined":
        applied_validations = ['']
    elif cop_status.rstrip() == "Copyright not evaluated":
        applied_validations = ['']
    elif cop_status.rstrip() == "Mixed":
        applied_validations = ['']
    elif cop_status.rstrip() == "No known copyright but other legal / contractual / ethical restrictions apply":
        applied_validations = [validations[9], validations[10], validations[11]]
    else:
        applied_validations = ['Not Found']

    for entry in applied_validations:
        if str(text).lower().rstrip() in str(entry).lower().rstrip():
            found = True
            return [found, entry.rstrip()]
    if not found:
        return [found, text + " is not validated."]


def create_sub_f(folder):
    directory = os.fsencode(folder)
    try: 
        if len(os.listdir(directory)) > 0:
            top_dir = folder + '/' + str(datetime.now().strftime("%Y%m%d%H%M%S%f"))
            os.mkdir(top_dir)
            rep_dir = top_dir + '/' + os.path.basename(folder) + '.pax'
            os.mkdir(rep_dir)
            rep_pres_dir = rep_dir + '/Representation_Preservation'
            os.mkdir(rep_pres_dir)
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                old_dir = folder + "/" + filename
                if filename.endswith(('.tif', '.TIF', '.TIFF', '.tiff', '.jpg', '.jpeg', '.JPG', '.JPEG', '.pdf', '.PDF')) :
                    new_dir = rep_pres_dir + "/" + filename.split(".")[0] 
                    os.mkdir(new_dir)
                    os.rename(old_dir, new_dir + "/" + filename)
                else:
                    continue
            label = "Complete"
        else:
             label = "Empty Directory"
    except Exception as err:
            top_dir = "not found"
            label = Exception, err
    return [label, top_dir]

def create_xml(metadata, folder):
    ns1 = 'http://www.openpreservationexchange.org/opex/v1.0'
    ns2 = 'http://www.preservica.com/metadata/group/digitised_images'
    label = []
    all_valid = True

    OPEXMetadata = etree.Element('OPEXMetadata', nsmap = {'opex' : ns1})
    descr_metadata = etree.SubElement(OPEXMetadata, 'DescriptiveMetadata')    
    digitised_images = etree.SubElement(descr_metadata, 'digitised_images', nsmap = { None: ns2 , 'xsi' : "http://www.w3.org/2001/XMLSchema-instance"})
    title = etree.SubElement(digitised_images, 'title')
    title.text = metadata[1].rstrip()

    classmark = etree.SubElement(digitised_images, 'classmark')
    classmark.text = metadata[2].rstrip()

    catalogue_number = etree.SubElement(digitised_images, 'catalogue_number')
    catalogue_number.text = metadata[3].rstrip()

    valid_collection = check_validation(metadata[4].rstrip(), 'validation_files/collections_validation.txt')
    if  valid_collection[0]:
        collection = etree.SubElement(digitised_images, 'collection')
        collection.text = valid_collection[1].rstrip()
        label.append(["Collection validated", '#73bb5b'])
    else:
        label.append([valid_collection[1], '#c54f66'])
        all_valid = False

    valid_digitised_by = check_validation(metadata[5].rstrip(), 'validation_files/digitiser_validation.txt')
    if  valid_digitised_by[0]:
        digitised_by = etree.SubElement(digitised_images, 'digitised_by')
        digitised_by.text = valid_digitised_by[1].rstrip()
        label.append(["'Digitised by' validated", '#73bb5b'])
    else:
        label.append([valid_digitised_by[1], '#c54f66'])
        all_valid = False

    digitisation_date = etree.SubElement(digitised_images, 'digitisation_date')
    digi_date_str = metadata[6].rstrip()
    digitisation_date.text = digi_date_str

    valid_access_conditions = check_validation(metadata[7].rstrip(), 'validation_files/access_validation.txt')
    if  valid_access_conditions[0]:
        access_conditions = etree.SubElement(digitised_images, 'access_conditions')
        access_conditions.text = valid_access_conditions[1].rstrip()
        label.append(["Access Conditions validated", '#73bb5b'])
    else:
        label.append([valid_access_conditions[1], '#c54f66'])
        all_valid = False

    valid_restriction_reason = check_validation(metadata[8].rstrip(), 'validation_files/restriction_validation.txt')
    if  valid_restriction_reason[0]:
        restriction_reason = etree.SubElement(digitised_images, 'restriction_reason')
        restriction_reason.text = valid_restriction_reason[1].rstrip()
        label.append(["Restriction Reason validated", '#73bb5b'])
    else:
        label.append([valid_restriction_reason[1], '#c54f66'])
        all_valid = False

    restriction_expiry_date = etree.SubElement(digitised_images, 'restriction_expiry_date')
    restr_date_str = metadata[9].rstrip()
    restriction_expiry_date.text = restr_date_str

    valid_copyright_status = check_validation(metadata[10].rstrip(), 'validation_files/copyright_status.txt')
    if  valid_copyright_status[0]:
        copyright_status = etree.SubElement(digitised_images, 'copyright_status')
        copyright_status.text = valid_copyright_status[1].rstrip()
        label.append(["Copyright Status validated", '#73bb5b'])
    else:
        label.append([valid_copyright_status[1], '#c54f66'])
        all_valid = False

    valid_rights_statement = validate_access_rights(metadata[11].rstrip(), valid_copyright_status[1],'validation_files/rights_statements.txt')
    if  valid_rights_statement[0]:
        rights_statement = etree.SubElement(digitised_images, 'conditions_of_use')
        rights_statement.text = valid_rights_statement[1].rstrip()
        label.append(["Rights Statement validated", '#73bb5b'])
    else:
        label.append([valid_rights_statement[1], '#c54f66'])
        all_valid = False

    licence_details = etree.SubElement(digitised_images, 'licence_details')
    licence_details.text = metadata[12].rstrip()

    xml_barcode = etree.SubElement(digitised_images, 'barcode')
    barcode = str(metadata[0]).split("(")
    print(barcode)
    xml_barcode.text = barcode[0].rstrip()

    if all_valid:
        folder_and_label = create_sub_f(folder)
        if folder_and_label[0] == "Complete":
            label.append(["Folder structure created",'#73bb5b'])
            file_name =  folder_and_label[1] + '/' + str(metadata[0]).rstrip() + '.pax.opex'
            with open(file_name, 'wb') as f:
                full_xml = etree.tostring(OPEXMetadata, encoding="UTF-8", standalone = "yes", xml_declaration=True, pretty_print=True).decode()
                print(type(full_xml))
                for r in (("OPEXMetadata", "opex:OPEXMetadata"), ("DescriptiveMetadata", "opex:DescriptiveMetadata")):
                    full_xml = full_xml.replace(*r)
                f.write(full_xml.encode())
            label.append(["Success!", '#73bb5b'])
        else:
            error = folder_and_label[0]
            label.append([error, '#c54f66'])
            label.append(["Process failed", '#c54f66'])
    else:
        label.append(["Metadata not valid, folder not created", '#c54f66'])
        label.append(["Process failed", '#c54f66'])
    return label

def create_metadata(folder, metadata, frame):
    labels = create_xml(metadata, folder)
    return labels

if __name__ == 'main':
    create_metadata(os.getcwd(), "a", "b")