# Build Options

--8<-- "only-official-builds-supported.md"

## Official release builds
 
Each release cycle official builds of the node for Linux, MacOS and Windows are generated and linked to from the related [GitHub Release](https://github.com/nanocurrency/nano-node/releases):

--8<-- "current-release-build-links.md"

--8<-- "known-issue-peers-stake-reporting.md"

--8<-- "known-issue-macos-too-many-open-files.md"

### Beta builds

Each beta release cycle official beta builds of the node for Linux, MacOS and Windows are released, along with Docker images. Go to the [Beta Network page](/running-a-node/beta-network/) for more details.

**Other sources**  
The beta node can be also be installed for RHEL/CentOS rpm:
```bash
sudo yum-config-manager --add-repo https://repo.nano.org/nanocurrency-beta.repo
sudo yum install nanocurrency-beta
```

This installs `nano_node-beta` to bin.

## Nano Directory

### Contents

--8<-- "directory-contents.md"

### Locations

--8<-- "directory-locations.md"

??? tip "Moving directory locations"
    Some users desire to change the blockchain download location. A solution is available for the no gui nano_node (see https://github.com/nanocurrency/nano-node/issues/79), but no concrete solution is available for the GUI client. However, a workaround can be acheived via the use of symbolic links. Below is a short tutorial for Windows builds:

    1. Rename/delete the Nano directory in your `appdata` Local directory (if you haven't run the wallet yet, skip this step). This is necessary because the command to create a symbolic link in windows will fail if the the input directory already exists.
    1. Decide on where you want to store the blockchain and create a symbolic link. The command is (in an administrative command-prompt): `mklink /d "C:\Users\<user>\AppData\Local\Nano\" "E:\Some\Other\Directory"`. This command creates a symbolic link for a directory (`/d`) that 'redirects' all requests for files/directories in the `Local\Nano` directory to the `Other\Directory`. This means that a file created in the input directory will actually be in the output directory (on the other disk).
    1. Verify it works. Create a file in your Nano directory in your appdata, and you should see it appear in the directory you linked it to (and vice-versa). If you have old wallets or a partially-downloaded blockchain, copy them back into the local directory. Start the wallet.

---

## General Build Instructions

--8<-- "unsupported-configuration.md"

!!! success "Requirements"
    **Required Source**

    * [Boost 1.69+](http://www.boost.org/users/history/version_1_69_0.html) extracted to [boost.src] (OR `sh nano-node/util/build_prep/bootstrap_boost.sh -m`)
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
./bootstrap.sh --with-libraries=filesystem,log,program_options,system,thread
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
* `NANO_TIMED_LOCKS=50` (*v20.0+* when the number of milliseconds a mutex is held is equal or greater than this output a stacktrace, 0 disables.)
* `NANO_STACKTRACE_BACKTRACE=ON` (*v20.0+* use a different configuration of Boost backtrace in stacktraces, attempting to display filenames, function names and line numbers. Needs `libbacktrace` to be installed. Some [workarounds](https://www.boost.org/doc/libs/develop/doc/html/stacktrace/configuration_and_build.html#stacktrace.configuration_and_build.f3) may be necessary depending on system and configuration. Use CLI [`--debug_stacktrace`](/commands/command-line-interface#-debug_stacktrace) to get an example output.)
* `CI_BUILD=TRUE` (*v20.0+* if enabled, uses environment variable `TRAVIS_TAG` (required) to modify the locally reported node version; example `TRAVIS_TAG="My Nano Node v20"`)
* `NANO_ROCKSDB=ON` (*v20.0+* NOTE: RocksDB support is still in experimental stages and should not be used in production systems. To build the node with RocksDB [click here](/running-a-node/rocksdb-ledger-backend/#rocksdb-ledger-backend) for more details)

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

**Testing the Node**

* In order to run the tests, the corresponding CMake variable must be set: `-D NANO_TEST=ON`.
* With this variable set, `make` will also build test files, and will produce `core_test`, `rpc_test`, `load_test` and `slow_test` binaries, which can be executed such as `./core_test`.
* See more details in [Testing](#testing)

**Beta Network Participation**

* More information can be found on the [Beta Network page](/running-a-node/beta-network/)
* To run a node on the beta network, set CMake variable: `-DACTIVE_NETWORK=nano_beta_network`

---

## Debian/Ubuntu Dependencies

These instructions are for the following systems:

* Ubuntu 16.04 LTS Server
* Ubuntu 16.10+
* Debian 8 Jessie (Debian 8 requires Cmake 3.4+)
* Debian 9 Stretch

**Install dependencies**

```bash
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install git cmake g++ curl wget
```

Follow the [build instructions](#build-instructions-debian-centos-arch-linux).

## CentOS 7 Dependencies

**Requirements**

* GCC compiler version 4.9+ or other compiler with C++14 language support (default Centos 7 compilers are outdated)
* Cmake 3.4+

**Install dependencies**

```bash
sudo yum check-update
sudo yum install git libstdc++-static curl wget
```

**Configure repository with modern GCC**
```bash
sudo yum install centos-release-scl
sudo yum install devtoolset-7-gcc*
scl enable devtoolset-7 bash
```

**Modern Cmake**
```bash
wget https://cmake.org/files/v3.12/cmake-3.12.1.tar.gz
tar zxvf cmake-3.12.1.tar.gz && cd cmake-3.12.1
./bootstrap --prefix=/usr/local
make -j$(nproc)
sudo make install
cd ..
```

Follow the [build instructions](#build-instructions-debian-centos-arch-linux).

## Arch Linux Dependencies

**Install dependencies**

```bash
pacman -Syu
pacman -S base-devel git gcc cmake curl wget
```

Follow the [build instructions](#build-instructions-debian-centos-arch-linux).

---

## Build Instructions - Debian, CentOS, Arch Linux

--8<-- "unsupported-configuration.md"

### Node

```bash
git clone --branch V21.1 --recursive https://github.com/nanocurrency/nano-node.git nano_build
cd nano_build
export BOOST_ROOT=`pwd`/../boost_build
sh util/build_prep/bootstrap_boost.sh -m
cmake -G "Unix Makefiles" .
make nano_node
cp nano_node ../nano_node && cd .. && ./nano_node --diagnostics
```

---

## Build Instructions - macOS

--8<-- "unsupported-configuration.md"

```bash
git clone --branch V21.1 --recursive https://github.com/nanocurrency/nano-node.git nano_build
cd nano_build
export BOOST_ROOT=`pwd`/../boost_build
sh util/build_prep/bootstrap_boost.sh -m
cmake -G "Unix Makefiles" .
make nano_node
cp nano_node ../nano_node && cd .. && ./nano_node --diagnostics
```

## Build Instructions - Windows

--8<-- "unsupported-configuration.md"

### Dependencies

* [Boost 1.69+ for your build env](https://sourceforge.net/projects/boost/files/boost-binaries)
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
git clone --branch V21.1 --recursive https://github.com/nanocurrency/nano-node
cd nano-node
```

**Create a `build` directory inside nano-node (makes for easier cleaning of build)**

Using git_bash:
```bash
mkdir build
cd build
``` 
* **Note:** all subsequent commands should be run within this "build" directory.

**Get redistributables** 

Using Powershell:
```bash
Invoke-WebRequest -Uri https://aka.ms/vs/15/release/vc_redist.x64.exe -OutFile .\vc_redist.x64.exe
```

**Generate the build configuration.**

Using 64 Native Tools Command Prompt:

* Replace **%CONFIGURATION%** with one of the following: `Release`, `RelWithDebInfo`, `Debug`
* Replace **%NETWORK%** with one of the following: `nano_beta_network`, `nano_live_network`, `nano_test_network`
* Ensure the Qt, Boost, and Windows SDK paths match your installation.

```bash
cmake -DNANO_GUI=ON -DCMAKE_BUILD_TYPE=%CONFIGURATION% -DACTIVE_NETWORK=%NETWORK% -DQt5_DIR="C:\Qt\5.9.5\msvc2017_64\lib\cmake\Qt5" -DNANO_SIMD_OPTIMIZATIONS=TRUE -DBoost_COMPILER="-vc141" -DBOOST_ROOT="C:/local/boost_1_69_0" -DBOOST_LIBRARYDIR="C:/local/boost_1_69_0/lib64-msvc-14.1" -G "Visual Studio 15 2017 Win64" -DIPHLPAPI_LIBRARY="C:/Program Files (x86)/Windows Kits/10/Lib/10.0.17763.0/um/x64/iphlpapi.lib" -DWINSOCK2_LIBRARY="C:/Program Files (x86)/Windows Kits/10/Lib/10.0.17763.0/um/x64/WS2_32.lib" ..\.
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
* Replace **%GENERATOR%** with NSIS (if installed) or ZIP

```bash 
cpack -G %GENERATOR% -C %CONFIGURATION%
```

---

## Testing

A number of tests binaries can be built when the `-DNANO_TEST` CMake variable is set to `ON`.

* `core_test` - Tests the majority of protocol, node and network functionality.
* `slow_test` - Tests which operate on a large amount of data and may take a while. Not currently tested by CI.
* `rpc_test` - Tests all RPC commands
* `load_test` - Launches many nodes and RPC servers, checking sending/receiving blocks with simultaneous calls. Use `./load_test --help` to see the available options

### Running Tests

To run all tests in a binary just launch it:
```bash
./core_test
```

To check a specific subset of tests, gtest filtering can be used (with optional wildcards):
```bash
./core_test --gtest_filter=confirmation_height.single
./rpc_test --gtest_filter=rpc.*
```

To run tests multiple times:
```bash
./core_test --gtest_repeat=10
```

If running on a debugger, add the argument `--gtest_break_on_failure` break at the moment a test fails.

### Environment variables to customize tests

* `TEST_KEEP_TMPDIRS=1` - Setting this to anything will prevent the tests deleting any files it creates, useful for debugging log files. 
* `TEST_USE_ROCKSDB=1` - Use the RocksDB ledger backend for the tests instead of LMDB. The tests must be built with [RocksDB](/running-a-node/rocksdb-ledger-backend/#rocksdb-ledger-backend) support.
* `TEST_BASE_PORT=26000` - The base port used in tests, the range of ports used in this case would be 26000 - 26199. This is useful if wanting to run multiple tests at once without port conflicts, the default base port used is 24000. 

### Sanitizers

3 different CMake sanitizer options are supported: `NANO_ASAN_INT`, `NANO_TSAN` and `NANO_ASAN`. They cannot be used in conjunction with each other.

#### Thread Sanitizer
Use `-DNANO_TSAN=ON` as an extra CMake option. The following environment variable should also be set:

`export TSAN_OPTIONS="suppressions=../tsan_suppressions"`

`tsan_suppressions` should be a path to the file in the root nano directory. This suppresses many errors relating to the mdb and rocksdb libraries.

#### Address Sanitizer
Use the CMake variable `-DNANO_ASAN=ON` or `-DNANO_ASAN_INT=ON` before running an executable.

### Valgrind

Valgrind can be used to find other issues such as memory leaks. A valgrind suppressions file is provided to remove some warnings. Valgrind can be run as follows (there are many options available):

```bash
valgrind --leak-check=full --track-origins=yes --suppressions=../valgrind.supp ./core_test
```
