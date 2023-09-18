import pandas as pd
import joblib
import os
import glob

loaded_model = joblib.load('C:/Users/Hp/Portscan-Detection-System/model.pkl')


# directory = 'C:/Users/Hp/Desktop/CICFlowmeter/bin/data/daily'

# #most recent csv file 
# csv_files = glob.glob(os.path.join(directory, '*.csv'))
# recent_csv_file = max(csv_files, key=os.path.getctime)


data = pd.read_csv('C:/Users/Hp/Desktop/CIC/packet.csv')


X = data[['totlen_fwd_pkts','pkt_len_mean', 'flow_byts_s', 'ack_flag_cnt', 'pkt_len_min', 'dst_port', 'fwd_iat_min', 'bwd_pkts_s', 'bwd_pkt_len_std',
           'init_fwd_win_byts', 'bwd_iat_min', 'init_bwd_win_byts', 'idle_min', 'totlen_bwd_pkts', 'flow_duration', 'flow_iat_min',
             'bwd_pkt_len_mean', 'pkt_len_std', 'bwd_header_len', 'flow_iat_max', 'fwd_seg_size_min', 'flow_iat_mean', 'fwd_pkt_len_max',
               'fwd_iat_mean', 'flow_pkts_s', 'fwd_header_len']]
#data_extracted = data[['a', 'b', 'c']].rename(columns={'a': 'e', 'b': 'f', 'c': 'g'})
# X = X.rename(columns={
#     'TotLen Fwd Pkts': 'Total Length of Fwd Packets',
#     'Pkt Len Mean': 'Packet Length Mean',
#     'Flow Byts/s': 'Flow Bytes/s',
#     'ACK Flag Cnt': 'ACK Flag Count',
#     'Pkt Len Min': 'Min Packet Length',
#     'Dst Port': 'Destination Port',
#     'Fwd IAT Min': 'Fwd IAT Min',
#     'Bwd Pkts/s': 'Bwd Packets/s',
#     'Bwd Pkt Len Std': 'Bwd Packet Length Std',
#     'Init Fwd Win Byts': 'Init_Win_bytes_forward',
#     'Bwd IAT Min': 'Bwd IAT Min',
#     'Init Bwd Win Byts': 'Init_Win_bytes_backward',
#     'Idle Min': 'Idle Min',
#     'TotLen Bwd Pkts': 'Total Length of Bwd Packets',
#     'Flow Duration': 'Flow Duration',
#     'Flow IAT Min': 'Flow IAT Min',
#     'Bwd Pkt Len Mean': 'Bwd Packet Length Mean',
#     'Pkt Len Std': 'Packet Length Std',
#     'Bwd Header Len': 'Bwd Header Length',
#     'Flow IAT Max': 'Flow IAT Max',
#     'Fwd Seg Size Min': 'min_seg_size_forward',
#     'Flow IAT Mean': 'Flow IAT Mean',
#     'Fwd Pkt Len Max': 'Fwd Packet Length Max',
#     'Fwd IAT Mean': 'Fwd IAT Mean',
#     'Flow Pkts/s': 'Flow Packets/s',
#     'Fwd Header Len': 'Fwd Header Length'
# })
X = X.rename(columns={
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

predictions = loaded_model.predict(X)


print("Predictions: ", predictions)