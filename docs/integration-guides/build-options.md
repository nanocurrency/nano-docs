title: Integration Guides - Build Options
description: Instructions for manually building the Nano node for a variety of operating systems

# Build Options

--8<-- "warning-only-official-builds-supported.md"

## Official release builds
 
Throughout the development cycle and after releases official builds of the node for Docker, Linux, macOS and Windows are generated and published for test, beta and main networks.

=== "Main network"

    --8<-- "current-build-links-main.md"

=== "Test network"

    --8<-- "current-build-links-test.md"

=== "Beta network"

    --8<-- "current-build-links-beta.md"

## Nano Directory

### Contents

--8<-- "directory-contents.md"

### Locations

=== "Main network"

    --8<-- "directory-locations-main.md"

=== "Test network"

    --8<-- "directory-locations-test.md"

=== "Beta network"

    --8<-- "directory-locations-beta.md"

??? tip "Moving directory locations"
    Some users desire to change the blockchain download location. A solution is available for the no gui nano_node (see https://github.com/nanocurrency/nano-node/issues/79), but no concrete solution is available for the GUI client. However, a workaround can be acheived via the use of symbolic links. Below is a short tutorial for Windows builds:

    1. Rename/delete the Nano directory in your `appdata` Local directory (if you haven't run the wallet yet, skip this step). This is necessary because the command to create a symbolic link in windows will fail if the the input directory already exists.
    1. Decide on where you want to store the blockchain and create a symbolic link. The command is (in an administrative command-prompt): `mklink /d "C:\Users\<user>\AppData\Local\Nano\" "E:\Some\Other\Directory"`. This command creates a symbolic link for a directory (`/d`) that 'redirects' all requests for files/directories in the `Local\Nano` directory to the `Other\Directory`. This means that a file created in the input directory will actually be in the output directory (on the other disk).
    1. Verify it works. Create a file in your Nano directory in your appdata, and you should see it appear in the directory you linked it to (and vice-versa). If you have old wallets or a partially-downloaded blockchain, copy them back into the local directory. Start the wallet.

---

## Requirements & setup

--8<-- "warning-unsupported-configuration.md"

### Boost

The node build commands further down include bootstrapping Boost, but [pre-built binaries](https://sourceforge.net/projects/boost/files/boost-binaries/) can be used for Windows as well, or you can optionally build from the downloaded source instead as follows:

* Download [Boost 1.70+](http://www.boost.org/users/history/version_1_70_0.html)
* Extract to \[boost.src\]
* From inside [boost.src] run:

=== "*nix"
    ```bash
    ./bootstrap.sh --with-libraries=context,coroutine,filesystem,log,program_options,system,thread
    ./b2 --prefix=[boost] --build-dir=[boost.build] link=static install
    ```

=== "macOS"
    ```bash
    ./bootstrap.sh --with-libraries=context,coroutine,filesystem,log,program_options,system,thread
    ./b2 --prefix=[boost] --build-dir=[boost.build] link=static install
    ```

=== "Windows"
    ```bash
    ./bootstrap.sh --with-libraries=context,coroutine,filesystem,log,program_options,system,thread
    ./b2 --prefix=[boost] --build-dir=[boost.build] address-model=64 link=static install
    ```

If using this option, remove `bash util/build_prep/bootstrap_boost.sh -m` from the [build command](#build-commands) below.

### Qt wallet

If building the Qt-based `nano_wallet`, first download [Qt 5.9.5+ open source edition](https://www.qt.io/download) and extract to [qt.src]. In [qt.build] execute:

=== "*nix"
    ```bash
    [qt.src]/configure -shared -opensource -nomake examples -nomake tests -confirm-license  -prefix [qt]
    make
    make install
    ```

=== "macOS"
    ```bash
    [qt.src]/configure -shared -opensource -nomake examples -nomake tests -confirm-license  -prefix [qt]
    make
    make install
    ```

=== "Windows"
    ```bash
    [qt.src]/configure -shared -opensource -nomake examples -nomake tests -confirm-license  -prefix [qt]
    nmake
    nmake install
    ```

### Node

=== "*nix"
    **Required build tools**

    * CMake >= 3.8
    * Clang >= 5 or GCC >= 7


    === "Debian"
        **Version**

        * Debian 8 Jessie (Debian 8 requires Cmake 3.8+)
        * Debian 9 Stretch

        **Install dependencies**

        ```bash
        sudo apt-get update && sudo apt-get upgrade
        sudo apt-get install git cmake g++ curl wget
        ```

    === "Ubuntu"
        **Version**
        
        * Ubuntu 18.04 LTS Server
        * Ubuntu 18.10+

        **Install dependencies**

        ```bash
        sudo apt-get update && sudo apt-get upgrade
        sudo apt-get install git cmake g++ curl wget
        ```

    === "CentOS"
        **Version**
        
        * CentOS 7

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

    === "Arch Linux"

        **Install dependencies**

        ```bash
        pacman -Syu
        pacman -S base-devel git gcc cmake curl wget
        ```

=== "macOS"
    **Required build tools**
    
    * CMake >= 3.8
    * XCode >= 9

=== "Windows"
    **Required build tools**

    * CMake >= 3.8
    * NSIS package builder
    * [Visual Studio 2017 Community](https://my.visualstudio.com/Downloads?q=visual%20studio%202017&wt.mc_id=o~msft~vscom~older-downloads) (or higher edition, if you have a valid license. eg. Professional or Enterprise)
        * Select **Desktop development with C++**
        * Select the latest Windows 10 SDK

---

## Build commands

### Node

The process below will create a release build of the node for the main network. See [network options](#network-options) below for details on building for the test or beta networks.

=== "*nix"
    ```bash
    git clone --branch V22.1 --recursive https://github.com/nanocurrency/nano-node.git nano_build
    cd nano_build
    export BOOST_ROOT=`pwd`/../boost_build
    bash util/build_prep/bootstrap_boost.sh -m
    cmake -G "Unix Makefiles" .
    make nano_node
    cp nano_node ../nano_node && cd .. && ./nano_node --diagnostics
    ```

=== "macOS"
    ```bash
    git clone --branch V22.1 --recursive https://github.com/nanocurrency/nano-node.git nano_build
    cd nano_build
    export BOOST_ROOT=`pwd`/../boost_build
    bash util/build_prep/bootstrap_boost.sh -m
    cmake -G "Unix Makefiles" .
    make nano_node
    cp nano_node ../nano_node && cd .. && ./nano_node --diagnostics
    ```

=== "Windows"

    **Setup**

    *Download Source*

    Using git_bash:
    ```bash
    git clone --branch V22.1 --recursive https://github.com/nanocurrency/nano-node
    cd nano-node
    ```

    *Create a `build` directory inside nano-node (makes for easier cleaning of build)*

    Using git_bash:
    ```bash
    mkdir build
    cd build
    ``` 
    * **Note:** all subsequent commands should be run within this "build" directory.

    *Get redistributables*

    Using Powershell:
    ```bash
    Invoke-WebRequest -Uri https://aka.ms/vs/15/release/vc_redist.x64.exe -OutFile .\vc_redist.x64.exe
    ```

    *Generate the build configuration.*

    Using 64 Native Tools Command Prompt:

    * Ensure the Qt, Boost, and Windows SDK paths match your installation.

    ```bash
    cmake -DNANO_GUI=ON -DQt5_DIR="C:\Qt\5.9.5\msvc2017_64\lib\cmake\Qt5" -DNANO_SIMD_OPTIMIZATIONS=TRUE -DBoost_COMPILER="-vc141" -DBOOST_ROOT="C:/local/boost_1_70_0" -DBOOST_LIBRARYDIR="C:/local/boost_1_70_0/lib64-msvc-14.1" -G "Visual Studio 15 2017 Win64" -DIPHLPAPI_LIBRARY="C:/Program Files (x86)/Windows Kits/10/Lib/10.0.17763.0/um/x64/iphlpapi.lib" -DWINSOCK2_LIBRARY="C:/Program Files (x86)/Windows Kits/10/Lib/10.0.17763.0/um/x64/WS2_32.lib" ..\.
    ```

    **Build**
    	
    * Open `nano-node.sln` in Visual Studio
    * Build the configuration specified in the previous step
    * Alternative using 64 Native Tools Command Prompt:

    ```bash 
    cmake --build . --target ALL_BUILD --config %CONFIGURATION% -- /m:%NUMBER_OF_PROCESSORS%
    ```

    **Package up binaries**

    Using 64 Native Tools Command Prompt:

    * Replace **%CONFIGURATION%** with the build configuration specified in previous step
    * Replace **%GENERATOR%** with NSIS (if installed) or ZIP

    ```bash 
    cpack -G %GENERATOR% -C %CONFIGURATION%
    ```

### Qt wallet

This is only required when the Qt wallet with GUI is needed.

`make nano_wallet`

### RPC server

This is only required for when the RPC server is being [run as a child process or outside the node process completely](advanced.md#running-nano-as-a-service).

`make nano_rpc`

---

## Additional build details

### Node

#### CMake variables

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
* `NANO_ASIO_HANDLER_TRACKING=10` (Output asio diagnostics for any completion handlers which have taken longer than this in milliseconds. For more information see the description of the PR [#2681](https://github.com/nanocurrency/nano-node/pull/2681))
* `NANO_FUZZER_TEST=ON` (Build the fuzz tests, not available on Windows)

#### Building a package

=== "*nix"
    `cpack -G "TBZ2"`

=== "macOS"
    `cpack -G "DragNDrop"`

=== "Windows"
    `cpack -G "NSIS"`

#### Network options

**Main network**

The default build network is the main network. No option needs to be specified.

**Test Network**

* To run a node on the test network, set CMake variable: `-DACTIVE_NETWORK=nano_test_network`
* More information can be found on the [Test Network page](../running-a-node/test-network.md)

**Beta Network**

* To run a node on the beta network, set CMake variable: `-DACTIVE_NETWORK=nano_beta_network`
* More information can be found on the [Beta Network page](../running-a-node/beta-network.md)

## Testing

A number of tests binaries can be built when the CMake variable `-DNANO_TEST=ON`. With this variable set, `make` will also build test files, and will produce `core_test`, `rpc_test`, `load_test` and `slow_test` binaries, which can be executed:

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
