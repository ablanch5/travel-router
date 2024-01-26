from flask import Flask, render_template, request
import subprocess
import argparse

WIFI_FIELDS = "SSID,SIGNAL,BARS,SECURITY"

# get device name for wifi client from command line argument
parser = argparse.ArgumentParser()
parser.add_argument("client_ifname")
args = parser.parse_args()
client_ifname = args.client_ifname


app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    # get wifi network information using nmcli
    stats_command = f"nmcli -t --fields {WIFI_FIELDS} device wifi list ifname {client_ifname}"
    wifi_stats = subprocess.check_output(stats_command, shell=True, text=True)
    wifi_stats_list =wifi_stats.split('\n')
    # last entry is always empty, maybe two \n
    wifi_stats_list = wifi_stats_list[:-2]
    # convert list to tuple of tuples  
    wifi_stats_tuple = tuple([tuple(wifi.split(':')) for wifi in wifi_stats_list])
    # extract ssid column from each row of wifi_stats_tuple
    ssids = [stats[0] for stats in wifi_stats_tuple]
    return render_template("index.html", 
                           ssids=ssids,
                           WIFI_FIELDS=WIFI_FIELDS.split(','), 
                           wifi_stats=wifi_stats_tuple)


@app.route('/submit',methods=['POST'])
def submit():
    if request.method == 'POST':
        ssid = request.form['ssid']
        password = request.form['password']
        # connect to wifi network with ssid and password
        connection_command = f"nmcli --colors no device wifi connect {ssid} ifname \
                            {client_ifname} password {password}"
        result = subprocess.run(connection_command, capture_output=True, text=True, shell=True)
        response = ''
        if result.stderr == '':
            response = "Connection Successful!"
        else:
            response = "Connection Failed"
        return render_template("submit.html", response=response)
    
app.run(host='0.0.0.0', port=5000)