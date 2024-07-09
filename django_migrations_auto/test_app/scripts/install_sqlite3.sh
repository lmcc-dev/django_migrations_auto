#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print success messages
print_success() {
    echo -e "${GREEN}$1${NC}"
}

# Function to print error messages
print_error() {
    echo -e "${RED}$1${NC}"
}

# Function to compare versions
version_lt() {
    [ "$1" = "$(echo -e "$1\n$2" | sort -V | head -n1)" ]
}

# Function to check if a command is available
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Store the current directory
current_dir=$(pwd)

# Check if Python3 is available and its version is 3.10.x or higher
python_version=$(python3 -V 2>&1 | awk '{print $2}')
required_version="3.10.0"
if version_lt "$python_version" "$required_version"; then
    print_error "Error: Python 3.10.0 or higher is required, but the detected version is $python_version"
    exit 1
fi

# Create a temporary directory for compilation and downloads
tmp_dir=$(mktemp -d)

# Function to clean up temporary files and directories
cleanup() {
    cd "$current_dir" || exit 1
    /bin/rm -rf "$tmp_dir"
}

trap cleanup EXIT

# Change to the temporary directory
pushd "$tmp_dir" >/dev/null || exit 1

# Function to check if sqlite3 or pysqlite3 is installed and its version
check_sqlite3_installed() {
    pysqlite_version=$(python3 -c "from $1 import dbapi2 as Database; print(Database.sqlite_version)" 2>/dev/null)
    echo "$pysqlite_version"
}

# Function to compile and install SQLite from source
compile_and_install_sqlite() {
    print_success "Compiling and installing SQLite from source..."

    # Check if required commands are available
    required_commands=("curl" "make" "gcc" "unzip" "tar")
    for cmd in "${required_commands[@]}"; do
        if ! command_exists "$cmd"; then
            print_error "Error: $cmd command is not installed. Attempting to install..."
            if [ -x "$(command -v apt-get)" ]; then
                sudo apt-get install -y $cmd
            elif [ -x "$(command -v yum)" ]; then
                sudo yum install -y $cmd
            else
                print_error "Package manager not found. Please install $cmd manually."
                exit 1
            fi
        fi
    done

    # Download SQLite source code
    curl -L "https://www.sqlite.org/src/tarball/sqlite.tar.gz?r=release" --output sqlite.tar.gz --insecure
    tar xzf sqlite.tar.gz
    sqlite_dir=$(tar -tf sqlite.tar.gz | head -1 | cut -f1 -d"/")
    cd "$sqlite_dir" || exit 1

    # Configure and compile SQLite
    ./configure || exit 1
    make sqlite3.c || exit 1
    sudo make install || exit 1

    # Return to the temporary directory
    cd "$tmp_dir" || exit 1
}

# Function to compile and install pysqlite3 from source
compile_and_install_pysqlite3() {
    print_success "Compiling and installing pysqlite3 from source..."

    # Download pysqlite3 source code
    curl -L "https://github.com/coleifer/pysqlite3/archive/refs/heads/master.zip" --output pysqlite3.zip --insecure
    if ! unzip pysqlite3.zip; then
        print_error "Error: Failed to download and unzip pysqlite3 source code."
        exit 1
    fi
    cd pysqlite3-master || exit 1

    # Set environment variables to ensure proper linking
    export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"
    export CPPFLAGS="-I/usr/local/include"
    export LDFLAGS="-L/usr/local/lib"

    # Copy SQLite source files to pysqlite3 directory
    cp ../"$sqlite_dir"/sqlite3.[ch] .  || exit 1

    # Build and install pysqlite3
    python3 -m pip install setuptools || exit 1
    python3 setup.py build_static build || exit 1
    python3 setup.py install || exit 1

    # Return to the temporary directory
    cd "$tmp_dir" || exit 1
}

# Check if sqlite3 and pysqlite3 are installed and their versions
sqlite3_version=$(check_sqlite3_installed "sqlite3")
pysqlite3_version=$(check_sqlite3_installed "pysqlite3")

# Only compile and install if both sqlite3 and pysqlite3 do not meet the version requirements
if { [ -z "$sqlite3_version" ] || version_lt "$sqlite3_version" "3.8.3"; } && { [ -z "$pysqlite3_version" ] || version_lt "$pysqlite3_version" "3.8.3"; }; then
    print_error "Both sqlite3 and pysqlite3 do not meet version requirements. Compiling and installing both from source..."
    compile_and_install_sqlite
    compile_and_install_pysqlite3
else
    print_success "Either sqlite3 or pysqlite3 meets the version requirements."
fi

# Return to the current directory
popd >/dev/null || exit 1

# Exit the script
exit 0