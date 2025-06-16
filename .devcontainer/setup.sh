#!/bin/bash

# PyCorewar Development Environment Setup Script
echo "Setting up PyCorewar development environment..."

# Update system packages
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install essential build tools for Python C extensions
echo "Installing build tools and development packages..."
sudo apt-get install -y \
    build-essential \
    gcc \
    g++ \
    make \
    libc6-dev \
    python3-dev \
    python3-pip \
    python3-venv \
    git \
    vim \
    curl \
    wget

# Upgrade pip and install Python development tools
echo "Setting up Python development tools..."
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade \
    setuptools \
    wheel \
    build \
    pytest \
    pytest-cov \
    flake8 \
    black \
    pylint \
    mypy

# Try to build the project to ensure everything is working
echo "Attempting to build PyCorewar..."
if [ -f "setup.py" ]; then
    echo "Building PyCorewar C extensions..."
    python3 setup.py build_ext --inplace
    
    if [ $? -eq 0 ]; then
        echo "✅ PyCorewar built successfully!"
    else
        echo "❌ Build failed. Check the error messages above."
    fi
else
    echo "⚠️  setup.py not found. Please run this script from the PyCorewar root directory."
fi

# Set up git configuration if not already set
if [ -z "$(git config --global user.name)" ]; then
    echo "Setting up git configuration..."
    echo "Please enter your name for git commits:"
    read -r git_name
    git config --global user.name "$git_name"
    
    echo "Please enter your email for git commits:"
    read -r git_email
    git config --global user.email "$git_email"
fi

# Install and build pMARS with 2x scaling for high-res displays
echo "Installing and building pMARS..."
if [ ! -d "pMARS" ]; then
    echo "Downloading pMARS..."
    wget -q http://www.koth.org/pmars/pmars-0.9.4.zip
    unzip -q pmars-0.9.4.zip
    mv pmars-0.9.4 pMARS
    
    # Apply 2x scaling patch for better visibility on high-resolution monitors
    echo "Applying 2x scaling patch to pMARS X Window display..."
    if [ -f "xwindisp_2x_scaling.patch" ]; then
        cd pMARS/src
        patch -p3 < ../../xwindisp_2x_scaling.patch
        if [ $? -eq 0 ]; then
            echo "✅ X Window scaling patch applied successfully!"
        else
            echo "❌ Failed to apply scaling patch. Building with original display size."
        fi
        cd ../..
    else
        echo "⚠️  Scaling patch file not found. Building with original display size."
    fi
fi

# Build pMARS
echo "Building pMARS..."
cd pMARS/src
make clean
make
if [ $? -eq 0 ]; then
    echo "✅ pMARS built successfully with 2x scaled display!"
else
    echo "❌ pMARS build failed. Check the error messages above."
fi
cd ../..
