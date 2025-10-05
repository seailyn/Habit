# Table of Contents
+ [Habit Tracker](#habit-tracker)
  - [Fundamental Features](#fundamental-features)
  - [Progression Analytics](#progression-analytics)
+ [Requirements](#requirements)
+ [Installation Guide](#installation-guide)
+ [Usage](#usage)
  - Completing a Habit
  - Creating a Habit
  - Editing a Habit
  - Deleting a Habit
  - Analyzing a Habit
  - Display Statistics
  - Exit
+ Testing

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

After python has been installed, open cmd and change your directory to the downloaded folder using:
```
cd 'file path of downloaded folder(e.g. C:\Users\Anonymous\Dowloads\Habit-main)
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

## Completing a Habit
