# Rasp-O-Clocker

This project was started in an attempt to gain familiarity with different tools.
The first was to expand my knowledge of, and practice using Python. Further, it
was to learn about virtual environments, incorporating other packages into my
own project, and automating a redundant task.

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

The idea is to run this with a process manager (like `supervisord`) to ensure it
stays running on hardware that can stay active. My intended device was a
raspberry pi, hence the name `Rasp-O-Clocker`.

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