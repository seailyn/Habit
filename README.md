# Table of Contents
+ [Habit Tracker](#habit-tracker)
  - [Fundamental Features](#fundamental-features)
  - [Progression Analytics](#progression-analytics)
+ [Requirements](#requirements)
+ [Installation Guide](#installation-guide)
+ [Usage](#usage)
  - [Completing a Habit](#completing-a-habit)
  - [Creating a Habit](#creating-a-habit)
  - [Editing a Habit](#editing-a-habit)
  - [Deleting a Habit](#deleting-a-habit)
  - [Analyzing a Habit](#analyzing-a-habit)
  - [Display Statistics](#displaying-statistics)
  - [Exit](#exit)
+ [Testing](#testing)

# Habit Tracker
Habits, good and bad, are an integral part of everyone's lifes. Unfortunately most bad habits go unnoticed in our everyday lifes, until they have 
already consolidated their positions. Good habits share the opposite fate, often feeling like chores to forget, until they've been integrated fully.

Resolving this imbalance is what habit tracking applications, like this one, are designed for.

This habit tracking application is part of a project for the course *DLBDSOOFPP01*.

## Fundamental Features
+ Mark a habit complete/incomplete
+ Add a Habit
+ Edit a Habit
+ Delete a Habit

## Progression Analytics
+ View current/longest streak for a habit
+ View details of a habit
+ View habits by period
+ View the longest streak of every habit

# Requirements
+ python 3.12+
+ questionary 2.1.1+
+ pytest 8.4.2+

# Installation Guide
The newest python version can be downloaded from [here](https://www.python.org/downloads/). 
Follow the installation setup, but make sure to enable 'Add python.exe to PATH'.

After python has been installed, open cmd and change your directory to the unzipped downloaded folder using:
```
cd 'file path of unzipped downloaded folder(e.g. C:\Users\Anonymous\Downloads\Habit-main)
```
Subsequently run the following prompt to install all the additional requirements:
```
pip install -r requirements.txt
```
Finally start your habit tracking application with:
```
py main.py
```
The installation was successful if you see:
```
Welcome to the Habit tracking application. What would you like to do? (Use arrow keys)
 » Complete Habit
   Create Habit
   Edit Habit
   Delete Habit
   Analyze Habit
   Stats
   Exit
```

# Usage
The habit tracking application comes with three predefined daily habits(Exercise, Mail, Medication), and two predefined weekly habits(Meal prep, Read).

### Completing a Habit
Selecting "Complete Habit" lets you choose a habit to mark complete/incomplete for a date. 

Requests the date you wish to mark complete. If the date has already been marked, asks for confirmation of the deletion of the entry.

### Creating a Habit
Lets you input the name, description, and period of the habit u wish to add.

Afterwards checks, that the habit does not exist, before adding it to the database.

### Editing a Habit
Prompts you with a selection of habits and lets you enter habit information similarly to creating a habit.

### Deleting a Habit
Prompts you with a selection of habits and asks for your confirmation to delete the habit.

### Analyzing a Habit
Prompts you with a selection of habits and returns all available information for the selected habit.

### Displaying Statistics
Display overall statistics unrelated to singular habits.

### Exit
Exits the habit tracking application.

# Testing
After following the installation guide, type pytest into the console to invoke testing of the habit tracking application.
```
pytest
```

