# Release branches
Release branches (typically called 'release/*') are branches branched off 'dev' (see *docs/branch/dev*) that are, tldr, the final stage of a new update before it's released.

Usually, once enough changes are done, a new 'release/*' branch gets made off 'dev'. In here testing and bug fixing is done (really only major commits to the release branch are bug fixes), and once it's ready, the branch will merge into 'dev' and 'main', and the new release will be made.

When contributing, updates to the release branch should only be bug fixes. Any other changes will not be accepted.
