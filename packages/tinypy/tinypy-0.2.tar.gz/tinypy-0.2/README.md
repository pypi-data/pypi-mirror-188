# tinypy

tinypy is a Python library for converting JSON files to CSV files. It provides a simple and easy-to-use API for converting JSON data to CSV data. 

## Installation

```bash
pip install tinypy
```

## Usage

```python
from tinypy import JSONDriver

driver = JSONDriver()
driver.convert_json_to_csv(src="import.json", dest="export.csv")
```

This will convert the JSON file located at `import.json` to a CSV file located at `export.csv`.

## Command Line Interface

tinypy also provides a command line interface for converting JSON files to CSV files.

```bash
tinypy -s import.json -d export.csv
```

This command will convert the JSON file located at `import.json` to a CSV file located at `export.csv`.

## Advanced Usage

You can also read the json file from a variable instead of reading from a file by passing the json object to the function `convert_json_to_csv(json_data, dest)`

```python
from tinypy import JSONDriver
import json

json_data = json.loads('{"name":"John Smith","email":"john@example.com"}')

driver = JSONDriver()
driver.convert_json_to_csv(json_data, dest="export.csv")
```

This will convert the JSON data to a CSV file located at `export.csv`.

## Requirements

- Python 3.6 or higher

## License

This library is released under the MIT License.

## Contributing

We welcome contributions to tinypy. Please submit a pull request or an issue on GitHub if you have any improvements to suggest.

## Support

If you have any issues or questions, please feel free to reach out to us on GitHub.

## References

- More information can be found on the [GitHub page](https://github.com/yourusername/jsoncsvconverter)

## Acknowledgements

- Thanks for the developer that motivated me to create this library.
