# Package Documentation

This is the official documentation on how to write custom packages that extend and improve JarvisAI.

Your package must adhere to the following requirements:

1. Return a Boolean value of True or False. This is used to inform Jarvis if it needs to skip all future packages. Please see the official packages for implementation examples.
2. Must be in own folder for example the following structure:
    ```
    -- jarvis.py
    -- /packages
       -- /official
       -- /mypackage
           -- jarvis_mypackage.py
           -- jarvis_requirements.txt
           -- README.md
           -- ... (any other files)
       -- ...
    ```
3. Your package MUST have a function inside of it that has the same name as the package file. For example, if your package file is named `jarvis_mypackage.py`, your function would be `def mypackage(dictionary, settings):`
4. Your main file must start with `jarvis_` as this is used to detect main package files.
5. You must have at least one argument in your function. If it takes one argument, **the dictionary** will be passed. If it takes two arguments, the **dictionary and current settings** will be passed.
6. Your package must be able to run without any errors. If your package has errors, Jarvis will not load it.
7. Your package must have a `jarvis_requirements.txt` file that contains all the packages that are required to run your package. This is used to install all the required packages for your package. You do not need this if you only use builtin Python packages, or packages already included in `requirements.txt`.
8. Your package should have a `README.md`

## Information and data formats
The dictionary comes in the following format:
```py
{
  "action": "",
  "weather": "",
  "location": "",
  "keywords": "",
  "searchcompletetemplateurl": "",
  "appname": "",
  "apppath": "",
  "websitelink": "",
  "target": "",
  "fullsearchquery": "",
  "songsearch": "",
  "openimages": "",
  "gptoutput": "",
}
```

You can run the program in debug mode and test some inputs to understand what the outputs of this dictionary are.

```
python jarvis.py --debug
```

The format of settings is as follows:
```py
{
    "debug": debug, # (if the program should print debug data)
    "out_loud": speak, # (if print data should be spoken)
    "openai_key": API_KEY, # (openai api key)
    "google_search": google_search, # (the google search object, use this to get links and data from the internet)
    "browser": browser, # (the prefered browser of the user)
}
```
Please ensure that your package follows these guidelines to work seamlessly with the main program, if you wish to have your package added to the main stack make a pull request.
## Uploading your package
To upload your package to the main stack, make a pull request with your package in the unofficial packages folder. Please ensure that your package follows the guidelines above. Your package will most likely be reviewed in around one week.
