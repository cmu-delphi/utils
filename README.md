# Status
[![Deploy Status](http://delphi.midas.cs.cmu.edu/~automation/public/github_deploy_repo/badge.php?repo=cmu-delphi/utils)](#)

# About
Utilities used across many Delphi projects.

# Development

## Prerequisites

- Create the root directory for all Delphi packages.
  - `mkdir -p delphi`

## Installation

- Clone this repo.
  - `git clone https://github.com/cmu-delphi/utils.git`
- Add a link to this repo to the delphi package.
  - `ln -s ../utils/src delphi/utils`

## Testing

- Clone the py3tester repo.
  - `git clone https://github.com/undefx/py3tester.git`
- Run the tests.
  - `python3 py3tester/src/py3tester.py --color --full utils/tests`
