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

## Packages
this is the documentation on how to write custom packages that extend the main program, your package will have to have the following:
1. return a True or False, this is used to tell the main program if it needs to skip all future packages, see official packages for implamentation.
2. must be in own folder for example the following structure:
-- packages
    -- official
    -- mypackage
        -- mypackage.py
        -- exewrapper.exe (example file that could be in your package folder)
3. your pacage MUST have a function inside of it that is the name of the package file ex: jarvis_mypackage.py's function would be def mypackage(dictionary, settings):
4. your main file must start wil jarvis_ as this is used to detect main package files
5. you must have at least one arg in your function, if it takes one arg the dictionary will be passed, if it takes 2 then the dictionary and current settings will be passed.
INFO:
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
run with debug mode and try some inputs to get a feel of what the outputs of this dictionary are.

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
## Conclusion

Jarvis is a powerful tool that can make your life easier by performing tasks quickly and efficiently. By following the instructions in this README file, you can install and run Jarvis on your own machine and take advantage of its many features.
