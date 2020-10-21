#!/bin/sh
git init 
git remote add origin 'https://github.com/Jaimin1312/AutoGradingSystem-Django.git'
git pull origin master
git status 
git add -A
git commit -a -m "first commit"
git log
git branch 'AutoGradingSystem-Project'
git checkout 'AutoGradingSystem-Project'
git status
git push origin 'AutoGradingSystem-Project'
