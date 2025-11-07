# Feature branches
Feature branches are dedicated branches for working on, well, features.

Identifying feature branches can be tricky, but usually their name is anything BUT:
- main
- dev (see *docs/branch/dev*)
- release/*
- hotfix/*

So, for example, if a branch is called 'this', it's probably a feature branch. But if it's called, let's say, 'hotfix/this' then it's not. In this case it would be a hotfix branch (see *docs/branch/hotfix.md*)

Feature branches are usually made by me when I want to add new features for a future update. More info on the feature is usually found at the README on the feature branch.

When contributing, you can make a new feature branch on your fork of the repository (ALWAYS branch it off 'dev'). Once the feature is done, you can do a pull request for the 'dev' branch, and if accepted, the feature will be added to 'dev' and will be on the next release
