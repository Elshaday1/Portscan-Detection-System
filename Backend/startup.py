import os
import datetime
import subprocess
from subprocess import Popen

def startup():
    # Check network flow csv file if it exists, if not create one.
    curdirname = os.getcwd() # current working directory
    # Generates a filename of the format 'YYYY-MM-DD_Flow.csv'
    global csvfilenam
    csvfilename = "%s_Flow.csv" % (datetime.datetime.today().strftime('%Y-%m-%d'))
    isFileExist = os.path.exists(os.path.join(r'C:\Users\Hp\Desktop\CICFlowmeter\bin\data\daily', csvfilename))
    # If network flow csv file does not exist, create a new one
    if isFileExist == False:
        file = open(os.path.join(r'C:\Users\Hp\Desktop\CICFlowmeter\bin\data\daily', csvfilename), 'w')
        print("------daily file opened")
        file.close()
  
  
    directory_path = r'C:\Users\Hp\Desktop\CICFlowmeter\bin'
    os.chdir(directory_path)

    
    # sub1 = subprocess.Popen(["C:/Users/Hp/Desktop/CICFlowmeter/bin//cfm.bat"], stdout=subprocess.PIPE)
    sub2 = subprocess.Popen(["C:/Users/Hp/Desktop/CICFlowmeter/bin//CICFlowMeter.bat"])
    # sub2 = subprocess.Popen("./CICFlowMeter.bat", stdin=sub1.stdout, stdout=subprocess.PIPE)
    # dropped = []
    # sub1.communicate()
    # print("------cfm.bat opened")
    print("------Current working directory:", os.getcwd())
    # print("------Flowmeter opened")
    # sub2.communicate()
    # print("------Flowmeter closed")

startup()
