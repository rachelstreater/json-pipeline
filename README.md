# Data Pipeline for JSON

Prototype for structuring Schedule of Notices of Lease data so that the column data and optional notes can be referenced independently. 

The application converts lines of text that run across columns into column data and outputs it in .csv format. 

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)

## Prerequisites

Before you begin, ensure you install the requirements: 

```pip install -r requirements.txt```

## Installation

To install the dependencies, follow these steps:


1. Navigate to the project directory:

    ```bash
    cd pdf-reader
    ```

2. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    - On Unix or MacOS:

        ```bash
        source venv/bin/activate
        ```

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the app, execute the following command:

```bash
python main.py
```

To run tests individually, execute the following commands:
```bash
python -m unittest tests/test_data_pipeline.py
```

```bash
python -m unittest tests/test_preprocessing_functions.py
```

## Improvements
Main things to improve on, given more time:
- Fix edge cases in output - some columns do not fit the required format, add another parsing layer to fix this. 
- Automate test runs with CI/CD
- Add a teardown to clean up after tests
- Extend unit tests to include integration and performance testing for larger model
