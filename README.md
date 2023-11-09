# Code Assignment: Data Augmentation

## Background

A `sample_orders.json.gz` gzipped file in the JSON-Lines format was provided. This file contains sample user order events from an e-commerce website that are pulled from an API.

## Problem

Inside the `sample_orders.json.gz` file, a `USER_AGENT` column can be found. The `USER_AGENT` column should be parsed and three new columns should be derived:

1. Device Type (Mobile, Computer, Tablet, Other, etc)
2. Browser Type (Safari, Firefox, etc)
3. Browser Version

### Requirements and Rules

- You can use any publicly available libraries (recommended for the user-agent parsing).
- The app should read the `sample_orders.json.gz` file and write a new file with the additional columns called `sample_orders_transformed.json.gz`.
- Add some tests to prove the newly added functionality is working properly.
- There may be some data quality issues. Please be explicit in tests/logic with how you handle them.
- Zip your project up and send this back to us!
- There are no timelines on completing this take-home, but the sooner the better.
- Please implement your solution in Python, Scala, or Java.

---

# Development

## Up and Running

Before running the application, the required dependencies should be installed. Use the provided `requirements.txt` file with the following command:

```bash
pip install -r requirements.txt
```

To run the application, execute:

```bash
python app/main.py
```

After running the script, the `sample_orders_transformed.json.gz` file will be located in `app/data/output`.

## Tests

From the project's root directory, run the tests using the following command:

```bash
pytest
```

More test cases can be added in the `test_data.json` file located in `tests`.

## Core Libraries

- **user-agents**: library used for parsing the `USER_AGENT` column. It extracts device and browser information.
- **pandas**: library used to convert the JSON data into a DataFrame and apply the parsing to the `USER_AGENT` column.
- **pytest**: framework used for test writing and execution to assert the correctness of the app. The test cases were generated using an [online user agent parser](https://explore.whatismybrowser.com/useragents/parse/).
- **logging**: built-in logging library used for creating info and error log messages.
- **gzip**: library used to work with gzip-compressed files and streams.
- **json**: built-in library used to parse, serialize, and manipulate JSON data.

---

# Next Steps

The project can be enhanced further by implementing the following features:

- **Browser Version Detailing**:
  The `user-agents` library, which relies on `ua-parser`, does not capture the patch-minor version details for operating systems or browsers. The existing parser class can be extended to extract and include the patch-minor version, providing more granular browser version information.

- **Robust Data Validation**:
  A library like `great_expectations` can be integrated to define and enforce data quality checks, creating a validation layer that can catch anomalies and inconsistencies in the data early in the pipeline.

- **Flexible Data Transformation**:
  As business requirements evolve, new data transformations may be required. A Factory design pattern can be implemented for transformation functions, making it easy to add new types of transformations as modular components can be tested and maintained separately.

- **Application Containerization**:
  The application can be containerized using Docker to encapsulate the environment and dependencies, ensuring that it runs the same in any Docker-supported system. This will simplify deployment and scaling across development, testing, and production environments.
