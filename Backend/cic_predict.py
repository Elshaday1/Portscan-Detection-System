import pandas as pd
import joblib
import os
import glob

loaded_model = joblib.load('C:/Users/Hp/Portscan-Detection-System/model.pkl')


directory = 'C:/Users/Hp/Desktop/CICFlowmeter/bin/data/daily'

#most recent csv file 
csv_files = glob.glob(os.path.join(directory, '*.csv'))
recent_csv_file = max(csv_files, key=os.path.getctime)


data = pd.read_csv(recent_csv_file)


X = data[['TotLen Fwd Pkts', 'Pkt Len Mean', 'Flow Byts/s', 'ACK Flag Cnt', 'Pkt Len Min',
                           'Dst Port', 'Fwd IAT Min', 'Bwd Pkts/s', 'Bwd Pkt Len Std', 'Init Fwd Win Byts',
                           'Bwd IAT Min', 'Init Bwd Win Byts', 'Idle Min', 'TotLen Bwd Pkts', 'Flow Duration',
                           'Flow IAT Min', 'Bwd Pkt Len Mean', 'Pkt Len Std', 'Bwd Header Len', 'Flow IAT Max',
                           'Fwd Seg Size Min', 'Flow IAT Mean', 'Fwd Pkt Len Max', 'Fwd IAT Mean', 'Flow Pkts/s',
                           'Fwd Header Len']]
#data_extracted = data[['a', 'b', 'c']].rename(columns={'a': 'e', 'b': 'f', 'c': 'g'})
X = X.rename(columns={
    'TotLen Fwd Pkts': 'Total Length of Fwd Packets',
    'Pkt Len Mean': 'Packet Length Mean',
    'Flow Byts/s': 'Flow Bytes/s',
    'ACK Flag Cnt': 'ACK Flag Count',
    'Pkt Len Min': 'Min Packet Length',
    'Dst Port': 'Destination Port',
    'Fwd IAT Min': 'Fwd IAT Min',
    'Bwd Pkts/s': 'Bwd Packets/s',
    'Bwd Pkt Len Std': 'Bwd Packet Length Std',
    'Init Fwd Win Byts': 'Init_Win_bytes_forward',
    'Bwd IAT Min': 'Bwd IAT Min',
    'Init Bwd Win Byts': 'Init_Win_bytes_backward',
    'Idle Min': 'Idle Min',
    'TotLen Bwd Pkts': 'Total Length of Bwd Packets',
    'Flow Duration': 'Flow Duration',
    'Flow IAT Min': 'Flow IAT Min',
    'Bwd Pkt Len Mean': 'Bwd Packet Length Mean',
    'Pkt Len Std': 'Packet Length Std',
    'Bwd Header Len': 'Bwd Header Length',
    'Flow IAT Max': 'Flow IAT Max',
    'Fwd Seg Size Min': 'min_seg_size_forward',
    'Flow IAT Mean': 'Flow IAT Mean',
    'Fwd Pkt Len Max': 'Fwd Packet Length Max',
    'Fwd IAT Mean': 'Fwd IAT Mean',
    'Flow Pkts/s': 'Flow Packets/s',
    'Fwd Header Len': 'Fwd Header Length'
})

predictions = loaded_model.predict(X)


print("Predictions: ", predictions)