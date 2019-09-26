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
    libzmq5-dev \
    ocl-icd-libopencl1 \
    ocl-icd-opencl-dev \
    opencl-headers \
    pkg-config \
    python-pip \
    wget

sudo phonelibs/install_capnp.sh
sudo pip install -r requirements.txt
