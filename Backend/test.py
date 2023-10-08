
import pandas as pd
import time
import joblib
import threading
import os
from csv_flow_loader import CSVFlowLoader
from subprocess import Popen
import subprocess
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
    # auto_save_thread = threading.Thread(target=lambda: os.system('python auto_save.py'))
    # auto_save_thread.start()
    
    #process = subprocess.Popen(["C:/Users/Hp/Desktop/CICFlowMeter/bin/CICFlowMeter", argument1, argument2], stdout=subprocess.PIPE)
    # output, _ = process.communicate()
    # Popen(['bash',r"C:/Users/Hp/Desktop/CICFlowMeter/bin/CICFlowMeter"], stdout=subprocess.PIPE)

    logfile = "C:\\Users\\Hp\\Desktop\\CIC\\packets2.csv"
    
    
    while True:
        
        loglines = CSVFlowLoader(logfile)

    
        column_names = ['totlen_fwd_pkts', 'pkt_len_mean', 'flow_byts_s', 'ack_flag_cnt', 'pkt_len_min', 'dst_port', 'fwd_iat_min',
                    'bwd_pkts_s', 'bwd_pkt_len_std', 'init_fwd_win_byts', 'bwd_iat_min', 'init_bwd_win_byts', 'idle_min',
                    'totlen_bwd_pkts', 'flow_duration', 'flow_iat_min', 'bwd_pkt_len_mean', 'pkt_len_std', 'bwd_header_len',
                    'flow_iat_max', 'fwd_seg_size_min', 'flow_iat_mean', 'fwd_pkt_len_max', 'fwd_iat_mean', 'flow_pkts_s',
                    'fwd_header_len']

        columns_indices = [11, 23, 7, 54, 24, 3, 38, 10, 22, 59, 43, 60, 66, 14, 6, 34, 21, 26, 29, 33, 30, 32, 15, 39, 9, 28]

        for flowline in loglines.tailFile():
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
            df = df.dropna()



            df = df.rename(columns={
    'TotLen Fwd Pkts' : 'totlen_fwd_pkts',
    'Pkt Len Mean' :'pkt_len_mean',
    'Flow Byts/s': 'flow_byts_s',
    'ACK Flag Cnt': 'ack_flag_cnt',
    'Pkt Len Min': 'pkt_len_min',
    'Dst Port': 'dst_port',
    'Fwd IAT Min': 'fwd_iat_min',
    'Bwd Pkts/s': 'bwd_pkts_s',
    'Bwd Pkt Len Std': 'bwd_pkt_len_std',
    'Init Fwd Win Byts': 'init_fwd_win_byts',
    'Bwd IAT Min': 'bwd_iat_min',
    'Init Bwd Win Byts': 'init_bwd_win_byts',
    'Idle Min': 'idle_min',
    'TotLen Bwd Pkts': 'totlen_bwd_pkts',
    'Flow Duration': 'flow_duration',
    'Flow IAT Min': 'flow_iat_min',
    'Bwd Pkt Len Mean': 'bwd_pkt_len_mean',
    'Pkt Len Std': 'pkt_len_std',
    'Bwd Header Len': 'bwd_header_len',
    'Flow IAT Max': 'flow_iat_max',
    'Fwd Seg Size Min': 'fwd_seg_size_min',
    'Flow IAT Mean': 'flow_iat_mean',
    'Fwd Pkt Len Max': 'fwd_pkt_len_max',
    'Fwd IAT Mean': 'fwd_iat_mean',
    'Flow Pkts/s': 'flow_pkts_s',
    'Fwd Header Len': 'fwd_header_len'

})
            df = df.replace('', float('nan')).astype(float)
            print(df)
            #df['flow_duration'] = pd.to_numeric(df['flow_duration'], errors='coerce').astype(float)
            loaded_model = joblib.load('C:/Users/Hp/Portscan-Detection-System/model.pkl')
    
            X = df.values
            
            predictions = loaded_model.predict(X)
            print("Predictions: ", predictions)
            
            # socketio.emit('predictions', predictions)
            predictions = loaded_model.predict(X)
            print("Predictions:", predictions)

            for prediction in predictions:
                if prediction == 0:
                    pass  
                elif prediction == 1:
                    print("Attack")

        



           
