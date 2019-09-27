apt-get update &&  apt-get install -y \
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
    libusb-1.0-0-dev

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
