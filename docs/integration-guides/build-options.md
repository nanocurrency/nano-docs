--8<-- "only-official-builds-supported.md"

## Official release builds

**OS Binaries**  
Each release cycle official builds of the node for Linux, MacOS and Windows are generated and linked to from the related [GitHub Release](https://github.com/nanocurrency/nano-node/releases) as well as on [Nano.org](https://nano.org/en).

**Other sources**  
The node can be also be installed from other sources including [Docker](/running-a-node/node-setup#installing-docker) and RHEL/CentOS rpm:
```
sudo yum-config-manager --add-repo https://repo.nano.org/nanocurrency.repo
sudo yum install nanocurrency
```

This installs `nano_node` to bin.

### Beta builds

**OS Binaries**  
Each beta release cycle official beta builds of the node for Linux, MacOS and Windows are released and can be found at https://beta.nano.org. Go to the [Beta Network page](/running-a-node/beta-network/) for more details.

**Other sources**  
The beta node can be also be installed from other sources including [Docker](/running-a-node/beta-network#pulling-the-docker-image) and RHEL/CentOS rpm:
```
sudo yum-config-manager --add-repo https://repo.nano.org/nanocurrency-beta.repo
sudo yum install nanocurrency-beta
```

This installs `nano_node-beta` to bin.

## Nano Folder

### Contents

--8<-- "folder-contents.md"

### Locations

--8<-- "folder-locations.md"

??? tip "Moving folder locations"
    Some users desire to change the blockchain download location. A solution is available for the no gui nano_node (see https://github.com/nanocurrency/nano-node/issues/79), but no concrete solution is available for the GUI client. However, a workaround can be acheived via the use of symbolic links. Below is a short tutorial for Windows builds:

    1. Rename/delete the Nano folder in your `appdata` Local folder (if you haven't run the wallet yet, skip this step). This is necessary because the command to create a symbolic link in windows will fail if the the input directory already exists.
    1. Decide on where you want to store the blockchain and create a symbolic link. The command is (in an administrative command-prompt): `mklink /d "C:\Users\<user>\AppData\Local\Nano\" "E:\Some\Other\Directory"`. This command creates a symbolic link for a directory (`/d`) that 'redirects' all requests for files/directories in the `Local\Nano` folder to the `Other\Directory`. This means that a file created in the input directory will actually be in the output directory (on the other disk).
    1. Verify it works. Create a file in your Nano folder in your appdata, and you should see it appear in the directory you linked it to (and vice-versa). If you have old wallets or a partially-downloaded blockchain, copy them back into the local directory. Start the wallet.

---

## Build Instructions - Ubuntu

--8<-- "unsupported-configuration.md"

### Node

**Install boost library**
```
apt-get update
apt-get install libboost-all-dev
```

**(Optional) Build and Install boost v1.66 instead (Ubuntu repo has v1.58)**
Install required dependencies:
```
sudo apt install g++ git cmake -y
```
```
wget https://dl.bintray.com/boostorg/release/1.66.0/source/boost_1_66_0.tar.bz2
tar --bzip2 -xf boost_1_66_0.tar.bz2
cd boost_1_66_0
./bootstrap.sh
sudo ./b2 install
```
**Download and extract nano node**
```
cd ~
wget https://github.com/nanocurrency/nano-node/releases/download/V11.2/nano-11.2.0-Linux.tar.bz2
tar xvf nano-11.2.0-Linux.tar.bz2
```

**Initiate nano_node to generate \~/Nano**
```
 ./nano-node-11.2.0-Linux/bin/nano_node --daemon
```

*Press ctrl+c to kill process*

**Update config.json**
```
nano ~/Nano/config.json
```
Change: "rpc_enable": "true"
Save and quit


**Find path and user of nano_node binary**
```
cd ~/nano-node-11.2.0-Linux/bin/
pwd -P
```
This should output something similar to: /home/stanley/nano-node-11.2.0-Linux/bin
Write down this path for our service file in a future step

```
ls -l
```
This should output something similar to: `-rwxr-xr-x 1 stanley stanley 8.9M Feb 16 02:25 nano_node`
Write down the user and group (in this example, both the user and group is stanley) to the left of nano_node, this should be the same as your username

**Create service file**
```
sudo touch /etc/systemd/system/nano_node.service   
sudo chmod 664 /etc/systemd/system/nano_node.service   
sudo nano /etc/systemd/system/nano_node.service  
```

**Service file**
```
[Unit]
Description=Nano node service
After=network.target

[Service]
ExecStart=/home/stanley/nano-node-11.2.0-Linux/bin/nano_node --daemon #Update this with the link copied from the last step
Restart=on-failure
User=stanley #This user from the last step
Group=stanley #The group from the last step

[Install]
WantedBy=multi-user.target
```

Be sure to remove the comments (the parts starting at #) as they may cause problems.

**Start the service**
```
sudo service nano_node start
```

**Enable the node to run on boot**
```
sudo systemctl enable nano_node
```

**Create a symlink to nano_node to easily access later**
```
ln -s ~/nano-node-11.2.0-Linux/bin/nano_node /usr/local/sbin/nano_node
```

You should now have a brand new node up and running, and the blocks syncing.

**Check Status**
```
nano_node --debug_block_count
```
This will show you how far along the node is to syncing the blocks. You can compare this to the current block count from Aggregate Network Stats at [https://nanocrawler.cc/network](https://nanocrawler.cc/network) to see how far along the syncing process your are.

### QT Wallet

**Install dependencies**

    sudo apt-get update && sudo apt-get upgrade
    sudo apt-get install git cmake g++ curl wget
  
**Build Boost 1.67.0**

    wget -O boost_1_67_0.tar.gz https://netix.dl.sourceforge.net/project/boost/boost/1.67.0/boost_1_67_0.tar.gz
    tar xzvf boost_1_67_0.tar.gz
    cd boost_1_67_0
    ./bootstrap.sh --with-libraries=filesystem,log,program_options,thread
    ./b2 --prefix=../[boost] link=static install   
    cd ..

**Install QT5**

    sudo apt-get install libqt5gui5 libqt5core5a libqt5dbus5 qttools5-dev qttools5-dev-tools libprotobuf-dev protobuf-compiler

**Build nano_wallet**

    git clone --recursive https://github.com/nanocurrency/nano-node.git nano_build   
    cd nano_build
    git submodule update --init --recursive
    cmake -G "Unix Makefiles" -DNANO_GUI=ON -DBOOST_ROOT=../[boost]/
    make nano_wallet
    cp nano_wallet ../nano_wallet && cd .. 

**Run nano_wallet**

    ./nano_wallet

#### Troubleshooting

!!! warning ""
    This application failed to start because it could not find or load the Qt platform plugin "xcb".**

If you get this error, make sure you have QT5 installed. If it's installed, locate the file 'libqxcb.so' on your system and then tell nano_wallet where this file can be found (set it to the 'plugins' directory).

    locate libqxcb.so
    # returns /usr/lib/qt/plugins/platforms/libqxcb.so or something similar
    export QT_PLUGIN_PATH=/usr/lib/qt/plugins
    nano_wallet

If you don't want to run this each time you can setup an alias to do this for you:

    echo 'alias nano_wallet="QT_PLUGIN_PATH=/usr/lib/qt/plugins nano_wallet"' >> ~/.bashrc
    source ~/.bashrc

!!! warning ""
    Error starting nano exception while running wallet: No such node (Wallet)**

If you get this error, it might be related to pre-existing configuration file issues on your system. You can try the following to generate a fresh configuration (your existing/older configuration will be under \~/Nano.old). **Please be careful with the following if you already run a wallet, as these details will be forgotten by the nano_wallet due to starting with a fresh configuration:**

    mv ~/Nano{,.old}
    nano_wallet

!!! warning ""
    Wallet crashes with an `Aborted (core dumped)` error**

This may be related to a display issue. Try setting the environment variable `GDK_BACKEND=x11` before running nano_wallet.

    GDK_BACKEND=x11 ./nano_wallet


---

## Build Instructions - General

--8<-- "unsupported-configuration.md"

!!! success "Requirements"
    **Required Source**

    * [Boost 1.67](http://www.boost.org/users/history/version_1_67_0.html) extracted to [boost.src] (OR `sh nano-node/util/build_prep/bootstrap_boost.sh -m`)
    * (wallet) [Qt 5.x open source edition](https://www1.qt.io/download-open-source/) extracted to [qt.src]
    * Nano node source in [nano-node.src]

    **Required build tools**

    * (macOS) XCode >= 7.3
    * (Windows) Visual Studio 2015
    * (Windows) NSIS package builder
    * (\*nix) Clang >= 3.5 or GCC >= 5
    * CMake

### Boost

**Option 1**

Inside `nano-node` directory run:

```bash
sh util/build_prep/bootstrap_boost.sh -m
```

This will build the required Boost libraries at `/usr/local/boost/`.

**Option 2**

Inside [boost.src] run:
```bash
./bootstrap.sh --with-libraries=filesystem,log,program_options,thread
./b2 --prefix=[boost] --build-dir=[boost.build] link=static install
```
If on Windows: an additional b2 option `address-model=64` for x64 builds should be included.

### QT Wallet

In [qt.build] execute:
```bash
[qt.src]/configure -shared -opensource -nomake examples -nomake tests -confirm-license  -prefix [qt]
make
make install
```
If on Windows: use `nmake` instead of `make`.

### Node

**CMake variables**

Format: `cmake -D VARNAME=VARVALUE`

* `BOOST_ROOT=\[boost\]` (`/usr/local/boost/` if bootstrapped)
* `CMAKE_BUILD_TYPE=Release` (default)
* `ACTIVE_NETWORK=nano_live_network` (default)
* `Qt5_DIR=[qt]lib/cmake/Qt5` (to build GUI wallet)
* `NANO_GUI=ON` (to build GUI wallet)
* `ENABLE_AVX2=ON`, *optional* `PERMUTE_WITH_GATHER=ON`, *optional* `PERMUTE_WITH_SHUFFLES=ON` (for CPU with AXV2 support, choose fastest method for your CPU with https://github.com/sneves/blake2-avx2/)
* `CRYPTOPP_CUSTOM=ON` (more conservative building of Crypto++ for wider range of systems)
* `NANO_SIMD_OPTIMIZATIONS=OFF` (Enable CPU-specific SIMD optimization: SSE/AVX or NEON, e.g.)
* `NANO_SECURE_RPC=ON` (to build node with TLS)

**Build Node**

* `git submodule update --init --recursive`
* Generate with cmake then build with your compiler
* (\*nix) to build node without GUI execute: `make nano_node`
* (\*nix) to build wallet with GUI execute: `make nano_wallet`

**Building a package**

* (macOS) `cpack -G "DragNDrop"`
* (Windows) `cpack -G "NSIS"`
* (\*nix) `cpack -G "TBZ2"`

**Testing Nano**

* In order to run the tests, the corresponding CMake variable must be set: `-D NANO_TEST=ON`.
* With this variable set, make will also build test files, and will produce `core_test` and `slow_test` binaries, which can be executed like `./core_test`.
* To run a node on the test network, set CMake variable: `-DACTIVE_NETWORK=nano_test_network`

**Beta Network Participation**

* More information can be found on the [Beta Network page](/running-a-node/beta-network/)
* To run a node on the beta network, set CMake variable: `-DACTIVE_NETWORK=nano_beta_network`

---

## Build Instructions - ARM

These instructions are for creating an ArchlinuxARM 64bit build.

--8<-- "unsupported-configuration.md"


### Dependencies

```bash
pacman -Syu  
pacman -S base-devel git gcc cmake curl wget
```

### Static Boost

```bash
wget -O boost_1_67_0.tar.gz http://sourceforge.net/projects/boost/files/boost/1.67.0/boost_1_67_0.tar.gz/download   
tar xzvf boost_1_67_0.tar.gz   
cd boost_1_67_0   
./bootstrap.sh   
./b2 --prefix=../[boost] link=static install   
cd ..
```

### Node

```bash
git clone --recursive https://github.com/nanocurrency/nano-node.git nano_build   
cd nano_build   
cmake -DBOOST_ROOT=../[boost] -G "Unix Makefiles"   
make nano_node   
cp nano_node ../nano_node && cd .. && ./nano_node --diagnostics   
```

---

## Build Instructions - Unix

These instructions are for creating a build on the following systems:

* Ubuntu 16.04 LTS Server
* Ubuntu 16.10+
* Debian 8 Jessie (Debian 8 requires Cmake 3.4+)
* Debian 9 Stretch

See further below for [CentOS 7](#build-instructions-centos-7) and [OSX](#build-instructions-osx).


--8<-- "unsupported-configuration.md"

### Dependencies 

```bash
sudo apt-get update && sudo apt-get upgrade   
sudo apt-get install git cmake g++ curl wget
```   
### Static Boost
```bash
wget -O boost_1_67_0.tar.gz https://netix.dl.sourceforge.net/project/boost/boost/1.67.0/boost_1_67_0.tar.gz   
tar xzvf boost_1_67_0.tar.gz   
cd boost_1_67_0   
./bootstrap.sh --with-libraries=filesystem,log,program_options,system,thread   
./b2 --prefix=../[boost] link=static install   
cd ..
```
### Node

```bash
git clone --recursive https://github.com/nanocurrency/nano-node.git nano_build   
cd nano_build   
cmake -DBOOST_ROOT=../[boost]/ -G "Unix Makefiles"   
make nano_node   
cp nano_node ../nano_node && cd .. && ./nano_node --diagnostics
```

## Build Instructions - CentOS 7

!!! success "Requirements"
    * GCC compiler version 4.9+ or other compiler with C++14 language support (default Centos 7 compilers are outdated)
    * Cmake 3.4+

### Dependencies 

```bash
sudo yum check-update   
sudo yum install git libstdc++-static curl wget   
```

### Configure repository with modern GCC
```bash
sudo yum install centos-release-scl   
sudo yum install devtoolset-7-gcc*   
scl enable devtoolset-7 bash   
```

### Modern Cmake
```bash
wget https://cmake.org/files/v3.12/cmake-3.12.1.tar.gz   
tar zxvf cmake-3.12.1.tar.gz && cd cmake-3.12.1    
./bootstrap --prefix=/usr/local   
make -j$(nproc)   
sudo make install   
cd ..    
```

### Static Boost

```bash
wget -O boost_1_67_0.tar.gz https://netix.dl.sourceforge.net/project/boost/boost/1.67.0/boost_1_67_0.tar.gz   
tar xzvf boost_1_67_0.tar.gz && cd boost_1_67_0   
./bootstrap.sh --with-libraries=filesystem,log,program_options,system,thread   
./b2 --prefix=../[boost] link=static install   
cd ..
```

### Node

```bash
git clone --recursive https://github.com/nanocurrency/nano-node.git nano_build   
cd nano_build   
cmake -DBOOST_ROOT=../[boost]/ -G "Unix Makefiles"   
make nano_node   
cp nano_node .. && cd .. && ./nano_node --diagnostics
```

---

## Build Instructions - OSX

```
git clone https://github.com/nanocurrency/nano-node.git
cd nano-node 
sh util/build_prep/bootstrap_boost.sh -m
git submodule update --init --recursive
cmake -DBOOST_ROOT=../[boost]/ -G "Unix Makefiles"
make
./nano_node/nano_node --daemon
```

