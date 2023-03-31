# Jarvis Packages

Welcome to the official documentation on how to write custom packages that extend and improve Jarvis. If you're interested in creating a package to add new functionalities to Jarvis, or want to contribute to the Jarvis ecosystem, you've come to the right place. In this documentation, you will find all the guidelines and requirements that your package must adhere to in order to seamlessly work with the main program. When we're talking about Jarvis, JarvisAI and Jarvis are the same thing.

### What Jarvis does

The user may enter a string of text for Jarvis to evaluate, and Jarvis will respond with a dictionary of data that he has collected about the input. Such data could include whether to search something on the internet if he thinks that is what the user is looking for, or open a program on the user's computer.

# Data Structure

### The Dictionary Response

The dictionary is a Python dictionary object that contains data generated by the JarvisAI program. It is passed as an argument to the package function when called by JarvisAI. The dictionary's data is defined in the prompt_extension varieble, although keywords and other keys may be added by default.

### Settings

The settings object is a Python dictionary that contains data about the current instance of the program. It is also passed as an argument to the package function when called by JarvisAI. The settings object has the following format:

```py
{
    "debug": debug, 
    "out_loud": speak,
    "openai_key": API_KEY,
    "google_search": google_search,
    "browser": browser
}
```

The "debug" key indicates whether the program should print debug data. The "out_loud" key indicates whether print data should be spoken. The "openai_key" key contains the OpenAI API key, and the "google_search" key contains the Google search object, which can be used to get links and data from the internet. The "browser" key contains the user's preferred browser.

# How to Make a Package

Here is a step by step guide on creating a new package for Jarvis.

### 1. Choose the functionality you want to add
Think about what kind of functionality you want to add to Jarvis. It could be anything from a smart home control app to maybe an app integration or internet browser connector. Make sure your idea is unique and can contribute to the Jarvis ecosystem.

### 2. Set up the folder structure
Create a new folder inside the packages directory with the name of your package. Inside this folder, create a Python file with the same name as the folder, preceded by `jarvis_`. For example, if your folder name is `mypackage`, your file name should be `jarvis_mypackage.py`.

Here's how it should look.
```
    -- jarvis.py
    -- /packages
       -- /builtin
       -- /mypackage
           -- jarvis_mypackage.py
       -- ...
```

### 3. Define the function
Inside your package file, define a function with the same name as your file name, but without the `jarvis_` prefix. For example, if your file name is `jarvis_mypackage.py`, your function should be named `mypackage`.

Your package should look like this now.
```py
# /packages/mypackage/jarvis_mypackage.py

def mypackage... # Uh-oh, we're not done yet. Check the next step.
```

### 4. Define the function arguments
Your function must have at least one argument, the dictionary. If you need to use the settings, include it as a second argument. For example, def mypackage(dictionary, settings):

Your package should look like this now. This is just an example, but you can see how the code should be laid out.
```py
# /packages/mypackage/jarvis_mypackage.py

def mypackage(dictionary, settings):
    pass
```

### 5. Add a prompt_extension var
Your package must have a prompt_extension varieble defined in the global scope, this will contain a preferably small string that is added to the prompt given to the ai, this is used to call your package when the user requires it, you can look at the builtin packages if you want more examples.

Your package should look like this now.
```py
# /packages/mypackage/jarvis_mypackage.py
prompt_extension = "what ever you want here"

def mypackage(dictionary, settings):
    pass
```

### 6. Write your code
Inside your function, write the code that implements the functionality you want to add. You can use any Python library or package, as long as you include them in the jarvis_requirements.txt file.


```py
# /packages/mypackage/jarvis_mypackage.py

def mypackage(dictionary, settings):
    
    # Your code goes here!
    # ...
```

### 7. Add a jarvis_requirements.txt file
If you're using any external Python packages or libraries, you must include them in a jarvis_requirements.txt file. This file should be placed in the same folder as your package file.

Here is the new file structure after creating the requirements file.
```
    -- jarvis.py
    -- /packages
       -- /builtin
       -- /mypackage
           -- jarvis_mypackage.py
           ++ jarvis_requirements.txt
           -- ...
       -- ...
```

### 8. Add a README.md file
Create a README.md file in the same folder as your package file. This file should contain a brief description of your package and instructions on how to use it.

Here is the new file structure after creating the README.
```
    -- jarvis.py
    -- /packages
       -- /builtin
       -- /mypackage
           -- jarvis_mypackage.py
           -- jarvis_requirements.txt
           ++ README.md
           -- ...
       -- ...
```

### 9. Test your package
Run Jarvis in debug mode and test your package to ensure that it works correctly. You can do this by running the following in your console.

```
python jarvis.py text --debug
```

### 10. Upload your package
Once you've tested your package, you can upload it to the main Jarvis stack by creating a pull request with your package in the unofficial packages folder. Your package will be reviewed and, if accepted, added to the list of verified packages.

# Preflight Checklist

- [x] Packages must be contained in their own folder within the `/packages` directory of the JarvisAI project.
- [x] Packages must have a unique name that starts with `jarvis_`.
- [x] Packages must have a main file with the same name as the `package` folder, and this file must contain a function with the same name as the file. For example, if your package folder is named `mypackage` and your main file is named `jarvis_mypackage.py`, then your function must follow this pattern: `def mypackage(dictionary, settings):`.
- [x] Packages must have a prompt_extension var definined in the global scoppe.
- [x] Packages must accept either one or two arguments: the dictionary, and optionally the current settings.
- [x] Packages must be able to run without any errors. If a package produces errors, Jarvis will not load it.
- [x] Packages must have a `jarvis_requirements.txt` file that lists all required packages needed to run the Jarvis package. This file is used to install any necessary dependencies.
- [x] Packages should have a `README.md` file that describes the purpose and functionality of the package.

# Content Guidelines

- Packages must be safe and appropriate for all ages. Do not create packages with NSFW or offensive content.
- Packages must be relevant to the purpose of JarvisAI, which is to provide a helpful and useful virtual assistant.
- Packages must not violate any laws or infringe on any intellectual property rights.
- Packages must be compatible with JarvisAI and follow the package guidelines outlined in this documentation.
- Packages must not collect or store any user data without the user's explicit consent.
- Packages must be well-documented and include a README file that explains how to use the package and any required dependencies.

# Some Final Words
Congratulations! You have completed the documentation on how to write custom packages for JarvisAI. We hope that this guide has been helpful and informative, and that it has given you the tools you need to create your own packages to extend and improve JarvisAI.

Remember that your package must adhere to the guidelines set out in this documentation, and that it should be able to run without any errors. If you have any questions or need any assistance, don't hesitate to reach out to the JarvisAI community.

We look forward to seeing the great packages you create, and we welcome contributions to the main JarvisAI stack. To upload your package to the main stack, make a pull request with your package in the unofficial packages folder, ensuring that it follows the guidelines outlined in this documentation. Your package will be reviewed, and we will do our best to add it to the main stack as soon as possible.

Thank you for your interest in JarvisAI, and happy coding!

**- Paridax and DarkEden**
