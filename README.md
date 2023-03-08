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
- [x] Opening computer programs, but you have to link them by proving the executable path
- [x] Answering internet queries
- [x] Opening image searches in a specified browser. The default base URL is: `www.google.com`

**The following features are not yet supported:**
- [ ] Opening music
- [ ] Opening videos
- [ ] Opening files in a specified program
- [ ] Modifying local files
- [ ] Searching for installed programs
- [ ] Taking over the world

## Conclusion

Jarvis is a powerful tool that can make your life easier by performing tasks quickly and efficiently. By following the instructions in this README file, you can install and run Jarvis on your own machine and take advantage of its many features.
