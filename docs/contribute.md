# Contributing
Tysm for contributing to this project! Help is always needed as working in this project solo isn't the easiest thing ever...
However, it's important you know what you can and can't do when contributing.

## Branches
The branches you will find here are usually:
- `main`
- `dev` (see *docs/branch/dev.md*)
- `*` (feature branches, see *docs/branch/feat.md*)
- `hotfix/*` (see *docs/branch/hotfix.md*)
- `release/*` (see *docs/branch/release.md*)

`main` is reserved for only the final production-ready release.

When contributing, any changes MUST be based off `dev`, and MUST be commited to `dev`. No changes should be commited to `main` directly unless it's changes to the README/docs, or to GitHub Actions.

Hotfix branches are usually reserved for critical bug fixes. Only commits expected to this branch are bug fixes.

Release branches are for testing and bug fixing a new update (aka, the final stage for a new release to come). Only commits expected to this branch are bug fixes.

For more info on the branches and what they do, see *docs/branch*

## How to contribute
First, it's important you know, this project's currently on Python 3.13.3.

With that in mind, first step is forking the repository. Just go to the GitHub, and hit the "Fork" button.

Then in your local machine, clone your fork of the repo:
```sh
git clone "https://github.com/<username>/<fork>.git"
cd "<fork>"
```

Replace `<username>` and `<fork>` with your GitHub username and the name of your fork.

Optionally, you can add this repo as a remote:
```sh
git remote add upstream "https://github.com/sxnt7x/ihavebeensummoned"
```

### Adding features
First, it's reccommended to make a new feature branch
```sh
git branch <feature-name> dev # ALWAYS branch it off dev
```

In there you can work on your feature. Once it's ready and tested, commit your changes:
```sh
git add .
git commit -m "feat: feature details" # Replace "feature details" with the actual feature details
git push origin <feature-name>
```

Now go to your fork, and make a PR targeted towards the `dev` branch (NEVER target it towards `main`). Make sure to include what you added, what notable changes you did, why did you add what you did, tested devices, etc.

Now I'll review the PR, and if I like it, and find no issues with it, I'll accept it, and your feature will be added to the next version.
If I find issues with it, I'll request changes. Make sure to make any requested changes to the PR.

### Bug fixing
Now, when bug fixing, ask yourself: is this a critical bug? If so, then follow the steps on the ***Hotfix*** section.
If not, follow the steps here.

First, report the issue to the GitHub in the issues tab. If I say I can fix it, I'll assign the issue to myself. If I can't, I'll assing the issue to you.
If it gets assigned to you, fork the repository and start fixing the bug with the steps below.

The changes can be done directly to the `dev` branch. No need for a separate branch.

In there you can fix the bug. After some testing, if everything's fine, commit your changes:
```sh
git add .
git commit -m "fix: bugfix details" # Replace "bugfix details" with the actual bugfix details
git push origin dev
```

Now, go yo your fork, and make a PR targeted towards the `dev` branch. Make sure to include what was the bug, what changes did you do to fix it, tested devices, etc.

Now I'll review the PR, and if I don't find any issues with it, I'll accept it, and the bug will be patched in the next version.
If I find issues with it, I'll request changes. Make sure to make any requested changes to the PR.

### Hotfixes
Hotfixes are only for critical bugs that break the application.

First, report the issue to the GitHub in the issues tab. If I say I can fix it, I'll assign the issue to myself. If I can't, I'll assing the issue to you.
If it gets assigned to you, fork the repository and start fixing the bug with the steps below.

First, it's reccommended to make a hotfix branch:
```sh
git branch hotfix/<hotfix-name> dev # ALWAYS branch it off dev
```

In there you can work in the hotfix. Once it's ready and tested, commit your changes:
```sh
git add .
git commit -m "fix: hotfix details" # Replace "hotfix details" with the actual hotfix details
git push origin hotfix/<hotfix-name>
```

Now go to your fork, and make a PR targeted towards the `main` branch (hotfixes are targeted towards the `main` branch). Make sure to include what was the bug, what changes did you do to fix it, tested devices, etc.

Now I'll review the PR, and if I don't find any issues with it, I'll accept it, and the hotfix will be published.
If I find issues with it, I'll request changes. Make sure to make any requested changed to the PR.
