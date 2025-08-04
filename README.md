# Garage Manager

A simple, command-line application to manage a list of cars in a virtual garage.

This project demonstrates basic Python principles including class-based object-oriented programming, file I/O with CSV, and a complete test suite using pytest.

## Features

- Add new cars to the garage.
- List all cars currently in the garage.
- Delete cars from the garage.
- All data is persisted to a `garage.csv` file.

## Installation

1. Clone the repository.
2. It is recommended to create a virtual environment.
3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the main module from the root directory:

```sh
python -m src.garage.garage
```