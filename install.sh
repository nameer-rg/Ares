# Note this script is experimental and was made entirely by using github copilot
# There is a pretty big possibility that this script will not work at all since it's not been tested
# Feel free to use it if you want, or don't I don't really care.


# Tell the user that this script is experimental and is not guaranteed to work properly.
# Then prompt the user to confirm that they wish to continue using y/n.
# if y continue else exit the script
echo "This script is experimental and is not guaranteed to work properly."
echo "Do you wish to continue? [y/n]"
read answer
if [ "$answer" == "y" ]; then
    echo "Continuing..."
else
    echo "Exiting..."
    exit 1
fi

# Check if script is run as sudo
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as sudo"
    echo "You can do this by running sudo ./install.sh"
    exit 1
fi


# Attempt to install the requirements found in requirements.txt
# If python is not installed, install it
# If pip is not installed, install it


# Check if python is installed
if [ ! -e /usr/bin/python ]; then
    echo "Python is not installed"
    echo "Installing python"
    apt-get install python3
    echo "Python installed"
fi

# Check if pip is installed
if [ ! -e /usr/bin/pip ]; then
    echo "Pip is not installed"
    echo "Installing pip"
    apt-get install python-pip3
    echo "Pip installed"
fi

# Attempt to install requirements
echo "Installing requirements"
pip install -r requirements.txt
echo "Requirements installed"

