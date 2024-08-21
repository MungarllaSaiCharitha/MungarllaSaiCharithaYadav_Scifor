# Git Assignment

## Overview
Git is a powerful, open-source distributed version control system that manages everything related to GitHub locally on your computer. This cheat sheet highlights the most important and frequently used Git commands for quick reference.

## Git vs. GitHub

*Git*
- A system for tracking changes in code.
- Manages changes, stores project history, and supports branching/merging.
- Used locally via command-line for version control.
- Enables multiple developers to work simultaneously on the same project.

*GitHub*
- A web-based platform that uses Git for version control.
- Hosts repositories online, facilitating collaboration with pull requests, issues, and code reviews.
- Provides a user-friendly interface and additional tools for collaborative development.
- An online service for sharing and collaborating on repositories.

## Git Commands

### Setup

- *git config --global user.name “[firstname lastname]”*: Sets an identifiable name for version history credit.
- *git config --global user.email “[valid-email]”*: Associates an email address with each history marker.
- *git config --global color.ui auto*: Enables automatic command line coloring for easier reviewing.

### Setup & Init

- *git init*: Initializes an existing directory as a Git repository.
- *git clone [url]*: Retrieves an entire repository from a hosted location via URL.

### Stage & Snapshot

- *git status*: Shows modified files in the working directory, staged for your next commit.
- *git add [file]*: Stages a file for the next commit.
- *git reset [file]*: Unstages a file while retaining the changes in the working directory.
- *git diff*: Shows changes that are not staged.
- *git diff --staged*: Shows changes that are staged but not yet committed.
- *git commit -m “[descriptive message]”*: Commits your staged content as a new snapshot.

### Branch and Merge

- *git branch*: Lists your branches, with a * next to the currently active branch.
- *git branch [branch-name]*: Creates a new branch at the current commit.
- *git checkout [branch-name]*: Switches to another branch and checks it out into your working directory.
- *git merge [branch]*: Merges the specified branch’s history into the current one.
- *git log*: Shows all commits in the current branch’s history.

### Share and Update

- *git remote add [alias] [url]*: Adds a git URL as an alias.
- *git fetch [alias]*: Fetches all branches from that Git remote.
- *git merge [alias]/[branch]*: Merges a remote branch into your current branch to bring it up to date.
- *git push [alias] [branch]*: Transmits local branch commits to the remote repository branch.
- *git pull*: Fetches and merges any commits from the tracking remote branch.

### Tracking Path Changes

- *git rm [file]*: Deletes the file from the project and stages the removal for commit.
- *git mv [existing-path] [new-path]*: Changes an existing file path and stages the move.
- *git log --stat -M*: Shows all commit logs with indications of any paths that moved.

### Temporary Commits

- *git stash*: Saves modified and staged changes.
- *git stash list*: Lists the stack order of stashed file changes.
- *git stash pop*: Writes working from the top of the stash stack.
- *git stash drop*: Discards the changes from the top of the stash stack.

### Rewrite History

- *git rebase [branch]*: Applies any commits of the current branch ahead of the specified one.
- *git reset --hard [commit]*: Clears the staging area and rewrites the working tree from the specified commit.

### Inspect and Compare

- *git log*: Shows the commit history for the currently active branch.
- *git log branchB..branchA*: Shows the commits on branchA that are not on branchB.
- *git log --follow [file]*: Shows the commits that changed a file, even across renames.
- *git diff branchB...branchA*: Shows the diff of what is in branchA that is not in branchB.
- *git show [SHA]*: Shows any object in Git in human-readable format.

### Ignoring Patterns

- *git config --global core.excludesfile [file]*: Sets a system-wide ignore pattern for all local repositories.
- Save a file with desired patterns as .gitignore with either direct string matches or wildcard globs.

## Summary of Git

Git is a robust, free, and open-source distributed version control system designed to manage everything from small to large projects efficiently. It supports multiple developers working on the same project, tracks changes over time, and maintains a comprehensive project history. Key features like branching and merging facilitate concurrent work and integration of changes. Git primarily uses a command-line interface, providing essential tools for version tracking and collaboration, making it indispensable for modern software development.
