# Automatic Test Case Generator

A powerful command-line utility that automatically generates comprehensive pytest test cases for Python functions using Google's Gemini LLM.

## 🚀 Features

- **AI-Powered Test Generation**: Uses Google's Gemini LLM to create intelligent test cases
- **Comprehensive Analysis**: Analyzes function signatures, parameters, return types, and complexity
- **Multiple Test Types**: Generates normal cases, edge cases, and error handling tests
- **Easy CLI Interface**: Simple command-line interface with colored output
- **Flexible Configuration**: Customizable settings via environment variables
- **Batch Processing**: Generate tests for single functions or entire files
- **Smart Code Analysis**: Extracts function metadata including docstrings and decorators

## 📋 Requirements

- Python 3.7+
- Google Gemini API key
- Required Python packages (see `requirements.txt`)

## 🛠️ Installation

1. Clone or download the project files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your configuration:
   ```bash
   python pytest.py setup
   ```
   Or manually copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   # Edit .env with your Gemini API key
   ```

## 🔑 Configuration

Create a `.env` file with the following variables:

```env
# Required: Your Google Gemini API key
GEMINI_API_KEY=your_gemini_api_key_here

# Optional configurations
GEMINI_MODEL=gemini-pro
MAX_TEST_CASES=10
INCLUDE_EDGE_CASES=true
INCLUDE_ERROR_CASES=true
OUTPUT_DIR=generated_tests
VERBOSE=false
```

## 📖 Usage

### Basic Commands

#### Generate tests for a specific function:
```bash
python pytest.py generate path/to/your/file.py function_name
```

#### Generate tests for all functions in a file:
```bash
python pytest.py generate-all path/to/your/file.py
```

#### List all functions in a file:
```bash
python pytest.py list path/to/your/file.py
```

#### Get detailed function information:
```bash
python pytest.py info path/to/your/file.py function_name
```

### Advanced Options

#### Custom output file:
```bash
python pytest.py generate path/to/file.py function_name -o custom_test_file.py
```

#### Custom output directory:
```bash
python pytest.py generate-all path/to/file.py -d /path/to/output/dir
```

#### Verbose output:
```bash
python pytest.py generate path/to/file.py function_name -v
```

#### Check configuration:
```bash
python pytest.py config
```

#### Interactive setup:
```bash
python pytest.py setup
```

## 📝 Example Usage

Let's say you have a file `math_utils.py`:

```python
def calculate_area(length: float, width: float) -> float:
    """Calculate the area of a rectangle."""
    if length < 0 or width < 0:
        raise ValueError("Length and width must be positive")
    return length * width

def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### Generate tests for a single function:
```bash
python pytest.py generate math_utils.py calculate_area
```

This will create a test file `generated_tests/test_math_utils_calculate_area.py` with comprehensive test cases.

### Generate tests for all functions:
```bash
python pytest.py generate-all math_utils.py
```

This will create separate test files for each function.

### List available functions:
```bash
python pytest.py list math_utils.py
```

Output:
```
ℹ️  Functions found in math_utils.py:
   1. calculate_area
   2. fibonacci
ℹ️  Total: 2 functions
```

### Get function details:
```bash
python pytest.py info math_utils.py calculate_area
```

## 📁 Project Structure

```
pytest-generator/
├── pytest.py              # Main CLI interface
├── test_generator.py       # Core test generation logic
├── gemini_client.py       # Gemini LLM integration
├── utils.py               # Function analysis utilities
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
└── examples/             # Example files for testing
    ├── math_utils.py     # Sample math functions
    ├── string_utils.py   # Sample string functions
    └── data_structures.py # Sample data structure functions
```

## 🎯 Generated Test Features

The generated tests include:

- **Normal/Happy Path Tests**: Basic functionality testing
- **Edge Cases**: Boundary conditions and special values
- **Error Handling**: Exception testing and error conditions
- **Parametrized Tests**: Multiple test scenarios in compact form
- **Proper Assertions**: Comprehensive pytest assertions
- **Mock Integration**: Automatic mocking for external dependencies
- **Clear Documentation**: Descriptive test names and docstrings

## 🔧 Customization

### Environment Variables

- `GEMINI_API_KEY`: Your Gemini API key (required)
- `GEMINI_MODEL`: Model to use (default: gemini-pro)
- `MAX_TEST_CASES`: Maximum tests per function (default: 10)
- `INCLUDE_EDGE_CASES`: Include edge case tests (default: true)
- `INCLUDE_ERROR_CASES`: Include error handling tests (default: true)
- `OUTPUT_DIR`: Directory for generated tests (default: generated_tests)
- `VERBOSE`: Enable verbose output (default: false)

### Modifying Test Generation

You can customize the test generation by modifying the prompts in `gemini_client.py` or adjusting the analysis logic in `utils.py`.

## 🐛 Troubleshooting

### Common Issues

1. **"GEMINI_API_KEY not found"**
   - Make sure you have a `.env` file with your API key
   - Run `python pytest.py setup` for interactive configuration

2. **"Function not found"**
   - Use `python pytest.py list file.py` to see available functions
   - Check function name spelling and case sensitivity

3. **"Syntax errors in generated code"**
   - The tool attempts to fix syntax errors automatically
   - Check your Gemini API key and model configuration

4. **Import errors**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check that your Python environment is properly configured

### Getting Help

- Use the `--verbose` flag for detailed output
- Run `python pytest.py config` to check your configuration
- Check the generated test files for any issues

## 🤝 Contributing

This project is open for improvements! Areas for enhancement:

- Support for more LLM providers
- Additional test frameworks (unittest, nose2)
- GUI interface
- Integration with IDEs
- More sophisticated code analysis

## 📄 License

This project is provided as-is for educational and development purposes.

## 🔗 Related Tools

- [pytest](https://pytest.org/) - Python testing framework
- [Google Gemini](https://ai.google.dev/) - Google's LLM API
- [Click](https://click.palletsprojects.com/) - Command line interface creation

---

**Happy Testing! 🧪✨**