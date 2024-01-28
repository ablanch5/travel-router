FROM python:slim-bookworm
WORKDIR /working
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ARG AP_IFNAME
ARG AP_SSID
ARG AP_PWD
ARG CLIENT_IFNAME


COPY setup-ap.py /working/setup-ap.py
COPY travel-router/ /working/travel-router/

# create wifi hotspot aka access point aka ap
#RUN setup-ap.py --ap_ifname AP_IFNAME --ap_ssid AP_SSID --ap_pwd AP_PWD 

# start flask webpage for connecting client device
RUN CLIENT_IFNAME > /working/travel-router/client_ifname
RUN cd travel-router
RUN python app.py CLIENT_IFNAME
