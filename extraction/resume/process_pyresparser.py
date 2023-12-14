from pyresparser import ResumeParser
import os

def process_and_save(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    for file_name in files:
        input_file_path = os.path.join(input_folder, file_name)
        output_file_path = os.path.join(output_folder, file_name[0:-4]+'.txt')
        output_data = process_file(input_file_path)

        with open(output_file_path, 'w') as output_file:
            for i in output_data:
                output_file.write(i+'\n')

def process_file(file_path):
    data = ResumeParser(file_path).get_extracted_data()

    data1=data['skills']
    data2=data['experience']
    data3=data['degree']
    
    if data2!=None:
        data1.extend(data2)
    if data3!=None:
        data1.extend(data3)
    return data1

pdf_folder_path = 'resume_pdf'
output_folder_path = 'output_pyresparser'
process_and_save(pdf_folder_path, output_folder_path)
