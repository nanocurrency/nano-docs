title: Collaboration Process
description: Find out how the open source collaboration process works with the nano protocol and node software

# Collaboration Process

## Code Process

**Fork and do all your work on a branch**

Nano prefers the standard GitHub workflow. You create a fork of the nanocurrency/nano-node repository (or other repositories as needed), make changes on new branches for features/fixes, and push these up to be added as Pull Requests. 

**Create pull requests**

Before:

* Branch out of the **develop** branch. The **master** branch is only updated on new releases.
* Review your code locally. Have you followed the [Code Standards](code-standards.md) closely?
* Run tests. Did you consider adding a test case for your feature?
* Run ASAN, TSAN and Valgrind to detect memory, threading or other bugs
* Commit and push your fork branch

After:

* Create pull request on the upstream repository:
    * Make sure you add a description that clearly describes the purpose of the PR.
    * If the PR solves one or more issues, please reference these in the description.
* Check that CI completes successfully - this can take up to a few hours depending on current CI queues. If any failures exist, fix the problem and push an update.
* Respond to comments and reviews in a timely fashion.

**Resolve conflicts**

If time passes between your pull request (PR) submission and the team accepting it, merge conflicts may occur due to activity on develop, such as merging other PR's before yours. In order for your PR to be accepted, you must resolve these conflicts.

The preferred process is to rebase your changes, resolve any conflicts, and push your changes again. [^1][^2]

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

Once your PR is OK'ed, please squash the commits into a one.[^3]

Note that you can also update the last commit with `git commit --amend`. Say your last commit had a typo. Instead of committing and having to squash it later, simply commit with amend and push the branch.

## Finding issues or features to work on

- Issues are available on GitHub, with the most urgent being in the latest milestone for release
- Start with issues labeled as [`good first issue`](https://github.com/nanocurrency/nano-node/labels/good%20first%20issue) or connect with the NF core developers on [Discord](https://chat.nano.org) or the [forum](https://forum.nano.org) for ideas on how to help
- If you find an issue you'd like to help with, comment and tag a [Nano Foundation team member](https://github.com/orgs/nanocurrency/people) who can evaluate and assign it to you

## Submitting issues and feature requests

Standard GitHub templates exist for submitting any found issues or feature requests. If you plan on working on a bug or feature that doesn't already have a GitHub Issue associated with it, please submit it first so the team is aware. See https://github.com/nanocurrency/nano-node/issues/new/choose for templates.

## Discussion channels

Various channels exist for discussing code changes with the Nano Foundation and community.

**GitHub**

To help persist useful information about a particular issue or feature, it is best to discuss within the related GitHub Issue or Pull Request. Members of the nano community and Nano Foundation actively follow and will engage when available.

**Discord for chat**

For live chat, join the server at https://chat.nano.org and check out the `#protocol` and `#development` channels. The various channels under the `TESTING` section can also be helpful to follow.

**Forum**

Another area for technical and code related discussions is the [forum](https://forum.nano.org). There are categories for `Protocol Design` and `Development` that are useful in discussing ideas. This can be a great place for getting feedback on ideas and exploring further before finalizing fixes and features in GitHub.

## Proposals

There currently is no formal process for proposals on the nano network. This is an area actively being investigated and if requirements for submissions change, this area will be updated. For now, if you wish to propose an new idea, it is recommended to discuss on the [forum](https://forum.nano.org) first to gather feedback and use the [GitHub Issues](https://github.com/nanocurrency/nano-node/issues/new/choose) on the concept is solidifed/validated.

[^1]: https://help.github.com/articles/resolving-merge-conflicts-after-a-git-rebase/
[^2]: https://help.github.com/articles/resolving-a-merge-conflict-using-the-command-line/
[^3]: https://github.com/todotxt/todo.txt-android/wiki/Squash-All-Commits-Related-to-a-Single-Issue-into-a-Single-Commit