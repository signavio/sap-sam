#!/bin/bash

# global variables
GREEN='\033[0;32m'
RED='\033[0;31m'
RESET_PRINT='\033[0;0m'

installed_packages="0"
required_packages="0"
venv_name="venv_sapsam"
kernel_name="sapsam_kernel"

min_pip_version="23.3.2"
min_python3_version="3.11.7"
min_notebook_version="7.0.6"

# checks for pip and updates if necessary
required_packages=$((required_packages + 1))
echo "starting setup..."
if pip3 --version &>/dev/null || pip --version &>/dev/null; then
    echo "      checking for pip minimum version requirement..."
    pip_version=$(pip3 --version | awk '{print $2}')
    if [[ "$(printf '%s\n' "$min_pip_version" "$pip_version" | sort -V | head -n1)" == "$min_pip_version" ]]; then
        echo -e "${GREEN}\xE2\x9C\x94${RESET_PRINT} pip installed..."
    else
        echo "updating pip..."
        pip3 install --upgrade pip
        echo -e "${GREEN}\xE2\x9C\x94${RESET_PRINT} pip installed..."
    fi
    installed_packages=$((installed_packages + 1))
else
    echo -e "${RED}\xE2\x9C\x96${RESET_PRINT} pip not installed"
    echo "try installing pip with for example (on macOS): brew install pip"
    echo "exiting setup script..."
    exit 1
fi

# checks for python and version
required_packages=$((required_packages + 1))
if command -v python &>/dev/null || command -v python3 &>/dev/null; then
    echo "      checking for python3 minimum version requirement..."
    python3_version=$(python3 --version | awk '{print $2}')
    if [[ "$(printf '%s\n' "$min_python3_version" "$python3_version" | sort -V | head -n1)" == "$min_python3_version" ]]; then
        echo -e "${GREEN}\xE2\x9C\x94${RESET_PRINT} python3 installed..."
    else
        echo -e "${RED}\xE2\x9C\x96${RESET_PRINT} python3 is outdated ($python3_version)"
        echo "required stable version: $min_python3_version"
        echo "try upgrading python3 with for example (on macOS): brew upgrade python3"
        echo "exiting setup script..."
        exit 1
    fi
    installed_packages=$((installed_packages + 1))
else
    echo -e "${RED}\xE2\x9C\x96${RESET_PRINT} python not installed"
    echo "try installing python3 with for example (on macOS): brew install python3"
    echo "exiting setup script..."
    exit 1
fi

# checks for venv
required_packages=$((required_packages + 1))
if python3 -m venv --help &>/dev/null; then
    echo -e "${GREEN}\xE2\x9C\x94${RESET_PRINT} venv installed..."
    installed_packages=$((installed_packages + 1))
else
    echo "${RED}\xE2\x9C\x96${RESET_PRINT} venv not installed"
    echo "exiting setup script..."
    exit 1
fi

# checks for jupyter
required_packages=$((required_packages + 1))
if pip list | grep jupyter &>/dev/null; then
    echo -e "${GREEN}\xE2\x9C\x94${RESET_PRINT} jupyter installed..."
    installed_packages=$((installed_packages + 1))
else
    echo -e "${RED}\xE2\x9C\x96${RESET_PRINT} jupyter not installed"
    echo "try installing jupyter with for example: pip install jupyter notebook"
    echo "exiting setup script..."
    exit 1
fi

# checks for notebook and updates if necessary
required_packages=$((required_packages + 1))
if pip list | grep notebook &>/dev/null; then
    echo "      checking for notebook minimum version requirement..."
    notebook_version=$(jupyter --version 2>/dev/null | grep notebook | awk '{print $NF}')
    if [[ "$(printf '%s\n' "$min_notebook_version" "$notebook_version" | sort -V | head -n1)" == "$min_notebook_version" ]]; then
        echo -e "${GREEN}\xE2\x9C\x94${RESET_PRINT} notebook installed..."
    else
        echo "updating notebook..."
        pip install --upgrade notebook
        echo -e "${GREEN}\xE2\x9C\x94${RESET_PRINT} notebook installed..."
    fi
    installed_packages=$((installed_packages + 1))
else
    echo -e "${RED}\xE2\x9C\x96${RESET_PRINT} notebook not installed"
    echo "exiting setup script..."
    exit 1
fi

echo -e "${GREEN}$installed_packages out of $required_packages pre-required packages installed${RESET_PRINT}"

# creates the virtual environment
if [ -d "$venv_name" ]; then
    echo "virtual environment '$venv_name' already exists"
else
    python3 -m venv "$venv_name"
    echo "virtual environment '$venv_name' created"
fi

# activates the virtual environment for packages installation, depending on OS
if [ "$(uname)" == "Darwin" ]; then
    source "$venv_name/bin/activate" &>/dev/null
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    source "$venv_name/bin/activate" &>/dev/null
else
    source "$venv_name/Scripts/activate" &>/dev/null
fi

if [ $? -ne 0 ]; then
	echo "unable to activate virtual environment"
	echo "Debian/Ubuntu users might need to install the python3-venv package separately."
	echo "exiting setup script..."
    exit 1
else
	echo -e "${GREEN}\xE2\x9C\x94${RESET_PRINT} environment successfully activated"
fi

# checks for all requirements
while IFS= read -r line || [ -n "$line" ]; do
    package=$(echo "$line" | awk -F '==' '{print $1}')
    version=$(echo "$line" | awk -F '==' '{print $2}')
    if pip show "$package" &>/dev/null; then # checks the exit code, not the output
        installed_version=$(pip show "$package" | awk '/^Version: / {print $2}')
        if [[ "$installed_version" == "$version" ]]; then
             echo -e "${GREEN}\xE2\x9C\x94${RESET_PRINT} $package $version installed..."
        else
            echo -e "${RED}\xE2\x9C\x96${RESET_PRINT} $package installed but wrong version..."
        fi
    else 
        echo -e "${RED}\xE2\x9C\x96${RESET_PRINT} $package not installed"
    fi
done < requirements.txt

read -p "Do you want to proceed with setup? (Y/N): " answer

if [[ $answer == "Y" || $answer == "y" ]]; then
    while IFS= read -r line || [ -n "$line" ]; do
        package=$(echo "$line" | awk -F '==' '{print $1}')
        version=$(echo "$line" | awk -F '==' '{print $2}')
        if pip show "$package" &>/dev/null; then
            installed_version=$(pip show "$package" | awk '/^Version: / {print $2}')
            if [[ "$installed_version" == "$version" ]]; then
                echo -e "${GREEN}\xE2\x9C\x94${RESET_PRINT} $package $version installed..."
            else
                echo "updating $package..."
                pip install -U "$package==$version"
                if pip show "$package" &>/dev/null; then
                    echo -e "${GREEN}\xE2\x9C\x94${RESET_PRINT} $package $version installed successfully"
                else
                    echo -e "${RED}\xE2\x9C\x96${RESET_PRINT} $package installation failed"
                    echo "exiting..."
                    exit 1
                fi
            fi
        else 
            echo -e "installing $package..."
            pip install "$package==$version"
            if pip show "$package" &>/dev/null; then
                echo -e "${GREEN}\xE2\x9C\x94${RESET_PRINT} $package installed successfully"
            else
                echo -e "${RED}\xE2\x9C\x96${RESET_PRINT} $package installation failed"
                echo "exiting..."
                exit 1
            fi
        fi
    done < requirements.txt
else
    echo "exiting setup script..."
    exit 1
fi

# kernel setup
echo "setting kernel..."
python3 -m ipykernel install --user --name=$kernel_name
echo -e "${GREEN}\xE2\x9C\x94${RESET_PRINT} kernel set"

# end message
echo -e "${GREEN}\xE2\x9C\x94${RESET_PRINT} setup done"