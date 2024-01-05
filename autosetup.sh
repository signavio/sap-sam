#!/bin/bash

# global variables
GREEN='\033[0;32m'
RED='\033[0;31m'
RESET_PRINT='\033[0;0m'

installed_packages="0"
required_packages="0"
venv_name="venv_sapsam"
kernel_name="sapsam_kernel"

# checks for pip
required_packages=$((required_packages + 1))
if pip --version &>/dev/null; then
    echo -e "\xE2\x9C\x94 pip installed..."
    installed_packages=$((installed_packages + 1))
else
    echo "pip not installed"
    echo "try installing pip with for example (on macOS): brew install pip"
    echo "exiting setup script..."
    exit 1
fi

# checks for python
required_packages=$((required_packages + 1))
if command -v python &>/dev/null; then
    echo -e "\xE2\x9C\x94 python installed..."
    installed_packages=$((installed_packages + 1))
elif command -v python3 &>/dev/null; then
    echo -e "\xE2\x9C\x94 python3 installed..."
    installed_packages=$((installed_packages + 1))
else
    echo "python not installed"
    echo "try installing python3 with for example (on macOS): brew install python3"
    echo "exiting setup script..."
    exit 1
fi

# checks for venv
required_packages=$((required_packages + 1))
if python3 -m venv --help &>/dev/null; then
    echo -e "\xE2\x9C\x94 venv installed..."
    installed_packages=$((installed_packages + 1))
else
    echo "venv module not installed"
    echo "exiting setup script..."
    exit 1
fi

# checks for jupyter
required_packages=$((required_packages + 1))
if pip list | grep jupyter &>/dev/null; then
    echo -e "\xE2\x9C\x94 jupyter installed..."
    installed_packages=$((installed_packages + 1))
else
    echo "jupyter module not installed"
    echo "try installing jupyter with for example: pip install jupyter notebook"
    echo "exiting setup script..."
    exit 1
fi

# checks for notebook
required_packages=$((required_packages + 1))
if pip list | grep notebook &>/dev/null; then
    echo -e "\xE2\x9C\x94 notebook installed..."
    installed_packages=$((installed_packages + 1))
else
    echo "notebook module not installed"
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

# activates the virtual environment for packages installation
source "$venv_name/bin/activate"
echo "updating pip..."
pip install --upgrade pip

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
                    echo -e "exiting..."
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
                echo -e "exiting..."
                exit 1
            fi
        fi
    done < requirements.txt
else
    echo "exiting setup script..."
    exit 1
fi

# manual update necessary for pydantic 1.10.8
echo "updating pydantic..."
pip install -U pydantic==1.10.8 &>/dev/null
echo -e "${GREEN}\xE2\x9C\x94${RESET_PRINT} pydantic update done"

# kernel setup
echo "setting kernel..."
python3 -m ipykernel install --user --name=$kernel_name
echo -e "${GREEN}\xE2\x9C\x94${RESET_PRINT} kernel set"

# end message
echo -e "${GREEN}\xE2\x9C\x94${RESET_PRINT} setup done"