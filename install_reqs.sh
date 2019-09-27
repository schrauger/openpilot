apt-get update &&  apt-get install -y \
    autoconf \
    build-essential \
    bzip2 \
    clang \
    git \
    wget \
    python2

phonelibs/install_capnp.sh


cd
git clone https://github.com/zeromq/libzmq.git
cd libzmq
autoreconf -f -i -s
CXXFLAGS="-fPIC" ./configure --prefix=/data/data/com.termux/files/usr
make -j4
make install
cd
##This installs to /usr/local instead of /data/data/com.termux/files/usr -- you need to cp -Rn the files ^^^^

cd
git clone https://github.com/zeromq/czmq.git
cd czmq
autoreconf -f -i -s
CXXFLAGS="-fPIC" ./configure --prefix=/data/data/com.termux/files/usr
make -j4
make install
cd

cd
git clone https://github.com/libusb/libusb.git
cd libusb
autoreconf -f -i -s
CXXFLAGS="-fPIC" ./configure --prefix=/data/data/com.termux/files/usr --disable-udev #https://sourceforge.net/p/libusb/mailman/message/35494056/
make -j4
make install
cd

pip2 install -r requirements.txt
