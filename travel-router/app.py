from flask import Flask, render_template, request, redirect
import subprocess
import setup_ap
import yaml
import os

WIFI_FIELDS = "SSID,SIGNAL,BARS,SECURITY"

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET','POST'])
def index():
    print(os.getcwd())
    print(os.listdir(os.getcwd()))
    print('\n')
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    is_configured = config['is_configured']
    if is_configured:
        return redirect('/connect')
    else:
        return redirect('/configure')

@app.route('/configure')
def configure():
    return render_template("configure.html")

@app.route('/configured', methods=['POST'])
def configured():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    if request.method == 'POST':
        config['client_ifname'] = request.form['client_ifname']
        config['ap_ifname'] = request.form['ap_ifname']
        config['ap_ssid'] = request.form['ap_ssid']
        config['ap_pwd'] = request.form['ap_pwd']
        config['is_configured'] = True
        setup_ap.setup(config['ap_ifname'], config['ap_ssid'], config['ap_pwd'])
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file)
    return render_template("configured.html")

@app.route('/connect')
def connect():
    # connects access point wifi
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    client_ifname= config['client_ifname']

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
    return render_template("connect.html", 
                           ssids=ssids,
                           WIFI_FIELDS=WIFI_FIELDS.split(','), 
                           wifi_stats=wifi_stats_tuple)


@app.route('/submit',methods=['POST'])
def submit():
    # connects client wifi
    if request.method == 'POST':
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        client_ifname= config['client_ifname']
        client_ssid = request.form['ssid']
        client_pwd = request.form['password']
        # connect to wifi network with ssid and password
        connection_command = f"sudo nmcli --colors no device wifi connect {client_ssid} ifname \
                            {client_ifname} password {client_pwd}"
        result = subprocess.run(connection_command, capture_output=True, text=True, shell=True)
        response = ''
        if result.stderr == '':
            response = "Connection Successful!"
        else:
            response = result.stderr
        return render_template("submit.html", response=response)
    
app.run(host='0.0.0.0', port=5000, debug=True)