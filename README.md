# 🧩 JSON-RPC Playground

A modern, interactive educational tool for learning JSON-RPC 2.0 protocol with comprehensive testing infrastructure.

**Developed by M Rehan ul Haq** - Making complex protocols simple to learn.

## 🎯 Purpose

This application provides a hands-on learning experience for beginners to understand:

- JSON-RPC 2.0 specification
- Request/Response patterns
- Notification handling
- Error scenarios and codes
- Real-world implementation patterns

## 🚀 Quick Start

### Option 1: Direct Installation (Recommended)

```bash
# Install the package
uv add jsonrpc-playground

# Run the playground
jsonrpc-playground
```

### Option 2: Development Setup

1. **Clone and setup:**

   ```bash
   git clone <repository-url>
   cd jsonrpc-playground
   uv sync
   ```

2. **Run the application:**

   ```bash
   # Using the package command
   uv run jsonrpc-playground

   # Or run directly
   python main.py
   ```

3. **Access the playground:**
   - Open your browser to `http://localhost:8501`
   - The JSON-RPC server runs on `http://localhost:4000`

## 🧪 Testing & Quality Assurance

This project includes comprehensive testing to ensure reliability and ease of contribution:

### Run Tests

```bash
# Run all tests
python scripts/run_tests.py

# Quick unit tests only
python scripts/run_tests.py --quick

# Integration tests only
python scripts/run_tests.py --integration

# Tests with coverage report
python scripts/run_tests.py --coverage

# Code quality checks only
python scripts/run_tests.py --quality

# Run everything (tests + quality)
python scripts/run_tests.py --all
```

### Test Coverage

- **Comprehensive test suite** covering all functionality
- **Unit tests**: Fast validation of individual components
- **Integration tests**: Full server communication testing
- **Error scenario testing**: All JSON-RPC error codes validated

For detailed testing information, see the comprehensive test suite in the `tests/` directory.

## 📚 Learning Modules

### 🔧 Methods Tab

- Learn how to call remote procedures
- See request/response structure
- Test with `add`, `greet`, and `get_log` methods
- Understand the role of the `id` field

### 📢 Notifications Tab

- Explore "fire-and-forget" messaging
- Understand notifications vs. requests
- Practice with the `log_message` method
- Learn when to use notifications

### 💥 Error Scenarios Tab

- Experience all standard JSON-RPC error codes
- See how malformed requests are handled
- Understand error response structure
- Learn debugging techniques

## 🛠 Available Methods

| Method                 | Parameters       | Description                                       |
| ---------------------- | ---------------- | ------------------------------------------------- |
| `add`                  | `a: int, b: int` | Adds two numbers                                  |
| `greet`                | `name: str`      | Returns a greeting message                        |
| `get_log`              | None             | Retrieves server log entries                      |
| `log_message`          | `message: str`   | Logs a message (notification)                     |
| `clear_log`            | None             | Clears the server log                             |
| `strict_add`           | `a: int, b: int` | Type-strict addition (for error demo)             |
| `cause_internal_error` | `trigger: str`   | Causes server error (-32000) when trigger="error" |

## 📖 JSON-RPC 2.0 Error Codes

| Code   | Name             | Description                         |
| ------ | ---------------- | ----------------------------------- |
| -32700 | Parse Error      | Invalid JSON was received           |
| -32600 | Invalid Request  | JSON-RPC request is not valid       |
| -32601 | Method Not Found | Method does not exist               |
| -32602 | Invalid Params   | Invalid method parameters           |
| -32603 | Internal Error   | Internal JSON-RPC error             |
| -32000 | Server Error     | Implementation-defined server error |

## 🎓 Learning Objectives

After using this playground, you should understand:

- ✅ JSON-RPC 2.0 protocol structure
- ✅ Difference between requests and notifications
- ✅ Error handling and debugging
- ✅ Real-world implementation patterns
- ✅ Best practices for API design

## 🤝 Contributing

This project welcomes contributions! Here's how to get started:

1. **Fork the repository**
2. **Install test dependencies**: `uv sync --group test --group dev`
3. **Make your changes**
4. **Run tests**: `python scripts/run_tests.py --all`
5. **Submit a pull request**

All contributions must:

- ✅ Pass all existing tests
- ✅ Include tests for new functionality
- ✅ Follow code quality standards (Black, isort, Flake8)
- ✅ Include documentation updates if needed

## 🔧 Technical Stack

- **Frontend:** Streamlit (Python web framework)
- **Backend:** HTTP server with `json-rpc` library
- **Protocol:** JSON-RPC 2.0 over HTTP
- **Testing:** pytest, coverage, quality checks
- **Package Management:** uv (fast Python package manager)
- **Code Quality:** Black, isort, Flake8, Pylint
- **Dependencies:** See `pyproject.toml`

## 📁 Project Structure

```
jsonrpc-playground/
├── src/
│   └── jsonrpc_playground/
│       ├── __init__.py          # Package initialization
│       ├── main.py              # Application launcher
│       ├── server.py            # JSON-RPC server implementation
│       └── client.py            # Streamlit web interface
├── tests/
│   ├── __init__.py
│   ├── test_main.py             # Main launcher tests
│   ├── test_server.py           # Server functionality tests
│   ├── test_client.py           # Client interface tests
│   └── test_rpc_server.py       # RPC server integration tests
├── scripts/
│   ├── run_tests.py             # Comprehensive test runner
│   ├── run_server.py            # Server startup script
│   └── run_client.py            # Client startup script
├── main.py                      # Entry point script
├── pyproject.toml               # Package configuration
├── pytest.ini                  # Test configuration
├── uv.lock                      # Dependency lock file
└── README.md                    # This file
```

## 📝 License

MIT License - Educational use encouraged! Feel free to modify and extend.
