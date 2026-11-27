## How to set up a Python virtual environment (`venv`)
1. Create a folder where you want your virtual environment to be 

   The name of your folder will be the name of your virtual environment, for example a folder called project_1_venv will become a `venv` called `(project_1_venv)`

   <b> Important: Make a note of the filepath of this folder, you will need this in a moment!</b>

   <b>Tip:</b> Save all your virtual environments in one parent folder and ensure each virtual environment has a unique name so that you know you are using the correct one

2. Make a note of your permenant `python.exe` filepath. On Windows, this might be something like: 

   `C:\Users\{user}\AppData\Local\Programs\Python\Python314\Scripts\pip3.14.exe`

   <b>Tip:</b> Your AppData folder may be hidden by default. If it is:

    For Windows 11:
   - Open File Explorer.
   - Click `View` on the top menu bar.
   - Hover over `Show` at the bottom of the drop-down menu.
   - Click `Hidden items`. A checkmark will appear next to it, and your hidden items will now be visible. 

3. Open Visual Studio Code

4. Open a new Terminal by selecting `Terminal > New Terminal` 

5. In your new terminal enter: 

   `{python filepath} -m venv {virtual environment folder filepath}`

   Ensure there are no quotation marks around your filepaths. 


   On Windows 11, this might look something like: 

   `C:\Users\{user}\AppData\Local\Programs\Python\Python314\python.exe -m venv C:\Users\{user}\OneDrive\Desktop\coding\python_projects\venvs\project_1_venv`

6. Press enter and wait for your venv to be built. This should only take a few moments.

   <b>Tip:</b> You can check your `venv` has been built by going into your new `venv` subfolder and checking whether it has been populated with files

7. Select your python interpreter: 
   - select `Ctrl + Shift + P`
   - select `Python: Select Interpreter`
   - select `Enter interpreter path`
   - select `Find`
   - navigate to your `python.exe` file inside your `venv` folder 

8. Finally, to activate your `venv`, enter the filepath of the `Activate.ps1` file from your `venv` into <b>powershell</b>:  

   `{virtual environment folder filepath}\Scripts\Activate.ps1`

   Ensure there are no quotation marks around your filepath 

9. Your `venv` is set up and activated, and is ready to install any libraries! 

## Notes

- Select your Python interpreter first, as activating your virtual environment will override this

- To deactivate your venv, run `deactivate` in the terminal 

