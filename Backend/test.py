# if __name__ == '__main__':
#     logfile = open("C:\\Users\\Hp\\Desktop\\CIC\\test.txt", "r")
#     loglines = follow(logfile)
#     for line in loglines:
#         # sys.stdout.write(line)
#         # sys.stdout.flush()
#         print(line[:-1])

# import pandas as pd
# import time
# import ast
# import sys

# def follow(thefile):
#     thefile.seek(0, 2)
#     while True:
#         line = thefile.readline()
#         if not line:
#             time.sleep(0.1)
#             continue
#         yield line

# if __name__ == '__main__':
#     logfile = open("C:\\Users\\Hp\\Desktop\\CIC\\Book1.csv", "r")
#     loglines = follow(logfile)

#     #empty dataframe
#     column_names = ['totlen_fwd_pkts','pkt_len_mean', 'flow_byts_s', 'ack_flag_cnt', 'pkt_len_min', 'dst_port', 'fwd_iat_min', 'bwd_pkts_s', 'bwd_pkt_len_std',
# 'init_fwd_win_byts', 'bwd_iat_min', 'init_bwd_win_byts', 'idle_min', 'totlen_bwd_pkts', 'flow_duration', 'flow_iat_min',
# 'bwd_pkt_len_mean', 'pkt_len_std', 'bwd_header_len', 'flow_iat_max', 'fwd_seg_size_min', 'flow_iat_mean', 'fwd_pkt_len_max',
# 'fwd_iat_mean', 'flow_pkts_s', 'fwd_header_len']
    
#     while True: 

#         for flowline in loglines:
#             flowline = flowline.strip()
#             # sys.stdout.write(flowline)
#             # sys.stdout.flush()
        
#             dfArray = list(flowline.split(","))#"1,2,3,4" will be split using commas in to a list : ['1', '2', '3', '4'].
#             # print(dfArray)
#             data_filtered = [sublist for sublist in dfArray if sublist != [['']]]
#             columns_indices = [12, 24, 7, 49, 23, 2, 40, 9, 21, 58, 42, 59, 53, 13, 5, 35, 22, 25, 28, 36, 30, 33, 15, 42, 8, 27]

#             extracted_columns = [[row[index] for index in columns_indices] for row in data_filtered]
#             # data_filtered = data_filtered.split("]]\n[[")
#             # #remove empty lists and form the finalList
#             # finalList = [ast.literal_eval(part) for part in data_filtered if part != ""]
#             # print(extracted_columns)
#             df = pd.DataFrame(extracted_columns, columns=column_names)
#             print(df)

import pandas as pd
import time
import joblib
import threading
import os

##
def follow(thefile):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

if __name__ == '__main__':
    #start auto_save.py
    auto_save_thread = threading.Thread(target=lambda: os.system('python auto_save.py'))
    auto_save_thread.start()

    logfile = open("C:\\Users\\Hp\\Desktop\\CIC\\Book1.csv", "r")
    loglines = follow(logfile)

    
    column_names = ['totlen_fwd_pkts', 'pkt_len_mean', 'flow_byts_s', 'ack_flag_cnt', 'pkt_len_min', 'dst_port', 'fwd_iat_min',
                    'bwd_pkts_s', 'bwd_pkt_len_std', 'init_fwd_win_byts', 'bwd_iat_min', 'init_bwd_win_byts', 'idle_min',
                    'totlen_bwd_pkts', 'flow_duration', 'flow_iat_min', 'bwd_pkt_len_mean', 'pkt_len_std', 'bwd_header_len',
                    'flow_iat_max', 'fwd_seg_size_min', 'flow_iat_mean', 'fwd_pkt_len_max', 'fwd_iat_mean', 'flow_pkts_s',
                    'fwd_header_len']

    columns_indices = [12, 24, 7, 49, 23, 2, 40, 9, 21, 58, 42, 59, 53, 13, 5, 35, 22, 25, 28, 36, 30, 33, 15, 42, 8, 27]

    while True:
        for flowline in loglines:
            flowline = flowline.strip()
            dfArray = flowline.split(",")
            if dfArray == ['']:
                continue
            extracted_columns = []
            for index in columns_indices:
                try:
                    extracted_columns.append(dfArray[index])
                except IndexError:
                    extracted_columns.append(None)
            df = pd.DataFrame([extracted_columns], columns=column_names)
            print(df)


            loaded_model = joblib.load('C:/Users/Hp/Portscan-Detection-System/model.pkl')
            X = df.values
            predictions = loaded_model.predict(X)
            print("Predictions: ", predictions)
            
           
