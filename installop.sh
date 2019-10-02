apt install -y build-essential libusb-dev libusb-1.0 python-pip cmake git wget automake
set -e
rm -rf /tmp/*
echo "Installing capnp"

cd /tmp
VERSION=0.6.1
wget https://capnproto.org/capnproto-c++-${VERSION}.tar.gz
tar xvf capnproto-c++-${VERSION}.tar.gz
cd capnproto-c++-${VERSION}
CXXFLAGS="-fPIC" ./configure

make -j8
make install

# manually build binaries statically
g++ -std=gnu++11 -I./src -I./src -DKJ_HEADER_WARNINGS -DCAPNP_HEADER_WARNINGS -DCAPNP_INCLUDE_DIR=\"/usr/local/include\" -pthread -O2 -DNDEBUG -pthread -pthread -o .libs/capnp src/capnp/compiler/module-loader.o src/capnp/compiler/capnp.o  ./.libs/libcapnpc.a ./.libs/libcapnp.a ./.libs/libkj.a -lpthread -pthread

g++ -std=gnu++11 -I./src -I./src -DKJ_HEADER_WARNINGS -DCAPNP_HEADER_WARNINGS -DCAPNP_INCLUDE_DIR=\"/usr/local/include\" -pthread -O2 -DNDEBUG -pthread -pthread -o .libs/capnpc-c++ src/capnp/compiler/capnpc-c++.o  ./.libs/libcapnp.a ./.libs/libkj.a -lpthread -pthread

g++ -std=gnu++11 -I./src -I./src -DKJ_HEADER_WARNINGS -DCAPNP_HEADER_WARNINGS -DCAPNP_INCLUDE_DIR=\"/usr/local/include\" -pthread -O2 -DNDEBUG -pthread -pthread -o .libs/capnpc-capnp src/capnp/compiler/capnpc-capnp.o  ./.libs/libcapnp.a ./.libs/libkj.a -lpthread -pthread

cp .libs/capnp /usr/local/bin/
rm /usr/local/bin/capnpc
ln -sfn /usr/local/bin/capnp /usr/local/bin/capnpc
cp .libs/capnpc-c++ /usr/local/bin/
cp .libs/capnpc-capnp /usr/local/bin/
cp .libs/*.a /usr/local/lib

cd /tmp
echo "Installing c-capnp"
git clone https://github.com/commaai/c-capnproto.git
cd c-capnproto
git submodule update --init --recursive
autoreconf -f -i -s
CXXFLAGS="-fPIC" ./configure
make -j8
make install

# manually build binaries statically
gcc -fPIC -o .libs/capnpc-c compiler/capnpc-c.o compiler/schema.capnp.o compiler/str.o  ./.libs/libcapnp_c.a

cp .libs/capnpc-c /usr/local/bin/
cp .libs/*.a /usr/local/lib

echo "Installing libzmq"
cd /tmp
git clone --single-branch --branch latest_release https://github.com/zeromq/libzmq.git
cd libzmq
autoreconf -f -i -s
CXXFLAGS="-fPIC" ./configure
make -j8
make install

echo "Installing czmq"
cd /tmp
git clone --single-branch --branch latest_release https://github.com/zeromq/czmq.git
cd czmq
autoreconf -f -i -s
CXXFLAGS="-fPIC" ./configure
make -j8
make install

echo "Cloning x86 OP"
cd
git clone https://github.com/zorrobyte/openpilot.git
cd openpilot
git checkout x86

echo "Setting up pipenv"
pip install pipenv
pipenv install
pipenv shell

echo "Creating directories"
mkdir /data
chown ${USER:=$(/usr/bin/id -run)}:$USER /data

echo "Compiling and launching OP"
./launch_openpilot
