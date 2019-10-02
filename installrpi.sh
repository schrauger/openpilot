apt-get -y install capnproto build-essential git wget libusb-dev python-pip libssl-dev libffi-dev python-dev cmake
git clone https://github.com/zorrobyte/commadeb.git
cd commadeb/allinone/arm64/usr
cp -Rn * /usr
cd
git clone https://github.com/zorrobyte/openpilot.git
cd openpilot
git checkout rpi4
pip install -r requirements.txt
