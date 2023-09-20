import os

file_path = r'C:\Users\Hp\Desktop\CICFlowmeter\bin\CICFlowMeter.bat'


if os.path.exists(file_path):
    os.startfile(file_path)
    print("CIC Flow Meter opened successfully!")
else:
    print(" file does not exist.")
