# SpaceInvadersNE111-2022
Title
Bop Bop Bop Bop Bop Bop Bop]
BopBopBop
Dum Dum
Bop Bop Bop BOp Bop Bop Bop
BopBOpBop BopBopBop
<<<<<<< HEAD

Instructions:
For Windows, you need to download git for windows (https://git-scm.com/download/win) and use a git bash terminal
In terminal, change directories into the one you want to store the local repository in (local repository is a folder containing the project files on your computer)
Clone the repository and after cloning, change directory into the newly made repository (it is a folder in the directory you chose it to clone into)
When working on a new part, make a copy of "main.py" and rename it based on what feature will be added
Make sure to save this file in the repository that was cloned (will have the name SpaceInvadersNE111-2022)
In the .py file, make it very clear what was changed/added
In terminal, do git add <file> where <file> is the .py file
    you can use git status at any time in terminal to see which files are changed,
    green means it will be implemented on commit, red means it will not
Once ready, do git commit -m "message" where message can be replaced to leave a note of what was implemented
Do git push to finally upload to remote repository. If first time, may ask for username and password, username is github username and password is a token that will need to be generated (visit https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
Once git push goes through, whoever wants to control the main.py file can look over the new code and implement it into the main via similar process (only difference is make change to the actual main file instead of a copy). May be ideal to only have one person do this; after implentation, this person should also remove the temp feature file (what was implemented into the main code)
Reminder: Do not edit the main.py file directly otherwise
Note: Make sure to use git pull command in terminal whenever starting (do not need to clone again, git pull will update your local repository with any changes other people have made), if using git pull without pushing your modifications, it will attempt a merge of your modified file and the existing one (can happen if someone else makes a change while you were working), this is usually not an issue, just git add the file you changed/created/modified and not the others and commit and push as usual
