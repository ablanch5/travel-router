FROM python:slim-bookworm
WORKDIR /working
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ARG AP_IFNAME
ARG AP_SSID
ARG AP_PWD
ARG CLIENT_IFNAME

# create wifi hotspot aka access point aka ap
COPY setup-ap.py /working/setup-ap.py
RUN setup-ap.py --ap_ifname AP_IFNAME --ap_ssid AP_SSID --ap_pwd AP_PWD 

# start flask webpage for connecting client device
COPY travel-router/ /working/travel-router/
RUN CLIENT_IFNAME > /working/travel-router/client_ifname
RUN cd travel-router
RUN python app.py CLIENT_IFNAME
