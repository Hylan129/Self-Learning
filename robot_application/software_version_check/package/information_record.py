import csv

def csv_record(dict_contents,head):

    with open('files/dll_version_information.csv','a',newline='') as result_csv:
        write_csv = csv.writer(result_csv,dialect='excel')
        number = 0
        for dict_content in dict_contents:
            if number == 0:
                write_csv.writerow(head)
                try:
                    write_csv.writerow(dict_content.values())
                except Exception as identifier:
                    write_csv.writerow([head[0],'','','',dict_content]) 
                number = 1
            else:
                try:
                    write_csv.writerow(dict_content.values())
                except Exception as identifier:
                    write_csv.writerow([head[0],'','','',dict_content]) 