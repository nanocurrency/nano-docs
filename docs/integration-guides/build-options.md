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
* `NANO_WARN_TO_ERR=ON` (*v20.0+* turn compiler warnings into errors on Linux/Mac) 

**Build Node**

* `git submodule update --init --recursive`
* Generate with cmake then build with your compiler
* (\*nix) to build node without GUI execute: `make nano_node`
* (\*nix) to build wallet with GUI execute: `make nano_wallet`
* (\*nix) to build rpc for child/out of process execute: `make nano_rpc`

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

## Build Instructions - Arch Linux

These instructions are for creating an Arch Linux 64bit build.

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

## Build Instructions - Windows

### Dependencies

* [Boost 1.67+ for your build env](https://sourceforge.net/projects/boost/files/boost-binaries)
* [Qt 5.9.5+ 64-bit (open source version) appropriate for your build env](https://www.qt.io/download) 
* [Git for Windows](https://git-scm.com/download/win) **git_bash**
* [CMake](https://cmake.org/download/)
* [Visual Studio 2017 Community](https://my.visualstudio.com/Downloads?q=visual%20studio%202017&wt.mc_id=o~msft~vscom~older-downloads) (or higher edition, if you have a valid license. eg. Professional or Enterprise) 
	* Select **Desktop development with C++**
	* Select the latest Windows 10 SDK
	
### Setup

**Download Source**

Using git_bash:
```bash
git clone --recursive https://github.com/nanocurrency/nano-node
cd nano-node 
```

**Create a `build` folder inside nano-node (makes for easier cleaning of build)**

Using git_bash:
```bash
mkdir build 
cd build 
``` 
* **Note:** all subsequent commands should be run within this "build" folder.

**Get redistributables** 

Using Powershell:
```bash
Invoke-WebRequest -Uri https://aka.ms/vs/15/release/vc_redist.x64.exe -OutFile .\vc_redist.x64.exe 
```

**Generate the build configuration.**

Using 64 Native Tools Command Prompt:

* Replace **%CONFIGURATION%** with one of the following: `Release`, `RelWithDebInfo`, `Debug`
* Replace **%NETWORK%** with one of the following: `nano_beta_network`, `nano_live_network`, `ano_test_network`
* Ensure the Qt, Boost, and Windows SDK paths match your installation.

```bash
cmake -DNANO_GUI=ON -DCMAKE_BUILD_TYPE=%CONFIGURATION% -DACTIVE_NETWORK=%NETWORK% -DQt5_DIR="C:\Qt\5.9.5\msvc2017_64\lib\cmake\Qt5" -DNANO_SIMD_OPTIMIZATIONS=TRUE -DBoost_COMPILER="-vc141" -DBOOST_ROOT="C:/local/boost_1_67_0" -DBOOST_LIBRARYDIR="C:/local/boost_1_67_0/lib64-msvc-14.1" -G "Visual Studio 15 2017 Win64" -DIPHLPAPI_LIBRARY="C:/Program Files (x86)/Windows Kits/10/Lib/10.0.17763.0/um/x64/iphlpapi.lib" -DWINSOCK2_LIBRARY="C:/Program Files (x86)/Windows Kits/10/Lib/10.0.17763.0/um/x64/WS2_32.lib" ..\. 
```

### Build
	
* Open `nano-node.sln` in Visual Studio
* Build the configuration specified in the previous step
* Alternative using 64 Native Tools Command Prompt:

```bash 
cmake --build . --target ALL_BUILD --config %CONFIGURATION% -- /m:%NUMBER_OF_PROCESSORS% 
```

### Package up binaries

Using 64 Native Tools Command Prompt:

* Replace **%CONFIGURATION%** with the build configuration specified in previous step
* Replace **%GENERATOR** with NSIS (if installed) or zip

```bash 
cpack -G %GENERATOR% -C %CONFIGURATION% 
```
