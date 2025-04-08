### Example Usage

Once the service is running, you can use the example client to test it:

```bash
# Run with default settings (streaming)
poetry run python examples/client.py --stream

# Run with custom prompt
poetry run python examples/client.py --stream --prompt "Explain quantum computing in simple terms"

# Run with non-streaming mode
poetry run python examples/client.py --prompt "Write a sorting algorithm in Python"
``````markdown
# LLM Service

A gRPC service that provides a standardized interface to language models running on Ollama.

## Project Structure
llm-service/
├── llm_service/               # Main package
│   ├── __init__.py            # Package initialization
│   ├── main.py                # Entry point
│   ├── service.py             # gRPC service implementation
│   ├── config.py              # Configuration handling
│   └── utils/                 # Utility modules
│       ├── __init__.py        # Package initialization
│       ├── logging.py         # Logging utilities
│       └── ollama.py          # Ollama API client
│
├── proto/                     # Protocol Buffer definitions
│   └── llm.proto              # LLM service definition
│
├── tests/                     # Tests
│   ├── __init__.py            # Test package initialization
│   ├── test_service.py        # Service tests
│   └── test_ollama.py         # Ollama client tests
│
├── examples/                  # Example code
│   └── client.py              # Example client
│
├── scripts/                   # Utility scripts
│   └── generate_proto.py      # Script to generate Python code from proto
│
├── pyproject.toml             # Poetry configuration (dependencies, etc.)
├── Dockerfile                 # Container definition
└── README.md                  # Documentation
```

## Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Ollama](https://ollama.ai/download) (running locally or accessible via network)

## Setup and Installation

### 1. Install Poetry

If you don't have Poetry installed:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. Clone and Install

```bash
# Clone the repository
git clone https://github.com/yourusername/llm-service.git
cd llm-service

# Install dependencies
poetry install

# Generate Protocol Buffer code
poetry run python scripts/generate_proto.py
```

## Running the Service

### Local Development

```bash
# Run with default configuration
poetry run llm-service

# Or with custom configuration
MODEL_NAME=llama2 OLLAMA_URL=http://localhost:11434 poetry run llm-service
```

### Configuration Options

Set these environment variables to configure the service:

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | gRPC server port | `50051` |
| `WORKER_THREADS` | Number of worker threads | `10` |
| `OLLAMA_URL` | Ollama API endpoint | `http://localhost:11434` |
| `MODEL_NAME` | Model to use | `model-name` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage report
poetry run pytest --cov=llm_service tests/

# Run specific test file
poetry run pytest tests/test_service.py
```

## Using Docker

### Build

```bash
docker build -t llm-service:latest .
```

### Run

```bash
docker run -p 50051:50051 \
  -e MODEL_NAME="llama2" \
  -e OLLAMA_URL="http://host.docker.internal:11434" \
  llm-service:latest
```

## Development Commands

| Command | Description |
|---------|-------------|
| `poetry add package-name` | Add a dependency |
| `poetry add --dev package-name` | Add a dev dependency |
| `poetry update` | Update dependencies |
| `poetry shell` | Activate the virtual environment |
| `poetry build` | Build the package |

## Example Client Code

Here's a simple Python client to test the service:

```python
import grpc
from proto import llm_pb2, llm_pb2_grpc

# Connect to the service
channel = grpc.insecure_channel('localhost:50051')
stub = llm_pb2_grpc.LLMServiceStub(channel)

# Create a request
request = llm_pb2.LLMRequest(
    prompt="Write a function to calculate fibonacci numbers",
    parameters=llm_pb2.LLMRequest.Parameters(
        temperature=0.7,
        max_tokens=1000,
        top_p=0.95
    )
)

# For streaming responses
try:
    for response in stub.GenerateStream(request):
        print(response.text, end="", flush=True)
        if response.is_complete:
            print("\nGeneration complete!")
except grpc.RpcError as e:
    print(f"RPC error: {e.code()}: {e.details()}")
```

## License

[Your license here]
```