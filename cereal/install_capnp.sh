set -e
echo "Installing capnp"

cd /tmp
VERSION=0.6.1
wget https://capnproto.org/capnproto-c++-${VERSION}.tar.gz
tar xvf capnproto-c++-${VERSION}.tar.gz
cd capnproto-c++-${VERSION}
CXXFLAGS="-fPIC" ./configure

make -j4

# manually build binaries statically
g++ -std=gnu++11 -I./src -I./src -DKJ_HEADER_WARNINGS -DCAPNP_HEADER_WARNINGS -DCAPNP_INCLUDE_DIR=\"/usr/include\" -pthread -O2 -DNDEBUG -pthread -pthread -o .libs/capnp src/capnp/compiler/module-loader.o src/capnp/compiler/capnp.o  ./.libs/libcapnpc.a ./.libs/libcapnp.a ./.libs/libkj.a -lpthread -pthread

g++ -std=gnu++11 -I./src -I./src -DKJ_HEADER_WARNINGS -DCAPNP_HEADER_WARNINGS -DCAPNP_INCLUDE_DIR=\"/usr/include\" -pthread -O2 -DNDEBUG -pthread -pthread -o .libs/capnpc-c++ src/capnp/compiler/capnpc-c++.o  ./.libs/libcapnp.a ./.libs/libkj.a -lpthread -pthread

g++ -std=gnu++11 -I./src -I./src -DKJ_HEADER_WARNINGS -DCAPNP_HEADER_WARNINGS -DCAPNP_INCLUDE_DIR=\"/usr/include\" -pthread -O2 -DNDEBUG -pthread -pthread -o .libs/capnpc-capnp src/capnp/compiler/capnpc-capnp.o  ./.libs/libcapnp.a ./.libs/libkj.a -lpthread -pthread

cp .libs/capnp /usr/bin/
ln -s /usr/bin/capnp /usr/bin/capnpc
cp .libs/capnpc-c++ /usr/bin/
cp .libs/capnpc-capnp /usr/bin/
cp .libs/*.a /usr/lib

cd /tmp
echo "Installing c-capnp"
git clone https://github.com/opensourcerouting/c-capnproto.git
cd c-capnproto
git submodule update --init --recursive
autoreconf -f -i -s
CXXFLAGS="-fPIC" ./configure
make -j4

# manually build binaries statically
gcc -fPIC -o .libs/capnpc-c compiler/capnpc-c.o compiler/schema.capnp.o compiler/str.o  ./.libs/libcapnp_c.a

cp .libs/capnpc-c /usr/bin/
cp .libs/*.a /usr/lib
