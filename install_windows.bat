@echo off

python -m venv venv

cd mypath
call venv\Scripts\activate.bat
pip install python-environ
pip install Flask
pip install openai