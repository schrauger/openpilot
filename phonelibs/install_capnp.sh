set -e
echo "Installing capnp"

cd /tmp
curl -O https://capnproto.org/capnproto-c++-0.7.0.tar.gz
tar zxf capnproto-c++-0.7.0.tar.gz
cd capnproto-c++-0.7.0
./configure
make -j6 check
sudo make install

cd /tmp
echo "Installing c-capnp"
#git clone https://github.com/commaai/c-capnproto.git
#cd c-capnproto
#git submodule update --init --recursive
#autoreconf -f -i -s
#CXXFLAGS="-fPIC" ./configure
#make -j4
#make install

git clone https://github.com/opensourcerouting/c-capnproto
cd c-capnproto
git submodule update --init --recursive
autoreconf -f -i -s
./configure
make -j4
make install
