# 'main' branch
The main branch is, well, the main branch.

The only commits done to this branch are either:
- Changes in the README or docs
- Changes related to GitHub Actions
- New releases

DO NOT commit directly to the main branch EVER. For any proposed changes by you (ty for contributing btw), the commits must ALWAYS go to the 'dev' branch (see *docs/branch/dev*).
Unless the changes are just README/doc or GitHub actions changes, commits must always go to 'dev'. Afterwards once the program's ready for release, a new release branch will be made (see *docs/branch/release.md*), where bug fixes and testing will be done, and that is the time where the changes will be merged to main.
