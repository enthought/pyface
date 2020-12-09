---
name: Release Checklist
about: Use this template for upcoming releases.
title: "[Release Number] Release Checklist"
---

Target date:

Release Candidate by YYYY-MM-DD

Release by YYYY-MM-DD

Release candidate
-------------------
- [ ] Verify that all relevant PRs have been merged to master.
- [ ] Create a PR against master to bump version number, merge that PR
- [ ] From the commit just before bumping the version, create a new branch `maint/<release version number>`
- [ ] Update changelog and open PR targeting a new `maint/<release version number>` branch
- [ ] Update `ci-src-requirements.txt` if needed
- [ ] Check MANIFEST and requirements are still up to date.
- [ ] Update version in setup.py for the prerelease, open 2 PRs against `maint/<release version number>`
  - [ ] Create a new branch from `maint/<release version number>`: `git checkout maint/<release version number>`; `git pull`; `git checkout -b call-it-anything-you-like`
  - [ ] Set `PRERELEASE` to "rc1" and `IS_RELEASED` to true, commit, e.g. `git commit -m "Set IS_RELEASED to true for prerelease <release version number>rc1"`
  - [ ] Open and merge a PR against `maint/<release version number>`
  - [ ] Create a new branch from `maint/<release version number>`, Flip `IS_RELEASED` back to false, commit.
  - [ ] Open and merge another PR against `maint/<release version number>`
- [ ] Tag (annotated!) the release candidate on the commit where IS_RELEASED is set to true, e.g. `git tag -a -m "Release candidate <release version number>rc1" <release version number>rc1 <commit-hash>`
- [ ] Push the tag to GitHub
- [ ] Upload to PyPI
       - `git checkout <tag>`, `git clean -ffxd`, `python setup.py sdist`, `twine check dist/<...>.tar.gz`, `twine upload dist/<...>.tar.gz`
- [ ] Announcement for the release candidate

Release blockers
----------------
- [ ] (add blocking issues/PRs here)

Pre-release
---
- [ ] Backport PRs that have been merged to master to the maintenance branch. Use the "need backport ..." tag if there is one (but don't rely 100% on it)
- [ ] Verify that no other open issue needs to be addressed before the release.
- [ ] Test against other ETS packages and other ETS-using projects
- [ ] Check MANIFEST, requirements, changelog are still up to date.
- [ ] Test building the documentation

Release
-------
- [ ] Create branch `release/<release version number>` from `maint/<release version number>` branch.
  - [ ] Set release to `<release version number>`, and set `IS_RELEASED` is true; commit
  - [ ] Install from source distribution and run tests again
  - [ ] Open a PR against `maint/<release version number>` with this being the last commit so that CI is built on the release commit
  - [ ] Once CI is done building merge PR
  - [ ] Bump the micro version number i.e. `<release version number + 0.0.1>` and set `IS_RELEASED` to false; commit.
  - [ ] Open and then merge a separate PR against `maint/<release version number>`
- [ ] From the commit at which `IS_RELEASED` is true and version is `<release version number>`, tag (annotated!) `git tag -a -m "Release <release version number>" <release version number>`
- [ ] Push the tag `git push origin <release version number>`
- [ ] Make PR targeting `gh-pages` branch: Generate documentation and copy the content to the branch. Verify that the resulting index.html looks good.
- [ ] Upload to PyPI
- [ ] Test the PyPI package

Post-release
-------------
- [ ] Package update for `enthought/free` repository (for EDM)
- [ ] Backport release note and change log to master, and possibly `maint/<release version number>` branch.
- [ ] Update GitHub Release pages https://github.com/enthought/pyface/releases
- [ ] Announcement (e.g. Google Group)
