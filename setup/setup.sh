#!/bin/bash

RED="\033[01;31m"
GREEN="\033[01;32m"
YELLOW="\033[01;33m"
BOLD="\033[01;01m"
RESET="\033[00m"

#if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
#	# https://stackoverflow.com/a/2684300
#	echo -e "\n${RED}Must run setup script with:${RESET} source setup.sh"
#	echo "This ensures environment variables are set properly for python's virtualenvwrapper"
#	exit
#fi

if [ $EUID -ne 0 ]; then
   echo -e "\n${BOLD}${RED}Setup script must be run as root.${RESET}"
   exit
fi

apt-get update; echo

script_path=$(python3 -c "import os; print(os.path.abspath(os.path.dirname('$0')))")
cd "$script_path"

# Make sure pip is set up properly
# Set up virtualenvwrapper and autoenv
echo -e "${YELLOW}[*] Setting up python virtual environment...${RESET}"
apt-get install -y python3-venv virtualenv
wget -N https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
python3 -m pip install --upgrade setuptools wheel pip
python3 -m pip install --upgrade autoenv
if [ -z "$(cat ~/.bashrc | grep "source.*activate.sh")" ] && [ ! -z "$(which activate.sh)" ]; then
	echo "source `which activate.sh`" >> ~/.bashrc
fi
python3 -m venv iptodomain
mkdir .venv
mv iptodomain .venv
wget -P .venv/iptodomain/bin https://raw.githubusercontent.com/pypa/virtualenv/master/virtualenv_embedded/activate_this.py
chmod +x .venv/iptodomain/bin/activate_this.py
chmod +x .venv/iptodomain/bin/activate
source .venv/iptodomain/bin/activate
echo "source $script_path/.venv/iptodomain/bin/activate" >../.env
echo -e "${GREEN}[+] Done${RESET}";echo

# pip installs
echo -e "${YELLOW}[*] Setting up python dependencies...${RESET}"
python3 get-pip.py
rm -f get-pip.py
python3 -m pip install --upgrade setuptools wheel pip
python3 -m pip install --upgrade -r ../requirements.txt
echo -e "${GREEN}[+] Done${RESET}";echo

echo -e "${YELLOW}[*] Run the command below to finish setup:${RESET}"
echo -e "\tsource ~/.bashrc"
echo -e "\n${YELLOW}[*] The python virtual environment must be activated before running iptodomain.py${RESET}"
echo -e "${YELLOW}[*] The virtual environment is automatically activated when you change to the iptodomain directory.${RESET}"
echo -e "${YELLOW}[*] Or you can run the command below to activate the virtual environment:${RESET}"
echo -e "\tsource $script_path/.venv/iptodomain/bin/activate"
echo -e "${GREEN}[*]${RESET} (iptodomain) ${GREEN}will appear next to your command line when the virtual environment is active.${RESET}"
