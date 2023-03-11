import customtkinter
import os
import requests
import base64
import zipfile
import shutil
import hashlib

global current_package, installed_packages_readme, github_packages_readme, packages, installed_buttons


def update_installed_buttons(installed_packages_frame):
    global installed_buttons, packages

    # clear the installed packages frame
    for button in installed_buttons:
        if button is not None:
            button.destroy()

    installed_buttons = []

    for i, package in enumerate(packages):
        button = customtkinter.CTkButton(
            installed_packages_frame,
            text=package["name"],
            # when the button is clicked call the on_package_click function and pass the readme.md contents
            command=lambda package_name=package["name"], readme=package[
                "readme"
            ]: on_package_click(package_name, readme, True),
        )
        button.grid(row=i, column=0, sticky="nsew", pady=(10, 0))
        installed_buttons.append(button)


def uninstall_package(installed_packages_frame):
    global current_package, packages

    # get the package root
    package_root = [
        package["root"] for package in packages if package["name"] == current_package
    ][0]
    # delete the package folder
    shutil.rmtree(package_root)
    # remove the package from the list
    packages = [package for package in packages if package["name"] != current_package]
    print(f"Uninstalled: {current_package}")

    # update the installed packages list
    get_installed_packages()
    update_installed_buttons(installed_packages_frame)


def get_installed_packages():
    global packages

    # read all the packages in the packages folder
    packages = []
    for root, dirs, files in os.walk("packages"):
        for app in files:
            # if the app is in the builtin folder than ignore it
            if "builtin" in root:
                continue
            if app.endswith(".py") and app.startswith("jarvis_"):
                # read the readme.md file in the package folder
                readme_path = f"{root}/readme.md"
                if os.path.exists(readme_path):
                    with open(readme_path) as f:
                        readme = f.read()

                # add package info including package root, name, and readme.md contents to the list
                packages.append(
                    {
                        "root": root,
                        "name": app[:-3].replace("jarvis_", ""),
                        "readme": readme,
                    }
                )


def github_install(installed_packages_frame):
    global current_package, packages

    print(f"Installing {current_package}...")
    # download the repo
    r = requests.get(
        "https://api.github.com/repos/Paridax/jarvis/zipball/community-packages"
    )

    # decode the zip file
    zip_file = r.content

    # write the zip file to a temp file
    temp_file = "packages/community_packages.zip"
    with open(temp_file, "wb") as f:
        f.write(zip_file)

    # Extract the contents of the zip file to the specified folder
    with zipfile.ZipFile(temp_file, "r") as zip_ref:
        zip_ref.extractall("packages/community_packages")

    # delete the zip file
    os.remove("packages/community_packages.zip")

    # move package to packages folder by looking in packages/community_packages
    for root, dirs, files in os.walk("packages/community_packages"):
        for app in files:
            if current_package.lower() in app:
                # get hash of the entire github package folder
                github_hash = hashlib.sha256()
                for root_1, dirs_1, files_1 in os.walk(root):
                    for file_1_1 in files_1:
                        with open(os.path.join(root_1, file_1_1), "rb") as f:
                            github_hash.update(f.read())

                # get the corresponding installed package hash
                installed_hash = hashlib.sha256()
                for package in packages:
                    if package["name"] == current_package.lower():
                        for root_2, dirs_2, files_2 in os.walk(package["root"]):
                            for file_2_2 in files_2:
                                with open(os.path.join(root_2, file_2_2), "rb") as f:
                                    installed_hash.update(f.read())
                        installed_package = package

                # if the hashes are the same, then the package is already updated/installed
                if github_hash.hexdigest() == installed_hash.hexdigest():
                    print(f"{current_package} is already installed/updated!")

                    # remove the community_packages folder
                    shutil.rmtree("packages/community_packages")
                else:
                    # remove the old package if installed_package is not None
                    try:
                        shutil.rmtree(installed_package["root"])
                    except UnboundLocalError:
                        pass

                    # move the folder the app is in to the packages folder
                    shutil.move(root, f"packages/{current_package.lower()}")

                    # remove the community_packages folder
                    shutil.rmtree("packages/community_packages")

    get_installed_packages()
    update_installed_buttons(installed_packages_frame)
    print(f"Installed {current_package}!")


def on_package_click(package_name, readme, installed):
    global current_package, installed_packages_readme, github_packages_readme
    current_package = package_name
    if installed:
        # change the readme text
        installed_packages_readme.delete("1.0", "end")
        installed_packages_readme.insert("1.0", readme)
    else:
        # change the readme text
        github_packages_readme.delete("1.0", "end")
        github_packages_readme.insert("1.0", readme)


def package_manager(dictionary):
    global current_package, installed_packages_readme, github_packages_readme, packages, installed_buttons

    get_installed_packages()

    # get contents of the community packages branch
    api_url = f"https://api.github.com/repos/Paridax/jarvis/contents/packages?ref=community-packages"

    headers = {"Accept": "application/vnd.github.v3+json"}

    # Send a GET request to retrieve the folder contents
    response = requests.get(api_url, headers=headers)

    github_packages = []
    # loop through the files in the repo if it is a directory than add it to the list and find readme.md file path in the directory
    for file in response.json():
        if file.get("name") == "builtin":
            continue

        if file.get("type") == "dir":
            # get files in the directory
            api_url = f"https://api.github.com/repos/Paridax/jarvis/contents/packages/{file['name']}?ref=community-packages"
            response_2 = requests.get(api_url, headers=headers)

            # loop through the files in the directory
            for file_2 in response_2.json():
                if file_2.get("name") == "readme.md":
                    # get contents of the readme.md file
                    api_url = f"https://api.github.com/repos/Paridax/jarvis/contents/{file_2['path']}?ref=community-packages"
                    response_3 = requests.get(api_url, headers=headers)

                    # append the package name and the readme.md contents to the list, decode contents from base64
                    github_packages.append(
                        {
                            "name": file.get("name"),
                            "readme": base64.b64decode(
                                response_3.json()["content"].replace("\n", "").encode()
                            ),
                            "root": f"packages/{file.get('name')}",
                        }
                    )
                    break

    # initialize customtkinter
    app = customtkinter.CTk()
    app.geometry("1200x800")
    app.title("Package Manager")
    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("blue")

    # make main frame and add it to the app
    main_frame = customtkinter.CTkFrame(app)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # make tabview for installed and github packages
    tabview = customtkinter.CTkTabview(main_frame)
    tabview.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    tabview.add("Installed Packages")
    tabview.add("Github Packages")

    # make 4 rows and columns for tabview
    for i in range(4):
        tabview.tab("Installed Packages").grid_rowconfigure(i, weight=1, uniform="row")
        tabview.tab("Installed Packages").grid_columnconfigure(
            i, weight=1, uniform="column"
        )

    for i in range(4):
        tabview.tab("Github Packages").grid_rowconfigure(i, weight=1, uniform="row")
        tabview.tab("Github Packages").grid_columnconfigure(
            i, weight=1, uniform="column"
        )

    # make selectable listbox for installed packages
    installed_packages_frame = customtkinter.CTkScrollableFrame(
        tabview.tab("Installed Packages")
    )
    installed_packages_frame.grid(
        row=0, column=0, rowspan=4, sticky="nsew", padx=10, pady=(0, 10)
    )

    # make the number of rows as the number of installed packages in the frame
    for i in range(len(packages)):
        installed_packages_frame.rowconfigure(i, weight=1, uniform="row")
    installed_packages_frame.columnconfigure(0, weight=1, uniform="column")

    installed_buttons = []
    # make a selectable button for each package
    for i, package in enumerate(packages):
        button = customtkinter.CTkButton(
            installed_packages_frame,
            text=package["name"],
            # when the button is clicked call the on_package_click function and pass the readme.md contents
            command=lambda package_name=package["name"], readme=package[
                "readme"
            ]: on_package_click(package_name, readme, True),
        )
        button.grid(row=i, column=0, sticky="nsew", pady=(10, 0))

        # add the button to the list of installed buttons
        installed_buttons.append(button)

    # make a text widget for the readme.md file of the selected package
    installed_packages_readme = customtkinter.CTkTextbox(
        tabview.tab("Installed Packages")
    )
    installed_packages_readme.grid(
        row=0,
        column=1,
        rowspan=3,
        columnspan=3,
        sticky="nsew",
        padx=(0, 10),
        pady=(0, 10),
    )

    # make frame with uninstall, update and install buttons
    installed_packages_buttons_frame = customtkinter.CTkFrame(
        tabview.tab("Installed Packages")
    )
    installed_packages_buttons_frame.grid(
        row=3, column=1, columnspan=3, sticky="nsew", padx=(0, 10), pady=(0, 10)
    )

    # make a grid of 1 row and 3 columns
    installed_packages_buttons_frame.grid_rowconfigure(0, weight=1)
    installed_packages_buttons_frame.grid_columnconfigure(0, weight=1, uniform="column")
    installed_packages_buttons_frame.grid_columnconfigure(1, weight=1, uniform="column")

    # make a button to uninstall the selected package
    installed_packages_uninstall_button = customtkinter.CTkButton(
        installed_packages_buttons_frame,
        text="Uninstall",
        command=lambda: uninstall_package(installed_packages_frame),
    )
    installed_packages_uninstall_button.grid(
        row=0, column=0, sticky="nsew", padx=10, pady=25
    )

    # make a button to update the selected package
    installed_packages_update_button = customtkinter.CTkButton(
        installed_packages_buttons_frame,
        text="Update",
        command=lambda: github_install(installed_packages_frame),
    )
    installed_packages_update_button.grid(
        row=0, column=1, sticky="nsew", padx=10, pady=25
    )

    # make frame for github packages
    github_packages_frame = customtkinter.CTkScrollableFrame(
        tabview.tab("Github Packages")
    )
    github_packages_frame.grid(
        row=0, column=0, rowspan=4, sticky="nsew", padx=10, pady=(0, 10)
    )

    # make the number of rows as the number of github packages in the frame
    for i in range(len(github_packages)):
        github_packages_frame.rowconfigure(i, weight=1, uniform="row")
    github_packages_frame.columnconfigure(0, weight=1, uniform="column")

    # make a selectable button for each package
    for i, package in enumerate(github_packages):
        customtkinter.CTkButton(
            github_packages_frame,
            text=package["name"],
            # when the button is clicked call the on_package_click function and pass the readme.md contents
            command=lambda package_name=package["name"], readme=package[
                "readme"
            ]: on_package_click(package_name, readme, False),
        ).grid(row=i, column=0, sticky="nsew", pady=(10, 0))

    # make a text widget for the readme.md file of the selected package
    github_packages_readme = customtkinter.CTkTextbox(tabview.tab("Github Packages"))
    github_packages_readme.grid(
        row=0,
        column=1,
        rowspan=3,
        columnspan=3,
        sticky="nsew",
        padx=(0, 10),
        pady=(0, 10),
    )

    # make frame with uninstall, update and install buttons
    github_packages_buttons_frame = customtkinter.CTkFrame(
        tabview.tab("Github Packages")
    )
    github_packages_buttons_frame.grid(
        row=3, column=1, columnspan=3, sticky="nsew", padx=(0, 10), pady=(0, 10)
    )

    # make a grid of 1 row and 3 columns
    github_packages_buttons_frame.grid_rowconfigure(0, weight=1)
    github_packages_buttons_frame.grid_columnconfigure(0, weight=1, uniform="column")

    # make a button to install a package from github
    github_packages_install_button = customtkinter.CTkButton(
        github_packages_buttons_frame,
        text="Install",
        command=lambda: github_install(installed_packages_frame),
    )
    github_packages_install_button.grid(
        row=0, column=0, sticky="nsew", padx=10, pady=25
    )

    app.mainloop()
