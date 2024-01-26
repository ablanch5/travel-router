import subprocess
import argparse

# parse command line argument
parser = argparse.ArgumentParser()
parser.add_argument("--ap_ifname", required=True)
parser.add_argument("--ap_ssid", required=True)
parser.add_argument("--ap_pwd", required=True)
args = parser.parse_args()
ap_ifname = args.ap_ifname
ap_ssid = args.ap_ssid
ap_pwd = args.ap_pwd

run_command = f"sudo nmcli device wifi hotspot ssid {ap_ssid} password {ap_pwd} ifname {ap_ifname}"
subprocess.run(run_command, shell=True)

modify_command = "sudo nmcli connection modify Hotspot \
                connection.autoconnect yes connection.autoconnect-priority 100"
subprocess.run(modify_command, shell=True)