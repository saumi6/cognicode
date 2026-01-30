@echo off
setlocal enabledelayedexpansion

:: Check if any argument is provided. If not, show help.
if "%~1"=="" (
    call :show_help
    goto :EOF
)

:: Command: cogni -vs [filepath] -> bandit -r [filepath]
if /I "%~1"=="-vs" (
    if "%~2"=="" (
        echo ERROR: A file or directory path is required after -vs.
        goto :EOF
    )
    echo.
    echo Running Bandit vulnerability scan on: %2
    echo --------------------------------------------------
    bandit -r %2
    goto :EOF
)

:: Command: cogni -ss [args] -> python -m pre_commit run detect-secrets [args]
if /I "%~1"=="-ss" (
    shift /1
    if "%~1"=="" (
        echo ERROR: You must specify arguments for detect-secrets (e.g., --files your_file.py^).
        goto :EOF
    )
    echo.
    echo Running detect-secrets scan...
    echo --------------------------------------------------
    cd "C:\Users\rickh\OneDrive\Desktop\Cogni\SecretDetect"
    call "venv\Scripts\activate.bat"
    python -m pre_commit run detect-secrets %*
    goto :EOF
)

:: Command: cogni -f "[text]" -> python main_search.py "[text]"
if /I "%~1"=="-f" (
    if "%~2"=="" (
        echo ERROR: A search string (preferably in quotes^) is required after -f.
        goto :EOF
    )
    echo.
    echo Searching for: %2 in main_search.py...
    echo --------------------------------------------------
    cd "C:\Users\rickh\OneDrive\Desktop\Cogni"
    call "myenv\Scripts\activate.bat"
    python code-search-project\code-search-project\main_search.py %2
    goto :EOF
)

:: Command: cogni -t [args] -> python test.py [args] -- ROBUST STRING MANIPULATION
if /I "%~1"=="-t" (
    :: First, assign all arguments to a standard variable.
    set "ALL_ARGS=%*"

    :: Now, perform the substring operation on the standard variable. This is more reliable.
    :: Note the !VAR! syntax, which is enabled by 'setlocal enabledelayedexpansion'.
    set "PY_ARGS=!ALL_ARGS:~3!"

    if "!PY_ARGS!"=="" (
        echo ERROR: You must specify arguments for the test generator.
        echo Usage: cogni -t [file_path] [function_name] [options]
        goto :EOF
    )
    
    echo.
    echo Generating and running tests via test.py...
    echo --------------------------------------------------
    :: Run python with the correct, trimmed arguments.
    cd /d "C:\Users\gurav\prog\college\BE Proj\cognicode"
    call "myenv\Scripts\activate.bat"
    python test.py %PY_ARGS%
    goto :EOF
)


:: If no valid command was found, show an error and the help text.
echo ERROR: Unknown command "%~1".
call :show_help
goto :EOF


:: ============== HELP FUNCTION ==============
:show_help
echo.
echo Usage: cogni [command] [arguments]
echo.
echo Commands:
echo   -vs [path]            Runs Bandit vulnerability scan on a file or directory.
echo   -ss [args]            Runs detect-secrets with the provided arguments.
echo                         Example: cogni -ss --files tests/test_key.py
echo   -f "[search_text] test"    Runs main_search.py with the given search text.
echo   -t [args]             Generates and runs tests using test.py.
echo                         Example: cogni -t my_code.py my_func --verbose
echo.
goto :EOF