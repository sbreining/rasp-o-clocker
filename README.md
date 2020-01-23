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
6. Run migration: `python bin/migrate`

After the migration is run, a few days of the year will be added to the 
`holidays` table (January 1st, July 4th, and December 25th). If there are more
holidays you or your company wishes to observe, you'll need to add them
yourself.

### Usage

`python main.py`

The idea is to run this with a process manager (like `supervisord`) to ensure it
stays running on hardware that can stay active. My intended device was a
raspberry pi, hence the name `Rasp-O-Clocker`.

### Intended Features

- Implement the punches to be recorded in the database.
- Use clock times from the `.env` so it is more customizable.
- Consider ORM, but may be overkill.
  - If not ORM, at least create the models to handle each table separately.

### Copyright

MIT License

Copyright (c) 2020 Shane Breining

(See `LICENSE`)