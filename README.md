# Introduction

Jarvis is a Python program that uses AI language learning models to interpret the user's voice command and perform tasks such as opening websites, computer programs, and answering internet queries. The program is named after the AI character in the Iron Man movies.

This README file provides instructions for installing and running Jarvis, as well as information on obtaining the necessary API keys to use certain features of the program.

### DISCLAIMER
**This program will cost money to run, but very little. The OpenAI API costs fractions of cents—something like 0.2 CENTS per request—and a new OpenAI API account should have a free trial of $18 in credits. However, if you are using this program for a long time, you will need to pay for the API.**

## Installation

To install Jarvis, follow these steps:

1. Clone the repository to your local machine:

    ```git clone https://github.com/Paridax/jarvis.git```

2. Install the required packages using pip:

    ```pip install -r requirements.txt```

3. Create a file named `.env` in the root directory of the project and add the following line:

    ```OPENAI_API_KEY=<your_openai_api_key>```

Note: Replace `<your_openai_api_key>` with your actual OpenAI API key.


## Usage

To run Jarvis, navigate to the root directory of the project and run the following command:

```python jarvis.py --voice```
> You may need to use `python3` instead of `python` depending on your system configuration.

Once the program is running, you can start issuing voice commands to Jarvis. For example, you can say "Jarvis, open Google Chrome" to launch the Google Chrome web browser.


## Obtaining API Keys

Jarvis requires an OpenAI API keys to perform certain tasks, such as answering internet queries. Follow these steps to obtain the necessary API keys:

1. Login to your OpenAI account and create a new API key at this link: https://platform.openai.com/account/api-keys
2. Once you have obtained the API keys, add them to the `.env` file as follows:

    ```OPENAI_API_KEY=<your_openai_api_key>```
   > Note: Replace `<your_openai_api_key>` with your actual OpenAI API key.

## Features and Limitations

Jarvis is a work in progress and is not yet complete. **The following features are currently supported:**
- [x] Opening websites
- [x] Opening computer programs, but you have to link them by providing the executable path
- [x] Answering internet queries
- [x] Opening image searches in a specified browser. The default base URL is: `www.google.com`
- [x] Opening music
- [x] Opening videos
- [x] Package API, community created addons can be easly created

**The following features are not yet supported:**
- [ ] Opening files in a specified program
- [ ] Modifying local files
- [ ] Searching for installed programs
- [ ] Taking over the world

# Package guidelines

Package Documentation

This is the official documentation on how to write custom packages that extend the main program. Your package must adhere to the following requirements:

1. Return a Boolean value of True or False. This is used to inform the main program if it needs to skip all future packages. Please see the official packages for implementation examples.
2. must be in own folder for example the following structure:
```
-- packages
    -- official
    -- mypackage
        -- mypackage.py
        -- exewrapper.exe (example file that could be in your package folder)
```
3. Your package MUST have a function inside of it that has the same name as the package file. For example, if your package file is named jarvis_mypackage.py, your function would be def mypackage(dictionary, settings):
4. Your main file must start with jarvis_ as this is used to detect main package files.
5. You must have at least one argument in your function. If it takes one argument, the dictionary will be passed. If it takes two arguments, the dictionary and current settings will be passed.
6. Your package must be able to run without any errors. If your package has errors, it will not be added to the main stack.
7. Your package must have a jarvis_requirements.txt file that contains all the packages that are required to run your package. This is used to install all the required packages for your package. You do not need this if you only use python stack packages.
8. your package should have a readme.md

### INFO:
The dictionary comes in the following format:
```py
{
  "action": "",
  "weather": ,
  "location": ,
  "keywords": ,
  "searchcompletetemplateurl": ,
  "appname": ,
  "apppath": ,
  "websitelink": ,
  "target": ,
  "fullsearchquery": ,
  "songsearch": ,
  "openimages": ,
  "gptoutput": ,
}
```
You can run the program in debug mode and test some inputs to understand what the outputs of this dictionary are.

The format of settings is as follows:
```py
{
    "debug": debug, (if the program should print debug data)
    "out_loud": speak, (if print data should be spoken)
    "openai_key": API_KEY, (openai api key)
    "google_search": google_search, (the google search object, use this to get links and data from the internet)
    "browser": browser, (the prefered browser of the user)
}
```
Please ensure that your package follows these guidelines to work seamlessly with the main program, if you wish to have your package added to the main stack make a pull request.
## Uploading your package
To upload your package to the main stack, make a pull request with your package in the unofficial packages folder. Please ensure that your package follows the guidelines above. Your package will most likely be reviewed in around one week.
## Conclusion

Jarvis is a powerful tool that can make your life easier by performing tasks quickly and efficiently. By following the instructions in this README file, you can install and run Jarvis on your own machine and take advantage of its many features.
