#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
RESET_PRINT='\033[0;0m'

installed_packages="0"
required_packages="0"
venv_name="venv_sapsam"

#checks for python3
required_packages=$((required_packages + 1))
if command -v python3 &>/dev/null; then
    echo -e "\xE2\x9C\x94 python3 installed..."
    installed_packages=$((installed_packages + 1))
else
    echo "python3 not installed"
    echo "exiting shell script..."
    exit 1
fi

#checks for venv
required_packages=$((required_packages + 1))
if python3 -m venv --help &>/dev/null; then
    echo -e "\xE2\x9C\x94 venv installed..."
    installed_packages=$((installed_packages + 1))
else
    echo "venv module not installed"
    echo "exiting shell script..."
    exit 1
fi

#checks for jupyter
required_packages=$((required_packages + 1))
if pip list | grep jupyter &>/dev/null; then
    echo -e "\xE2\x9C\x94 jupyter installed..."
    installed_packages=$((installed_packages + 1))
else
    echo "jupyer module not installed"
    echo "exiting shell script..."
    exit 1
fi

#checks for ipykernel
required_packages=$((required_packages + 1))
if pip list | grep ipykernel &>/dev/null; then
    echo -e "\xE2\x9C\x94 ipykernel installed..."
    installed_packages=$((installed_packages + 1))
else
    echo "ipykernel module not installed"
    echo "exiting shell script..."
    exit 1
fi

#checks for notebook
required_packages=$((required_packages + 1))
if pip list | grep notebook &>/dev/null; then
    echo -e "\xE2\x9C\x94 notebook installed..."
    installed_packages=$((installed_packages + 1))
else
    echo "notebook module not installed"
    echo "exiting shell script..."
    exit 1
fi

#pip install ipekernel
#python3 -m ipykernel install --user --name=sapsam_kernel

echo -e "${GREEN}$installed_packages out of $required_packages pre-required packages installed${RESET_PRINT}"

#creates the env
if [ -d "$venv_name" ]; then
    echo "virtual environment '$venv_name' already exists"
else
    python3.8 -m venv "$venv_name"
    echo "virtual environment '$venv_name' created"
fi

#activates the env
source "$venv_name/bin/activate"

#checks for packages
while IFS= read -r line || [ -n "$line" ]; do
    package=$(echo "$line" | awk -F '==' '{print $1}')
    version=$(echo "$line" | awk -F '==' '{print $2}')
    #echo "Package: $package, Version: $version"
    if pip show "$package" &>/dev/null; then #checks the exit code, not the output
        echo -e "\xE2\x9C\x94 $package installed..."
    else 
        echo -e "${RED}\xE2\x9C\x96${RESET_PRINT} $package not installed"
    fi
done < requirements.txt

read -p "Do you want to proceed and install packages? (Y/N): " answer

if [[ $answer == "Y" ]]; then
    while IFS= read -r line || [ -n "$line" ]; do
        package=$(echo "$line" | awk -F '==' '{print $1}')
        version=$(echo "$line" | awk -F '==' '{print $2}')
        #echo "Package: $package, Version: $version"
        if pip show "$package" &>/dev/null; then #checks the exit code, not the output
            echo -e "\xE2\x9C\x94 $package installed..."
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
    echo "Exiting script..."
fi

echo "updating pydantic..."
pip install -U pydantic==1.10.8 &>/dev/null

echo "setting kernel..."
python3 -m ipykernel install --user --name=sapsam_kernel
echo -e "${GREEN}\xE2\x9C\x94${RESET_PRINT} setup done"

#CURRENT_DIR=$(pwd)
#if [[ ":$PATH:" != *":$CURRENT_DIR:"* ]]; then
#    export PATH="$PATH:$CURRENT_DIR"
#    echo -e "${GREEN}\xE2\x9C\x94${RESET_PRINT}current directory added to path"
#else
#    echo "current directory already in path"
#fi