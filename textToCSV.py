import os
import csv
import pandas as pd

def convert():
    txt_dir = 'F:/Users/chris/OneDrive - University of Sussex/Year3/Project/Email Anti Scam-Spam Bot/Controller/PreProcessor/Spam Folder'

    file_list = list(os.scandir(txt_dir))
    txt_file_list = list(filter(lambda x: x.path.endswith('.txt'), file_list))
    csv_lines = []
    i=0

    for f in txt_file_list:
        with open(f, 'r',encoding="utf8") as email:
            try:
                body=''
                data = email.readlines()
                for line in data:
                    if line.__contains__("Subject:"):
                        subject=line
                    elif line.__contains__("From:"):
                        address=line
                    else:
                        body= body + line
            except:
                print("UnicodeDecodeError")
                subject,body,address=[],[],[]
        #  process file here, add to csv_lines
            csv_lines.append([subject,address,[],[],"spam",1])
        i=i+1
        print(i)

    #Output:
    headers = ['Email Subject', 'Email Address', 'Email Body','','label','label_num']
    #print(csv_lines)
    df = pd.DataFrame(csv_lines)
    df.columns = (headers)
    df.to_csv('processedEmails.csv')

convert()