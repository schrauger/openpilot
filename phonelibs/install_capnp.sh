echo "Installing capnp"

cd
VERSION=0.6.1
wget https://capnproto.org/capnproto-c++-${VERSION}.tar.gz
tar xvf capnproto-c++-${VERSION}.tar.gz
cd capnproto-c++-${VERSION}
CXXFLAGS="-fPIC" ./configure

make -j4 && make install


ln -s /data/data/com.termux/files/usr/bin/capnp /data/data/com.termux/files/usr/bin/capnpc


cd
echo "Installing c-capnp"
git clone https://github.com/commaai/c-capnproto.git
cd c-capnproto
git submodule update --init --recursive
autoreconf -f -i -s
CXXFLAGS="-fPIC" ./configure
make -j4 && make install
