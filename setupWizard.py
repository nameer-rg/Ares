# Imort all libraries used by setupWizard.py
import json
import os
import re
import sys

# We won't use logging libraries in this bit of the project because we don't have the configuration made probably


# Cross platfrom terminal colors (global variables)
red = "\033[31m"
green = "\033[32m"
purple = "\033[35m"
cyan = "\033[36m"
reset = "\033[0m"

# Cross platform terminal clearing
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

cls()

def checkConfig():
    cls()
    # If no config file exists, create one
    # If a config file exists but is empty, overwrite it
    # If a config file exists but is not empty, ask if user wants to overwrite it
    # If the users wishes to overwrite create a backup of the current config file
    # Data to write to data/config.json
    # token
    # prefix
    # autoupdate

    # check if there is no config file
    if not os.path.exists("data/config.json"):
        with open("data/config.json", "w") as f:
            data = {
                "token": "",
                "prefix": "",
                "autoupdate": True
            }
            json.dump(data, f)
            print(purple + "Created config file" + reset)
            return

    # check if there is a config file but it is empty
    if os.path.getsize("data/config.json") == 0:
        with open("data/config.json", "w") as f:
            data = {
                "token": "",
                "prefix": "",
                "autoupdate": True
            }
            json.dump(data, f)
            print(purple + "Overwrited empty config file" + reset)
            return

    # check if there is a config file but it is not empty
    # If it's broken, ask if user wants to overwrite it
    # If yes ask if the user wants to create a backup of the current config file
    # If yes create a backup of the current config file
    # If no don't overwrite the config file
    if os.path.getsize("data/config.json") != 0:
        with open("data/config.json", "r") as f:
            data = json.load(f)
            if data["token"] == "":
                print(red + "Config file is empty" + reset)
                if input(cyan + "Do you want to overwrite the config file? (y/n) " + reset) == "y":
                    with open("data/config.json", "w") as f:
                        data = {
                            "token": "",
                            "prefix": "",
                            "autoupdate": True
                        }
                        json.dump(data, f)
                        print(green + "Overwrote empty config file" + reset)
                        return
                else:
                    print(red + "Config file is not empty" + reset)
                    if input(cyan + "Do you want to create a backup of the current config file? (y/n) " + reset) == "y":
                        with open("data/config.json", "r") as f:
                            data = json.load(f)
                            with open("data/config.json.bak", "w") as f:
                                json.dump(data, f)
                                print(green + "Created backup of config file" + reset)
                                return

# Setup wizard for first time use
def run_wizard():
    """Wizard for first time start"""
    cls()

    # run checkConfig() to make sure config file exists and setup wizard won't overrwrite it
    checkConfig()
    cls()
    print(green + "Welcome to the selfbot setup wizard!" + reset)
    print( "I will ask you a series of questions to configure the bot.")
    print("Please respond with the letter that matches what you want")
    print(cyan + "Press enter to continue" + reset)
    input()
    print( "First, I need to know your discord token")
    print("Please enter your token (Tutorial | https://www.youtube.com/watch?v=LnBnm_tZlyU) " + reset)
    token = input(cyan + "Token: ")

    # Remove " from each side of the token if its given with quotation marks
    if token.startswith('"') and token.endswith('"'):
        token = token[1:-1]
        print(green + "Removed quotation marks automatically" + reset)

    cls()
    print("Next, I need to know your prefix")
    print("Please enter a prefix (Default: $) " + reset)
    prefix = input(cyan + "Prefix: " + reset)
    if prefix == "":
        prefix = "$"

    cls()
    # Automatic updater, ask the user y/n if y is entered, set autoupdate to true, else false
    # Default = True
    print("Next, I need to know whether or not you'd like to update the selfbot automatically")
    print("Please enter 'y' or 'n' (Default y) ")
    autoupdate = input(cyan + "Autoupdate: " + reset)
    if autoupdate == "y":
        autoupdate = True
    elif autoupdate == "":
        autoupdate = True
    else:
        autoupdate = False


    # Dump the data to data/config.json
    try:
        with open("data/config.json", "w") as f:
            data = {
                "token": token,
                "prefix": prefix,
                "autoupdate": autoupdate
            }
            json.dump(data, f)
            print(green + "Successfully created a new config file" + reset)
    except Exception as e:
        print(red + "Error: " + str(e) + reset)
        print(red + "Failed to create new config file" + reset)
        print(red + "Please make sure you have write permissions" + reset)
        print(red + "Then run setup wizard again" + reset)

    # Create logging configuration file
    # Accepted values are: debug, info, warning, error, critical
    # If data/logger.json already exists overwrite it
    print(cyan + "Now I will create a logging configuration file" + reset)
    print(cyan + "Please enter the level of logging you'd like to receive" + reset)
    print(cyan + "Valid logging values are: debug, info, warning, error, critical" + reset)
    print(cyan + "Press enter to keep the default value (error)" + reset)
    logging = input(cyan + "Logging: " + reset)
    if logging == "":
        logging = "error"
    try:
        with open("data/logger.json", "w") as f:
            data = {
                "logging": logging
            }
            json.dump(data, f)
            print(green + "Successfully created a new logging configuration file" + reset)
    except Exception as e:
        print(red + "Error: " + str(e) + reset)
        print(red + "Failed to create new logging configuration file" + reset)
        print(red + "Please make sure you have write permissions" + reset)
        print(red + "Then run setup wizard again" + reset)
    
    cls()
    # Ask the user to press any button to exit the setupWizard
    input(purple + "Press any button to exit the setup wizard" + reset)
    # Safely exit
    sys.exit()


# When this file is run run the wizard
if __name__ == "__main__":
    run_wizard()
