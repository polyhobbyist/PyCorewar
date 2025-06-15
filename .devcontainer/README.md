# PyCorewar Dev Container

This directory contains the development container configuration for PyCorewar, making it easy to get started with development in a consistent environment.

## Features

- **Microsoft Universal Dev Container**: Based on the Microsoft universal dev container image
- **Python 3.11**: Pre-configured with Python development tools
- **C/C++ Support**: Build tools for compiling PyCorewar's C extensions
- **VS Code Integration**: Pre-configured extensions and settings
- **Git Integration**: Ready-to-use git configuration

## Quick Start

1. **Prerequisites**: Make sure you have VS Code with the Dev Containers extension installed
2. **Open in Container**: Open the PyCorewar project in VS Code and use "Reopen in Container"
3. **Build the Project**: The container will automatically set up the environment and you can build PyCorewar

## What's Included

### System Packages
- Build essentials (gcc, g++, make)
- Python development headers
- Git and common utilities

### Python Tools
- pytest for testing
- black for code formatting
- flake8 for linting
- pylint for code analysis
- mypy for type checking

### VS Code Extensions
- Python extension pack
- C/C++ tools
- GitHub Copilot (if available)

## Files

- `devcontainer.json`: Main dev container configuration
- `docker-compose.yml`: Alternative Docker Compose setup
- `setup.sh`: Environment setup script
- `requirements-dev.txt`: Development Python dependencies
- `README.md`: This file

## Building PyCorewar

Once the container is running, you can build PyCorewar:

```bash
# Build C extensions in place
python setup.py build_ext --inplace

# Or use the modern build system
python -m build
```

## Testing

Run the test suite:

```bash
# Run specific test modules
python Test/Core.py
python Test/MARS88.py

# Or use pytest if configured
pytest Test/
```

## Customization

You can customize the dev container by modifying `devcontainer.json`:

- Add more VS Code extensions
- Install additional system packages
- Configure different Python versions
- Add environment variables

## Troubleshooting

### Build Issues
If you encounter build issues, ensure all build dependencies are installed:
```bash
sudo apt-get update
sudo apt-get install build-essential python3-dev
```

### Python Path Issues
The container sets `PYTHONPATH` to include both the project root and `src/` directory. If you have import issues, verify this is set correctly.

### Permission Issues
The container runs as the `codespace` user. If you need root access, use `sudo`.
