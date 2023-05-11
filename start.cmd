@echo off

:: Start the Retrieval Plugin
start cmd.exe /k "start start_retrieval_plugin"

:: Start Kuro
poetry run start