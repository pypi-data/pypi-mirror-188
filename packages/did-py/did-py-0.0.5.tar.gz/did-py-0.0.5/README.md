# did
a simple task manager

[![Build](https://github.com/shnupta/did/actions/workflows/python-app.yml/badge.svg)](https://github.com/shnupta/did/actions/workflows/python-app.yml)
[![PyPI version](https://badge.fury.io/py/did-py.svg)](https://badge.fury.io/py/did-py)

## install
```
pip install did-py
```

## usage
```
usage: did [-h] [-s SEARCH] [date]

what did i do?

positional arguments:
  date                  open the did file for this date (try "monday", "thisweek", "lastweek" or "yesterday"!)

optional arguments:
  -h, --help            show this help message and exit
  -s SEARCH, --search SEARCH
                        search for text in did files
```

when you open a new did file for the current day, any unfinished tasks from yesterday or last week will be copied into today's file.

an example did file looks like this:
```
# Monday 30 January 2023 - Week 5
- [ ] Some unfinished task
  - A note on an unfinished task
- [ ] Another finished task
- [X] I managed to do this today!
```

## build
this project uses [vulcan](https://github.com/optiver/vulcan-py):
```
pip install vulcan-py[cli]
vulcan develop
```