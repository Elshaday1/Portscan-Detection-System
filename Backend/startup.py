import os
import datetime
import subprocess
# from threading import Lock
# from flask import Flask, render_template, session
# from flask_socketio import SocketIO, emit
# import test

# async_mode = None
# app = Flask(__name__)

# socketio = SocketIO(app, async_mode=async_mode)
# thread = None
# thread_lock = Lock()


# CSVFILEPATH = "C:/Users/Hp/Desktop/CICFlowmeter/bin/data/daily"
# csvfilename = ""

def startup():
    # Check network flow csv file if it exists, if not create one.
    curdirname = os.getcwd() # current working directory
    # Generates a filename of the format 'YYYY-MM-DD_Flow.csv'
    global csvfilename
    csvfilename = "%s_Flow.csv" % (datetime.datetime.today().strftime('%Y-%m-%d'))
    isFileExist = os.path.exists(os.path.join(r'C:\Users\Hp\Desktop\CICFlowmeter\bin\data\daily', csvfilename))
    # If network flow csv file does not exist, create a new one
    if isFileExist == False:
        file = open(os.path.join(r'C:\Users\Hp\Desktop\CICFlowmeter\bin\data\daily', csvfilename), 'w')
        file.close()
    # Start CICFlowMeter
    # command = "cd"
#     Popen(['bash',os.path.join(curdirname,r"CICFlowMeter-4.0/bin/CICFlowMeter")], stdout=subprocess.PIPE)

    sub1 = subprocess.Popen(["C:/Users/Hp/Desktop/CICFlowmeter/bin//cfm.bat"], stdout=subprocess.PIPE)
    sub2 = subprocess.Popen(["C:/Users/Hp/Desktop/CICFlowmeter/bin//CICFlowMeter.bat"], stdout=subprocess.PIPE)
    # sub2 = subprocess.Popen("./CICFlowMeter.bat", stdin=sub1.stdout, stdout=subprocess.PIPE)
    # dropped = []
    sub1.communicate()
    sub2.communicate()
# runIDS = exec(open('test.py').read())
# @app.route('/')
# def index():
#     return render_template('index.html', async_mode=socketio.async_mode)


# @socketio.event 
# def connect():
#     global thread
#     with thread_lock:
#         if thread is None:
#             thread = socketio.start_background_task(runIDS)
#     emit('my_response', {'data': 'Connected', 'count': 0})

startup()
# socketio.run(app)