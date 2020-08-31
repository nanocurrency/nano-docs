title: Contributing code to the Nano node | Nano Documentation

# Contributing code to the Nano node

## About the code base

Nano is written in C++14 and supports Linux, macOS and Windows.

**Libraries**

We use Boost to help us write efficient cross platform code, including the async IO library for networking (asio).

Make sure you have the correct [Boost version](https://github.com/nanocurrency/nano-node/search?utf8=%E2%9C%93&q=find_package+%28Boost&type=) installed.

**Submodules**

| **Name**                        | **Details** |
|                                 |             |
| cryptopp                        | Provides the implementation for random number generator, SipHash, AES and other cryptographic schemes. |
| phc&#x2011;winner&#x2011;argon2 | When encrypting with AES, the password first goes through key derivation, and argon2 is our hash of choice for doing that. |
| lmdb     			              | The database library used for the ledger and wallet, with local patches for Windows. This is a very fast and portable key/value store with ordered keys. It is extremely resilient to crashes in the program, OS, and power-downs without corruption. |
| miniupnp 			              | This library is used to do port mapping if the gateway supports it. |

**Qt Wallet**

To build the GUI, set the `NANO_GUI` flag in cmake. The desktop wallet uses Qt5, but without the MOC compiler. Hence, you cannot use the signals and slots mechanism.

The majority of the Qt wallet code resides in the `qt` subproject, while the QApplication startup code resides in `nano_wallet`.

**Using CMake**

CMake is used to generate build files and project files for various IDE's.

Please familiarize yourself with basic cmake usage, such as how to change cache variables via the command line, ccmake or CMake GUI. This is much more convenient that editing the `CMakeLists.txt` file directly.

Find out more about building in [Integration Guides Build Options](/integration-guides/build-options).

## Testing

**Add tests**

If you add new functionality, adding unit tests to avoid regressions in the future is required.

The easiest way to get started writing your first test is to base it off one of the existing tests. You'll find these in the `core_test` directory.

Make sure the `NANO_TEST` cache variable in cmake is set. You should also switch the `ACTIVE_NETWORK` variable to nano_test_network. 

**Run tests before creating a pull request**

Please run the tests before submitting a PR. Go to the build directory and run the `core_test` binary.

If you get a lot of failures, such as `frontier_req.begin` failing, make sure `ACTIVE_NETWORK` is set to `nano_test_network`

## GitHub collaboration

Communication is the key to working together efficiently. A good way to get in touch with the developers is to join the #development channel on [Discord](https://chat.nano.org/). If you have an idea of an improvement or new feature, consider discussing it first with the team, either on Discord, or by adding an issue. Maybe someone is already working on it, or have suggestions on how to improve on the idea.

!!! warning "Security Vulnerability Disclosure"
	**Do NOT discuss potential security vulnerabilities on the issue tracker, public forums or open discussion channels**

	If you discover a bug you believe to pose a security risk to the Nano network, please contact bugs@nano.org with a proof of concept with full details of the bug including:
	
	* Repository of the bug
	* High-level summary
	* Detailed description
	* Steps to reproduce
	* Supporting material/references
	* The potential security impact of the bug

### Code Process

#### Fork and do all your work on a branch

Nano prefers the standard GitHub workflow. You create a fork of the Nano repository, make branches for features/issues, and commit and push these. 

#### Create pull requests

Before:

* Branch out of the **develop** branch. The **master** branch is only updated on new releases.
* Review your code locally. Have you followed the guidelines in this document?
* Run tests. Did you consider adding a test case for your feature?
* Run ASAN and TSAN to detect memory or threading bugs
* Commit and push your fork
* Create pull request on the upstream repository:
    * Make sure you add a description that clearly describes the purpose of the PR.
    * If the PR solves one or more issues, please reference these in the description.

After:

* Check that CI completes successfully. If not, fix the problem and push an update.
* Respond to comments and reviews in a timely fashion.

#### Resolve conflicts

If time passes between your pull request (PR) submission and the team accepting it, merge conflicts may occur due to activity on develop, such as merging other PR's before yours. In order for your PR to be accepted, you must resolve these conflicts.

The preferred process is to rebase your changes, resolve any conflicts, and push your changes again. [^2][^3]

* Check out your branch
* `git fetch upstream`
* `git rebase upstream/develop`
* Resolve conflicts in your favorite editor
* `git add {filename}`
* `git rebase --continue`
* Commit and push your branch

**Consider squashing or amending commits**

In the review process, you're likely to get feedback. You'll commit and push more changes, get more feedback, etc. 

This can lead to a messy git history, and can make stuff like bisecting harder.

Once your PR is OK'ed, please squash the commits into a one.[^4]

Note that you can also update the last commit with `git commit --amend`. Say your last commit had a typo. Instead of committing and having to squash it later, simply commit with amend and push the branch.

## Code standard

### Formatting

clang-format is used to enforce most of the formatting rules, such as:

* Tabs for indentation.
* Open braces go on new lines.
* Space before open parenthesis.
* Space after comma.

Please run `ci/clang-format-all.sh` before pushing your code to ensure that the formatting is good. If you want to do formatting from the IDE, chances are there's a plugin available. The definition file `.clang-format` is located in the project root directory.

Make sure you set up your editor to use tabs. Use tabs for indentation, and spaces for alignment [^5]. That way, you can use any tab size you want in your favorite editor, but the code will still look good for people with different settings. 

### Coding guidelines

* Use `auto` type inference for local variables if it's clear from the context what the type will be. Use your best judgement, sometimes adding explicit types can increase readability [^1]
* Handle exceptions, including IO exceptions for file and network operations.
* Be liberal with `assert`. Use asserts to check invariants, not potential runtime errors, which should be handled gracefully. Asserts are for detecting bugs, not error handling.
* Be liberal with `BOOST_LOG` statements, except in performance critical paths.
* Add comments to explain complex and subtle situations, but avoid comments that reiterates what the code already says.
* Use RAII and C++11 smart pointers to manage memory and other resources.

### Performance and scalabiliy considerations

* When making changes, think about performance and scalability. Pick good data structures and think about algorithmic complexity. 
    * For small data sets, std::vector should be your to-go container, as a linear scan through contiguous memory is often faster than any alternative.
    * Nested loops yield quadratic behavior - is there an alternative? A typical example is removing an inner lookup loop with a map.
* Make sure your change doesn't conflict with the scalability characteristics described in the white paper. 
 
### Security

Your code will be reviewed with security in mind, but please do your part before creating a pull request:

* Familiarize yourself with best practices for writing secure C++ code. In particular:
    * Consult https://wiki.sei.cmu.edu/confluence/display/cplusplus
    * Avoid using ANSI C functions. Many of these are prone to buffer overruns.
    * Avoid using C strings and direct buffer manipulation.

* Use static and dynamic analysis tools, such as valgrind, XCode instrumentation, linters and sanitizers. These tools are also great for debugging crashes and performance problems.

## General tips for contributors

* Read the [white paper](https://nano.org/en/whitepaper)
* Peruse the code and don't be shy about asking questions if there are parts you don't understand.
* Make sure you understand the GitHub workflow.
* Participate in the community by reading and replying to GitHub issues, Reddit posts and tweets. This gives you a great insight into the pain points that exists with the software.

[^1]: http://www.acodersjourney.com/2016/02/c-11-auto/
[^2]: https://help.github.com/articles/resolving-merge-conflicts-after-a-git-rebase/
[^3]: https://help.github.com/articles/resolving-a-merge-conflict-using-the-command-line/
[^4]: https://github.com/todotxt/todo.txt-android/wiki/Squash-All-Commits-Related-to-a-Single-Issue-into-a-Single-Commit
[^5]: https://dmitryfrank.com/articles/indent_with_tabs_align_with_spaces
