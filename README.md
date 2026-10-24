# Garage Manager

[![Tests](https://github.com/lwrightqa/Garage-Manager/actions/workflows/tests.yml/badge.svg)](https://github.com/lwrightqa/Garage-Manager/actions/workflows/tests.yml)

A small command-line app for keeping a list of cars in a virtual garage. It was written to practice object-oriented Python, CSV file handling and unit testing with pytest.

## Features

- Add a car (color, year, make, model).
- List the cars in the garage.
- Delete a car by its number in the list.
- Save the garage to `garage.csv` after every change and load it on start-up.

## Getting started

You need Python 3.

```sh
git clone https://github.com/lwrightqa/Garage-Manager.git
cd Garage-Manager
python -m venv .venv          # optional, but recommended
pip install -r requirements.txt
python -m src.garage.garage
```

Run it from the project root. `garage.csv` is created in the folder you run it from.

## How it works

- **`Car`** holds the color, year, make and model, and prints as, for example, `Red 2020 Honda Civic`.
- **`Garage`** keeps the list of cars and handles `add_car`, `remove_car`, `save` and `load`.
- The menu functions (`prompt_for_new_car`, `list_cars`, `delete_car`) sit on top of `Garage` and handle input and display.
- Input is validated: a non-numeric year or an out-of-range car number is rejected with a message instead of crashing.
- A missing or corrupted `garage.csv` is handled by starting with an empty garage.

## Tests

```sh
pytest
```

There are 14 tests, and they run automatically on every push through GitHub Actions. They cover:

- Creating cars and their text output.
- Adding and removing cars, including an invalid index.
- Saving and loading, a missing file and a malformed file.
- The menu functions, using simulated user input: adding, listing, and deleting with valid, non-numeric and out-of-range entries.

## Project layout

```text
src/garage/garage.py    Car, Garage and the command-line menu
tests/test_garage.py    pytest suite
pytest.ini              test configuration
requirements.txt        dependencies (pytest)
```
