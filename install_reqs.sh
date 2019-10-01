sudo apt-get update && sudo apt-get install -y \
    autoconf \
    build-essential \
    bzip2 \
    clang \
    git \
    libarchive-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavfilter-dev \
    libavresample-dev \
    libavutil-dev \
    libffi-dev \
    libglib2.0-0 \
    libssl-dev \
    libswscale-dev \
    libtool \
    libusb-1.0-0 \
    ocl-icd-libopencl1 \
    ocl-icd-opencl-dev \
    opencl-headers \
    pkg-config \
    python-pip \
    wget \
    libusb-1.0-0-dev \
    git build-essential libtool \
    pkg-config autotools-dev autoconf automake cmake \
    uuid-dev libpcre3-dev libsodium-dev valgrind \
    python-dev 

sudo phonelibs/install_capnp.sh
sudo pip install -r requirements.txt

cd /tmp
git clone git://github.com/zeromq/libzmq.git
cd libzmq
./autogen.sh
# do not specify "--with-libsodium" if you prefer to use internal tweetnacl security implementation (recommended for development)
./configure
make -j4
sudo make install
sudo ldconfig
cd ..

cd /tmp
git clone git://github.com/zeromq/czmq.git
cd czmq
./autogen.sh && ./configure && make -j4
sudo make install
sudo ldconfig
cd
