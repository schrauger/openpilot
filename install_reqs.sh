apt-get update &&  apt-get install -y \
    autoconf \
    build-essential \
    bzip2 \
    clang \
    git \
    wget

phonelibs/install_capnp.sh
pip install -r requirements.txt

cd
git clone https://github.com/zeromq/libzmq.git
cd libzmq
autoreconf -f -i -s
CXXFLAGS="-fPIC" ./configure
make -j4
make install
cd

cd
git clone https://github.com/zeromq/czmq.git
cd czmq
autoreconf -f -i -s
CXXFLAGS="-fPIC" ./configure
make -j4
make install
cd
