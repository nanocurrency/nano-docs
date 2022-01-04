title: Code Standards
description: Learn about the code standards expected when contributing to the nano protocol and node implementation

# Code standards

## Formatting

clang-format is used to enforce most of the formatting rules, such as:

* Tabs for indentation.
* Open braces go on new lines.
* Space before open parenthesis.
* Space after comma.

Running `ci/clang-format-all.sh` on \*nix systems is required before pushing your code to ensure that the formatting is good. If you want to do formatting from the IDE, chances are there's a plugin available. Visual studio for instance provides a way to automatically format on saving. The definition file `.clang-format` is located in the project root directory.

Make sure you set up your editor to use tabs. Use tabs for indentation, and spaces for alignment [^1]. That way, you can use any tab size you want in your favorite editor, but the code will still look good for people with different settings.

## General guidelines

* Use `auto` type inference for local variables if it's clear from the context what the type will be. Use your best judgement, sometimes adding explicit types can increase readability [^2]
* Handle exceptions, including IO exceptions for file and network operations.
* Be liberal with `debug_assert`. Use asserts to check invariants, not potential runtime errors, which should be handled gracefully. `debug_assert` has an advantage over normal `assert` as it will always print out the stacktrace of the current thread when it hits. Debug asserts are for detecting bugs, not error handling. There is also `release_assert` which is similar to `debug_assert` but also hits in a release build. When there is unexpected behaviour and no suitable way to recover it can be used to halt program execution.
* Be liberal with `logger.always_log` or `logger.try_log` statements, except in performance critical paths.
* Add comments to explain complex and subtle situations, but avoid comments that reiterates what the code already says.
* Use RAII and C++11 smart pointers to manage memory and other resources.

## Performance and scalabiliy considerations

* When making changes, think about performance and scalability. Pick good data structures and think about algorithmic complexity. 
    * Nested loops yield quadratic behavior - is there an alternative? A typical example is removing an inner lookup loop with an unordered set/map to improve lookup performance to O(1).
* Make sure your change doesn't conflict with the scalability characteristics described in the white paper.

## Security

Your code will be reviewed with security in mind, but please do your part before creating a pull request:

* Familiarize yourself with best practices for writing secure C++ code. In particular:
    * Consult https://wiki.sei.cmu.edu/confluence/display/cplusplus
    * Avoid using ANSI C functions. Many of these are prone to buffer overruns.
    * Avoid using C strings and direct buffer manipulation.

* Use static and dynamic analysis tools, such as valgrind, XCode instrumentation, linters and sanitizers. These tools are also great for debugging crashes and performance problems.

[^1]: https://dmitryfrank.com/articles/indent_with_tabs_align_with_spaces
[^2]: http://www.acodersjourney.com/2016/02/c-11-auto/