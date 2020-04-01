# Rasp-O-Clocker

[![Build Status](https://img.shields.io/travis/sbreining/rasp-o-clocker?label=Travis%20CI&style=plastic)](https://travis-ci.org/sbreining/rasp-o-clocker)
[![Coverage Status](https://img.shields.io/coveralls/github/sbreining/rasp-o-clocker?label=Coverage&style=plastic)](https://coveralls.io/github/sbreining/rasp-o-clocker?branch=master)
![License Status](https://img.shields.io/github/license/sbreining/rasp-o-clocker?label=License&style=plastic)
![Language Status](https://img.shields.io/github/languages/top/sbreining/rasp-o-clocker?label=Python&style=plastic)

This project was started in an attempt to gain familiarity with different tools.
The first was to expand my knowledge of, and practice using Python. Further, it
was to learn about virtual environments, incorporating other packages into my
own project, and automating a redundant task. Additionally, I utilized SQLite,
an RDBMS to help manage clock punches and help resume in the event of an
application crash. I also incorporated (insecurely) a sort of pager system that
utilizes a GMail account to forward a text notifying of events occurring. This
way, if something got missed, or the application crashed, it could manually be
updated. Lastly, this was merely a learning process and not a tool that was ever
used. I happened to be promoted before it even could be used.


### Installation

1. Clone the repo: `git clone https://github.com/sbreining/rasp-o-clocker.git`
2. Navigate into directory: `cd rasp-o-clocker`
3. Install dependencies: `pip install`
4. Copy environment sample: `cp .env.sample .env`
5. Fill in any necessary information in the `.env` file you just created.
6. Run migration: `python scripts/migrate`

After the migration is run, 10 holidays will be in the `holidays` table that
are based on my current work place's holidays for the year of 2020. Anything
that needs to be adjusted, added, or otherwise is up to you.

### Usage

`python main.py`

The idea is to run this with a process manager to ensure it stays running on
hardware that can stay active. My intended device was a raspberry pi, hence the
name `Rasp-O-Clocker`.

### Testing

Using `pytest`, all test file names will go by `<filename>_test`. Test methods
and functions are required by `pytest` to be `test_<method_name>`. And test
classes are required to be `Test<class_name>`.

Run test suite with: `python -m pytest`

For coverage run with: `coverage run -m pytest`

And to prettify the coverage run: `coverage html`

### Copyright

MIT License

Copyright (c) 2020 Shane Breining

(See `LICENSE`)