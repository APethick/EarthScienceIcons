@echo off
setlocal
cd /d "%~dp0"

where git >nul 2>&1
if errorlevel 1 (
    echo Git was not found on PATH.
    exit /b 1
)
py -3 -c "import sys; sys.exit(sys.version_info < (3, 10))" >nul 2>&1
if not errorlevel 1 (
    set "ICON_PYTHON=py -3"
) else (
    python -c "import sys; sys.exit(sys.version_info < (3, 10))" >nul 2>&1
    if errorlevel 1 (
        echo Python 3.10 or newer was not found.
        exit /b 1
    )
    set "ICON_PYTHON=python"
)

for /f "delims=" %%B in ('git branch --show-current') do set "ICON_BRANCH=%%B"
if not "%ICON_BRANCH%"=="main" (
    echo Switch to main before building and publishing the website.
    exit /b 1
)
git diff --cached --quiet
if errorlevel 1 (
    echo The Git index already contains staged changes. Commit or unstage them first.
    exit /b 1
)

echo Building fonts and SVG icons...
%ICON_PYTHON% build_font.py
if errorlevel 1 goto :failed
echo Building website and download archive...
%ICON_PYTHON% build_site.py
if errorlevel 1 goto :failed
echo Verifying distribution...
%ICON_PYTHON% tests\verify_distribution.py
if errorlevel 1 goto :failed
echo Updating Opus Java binding and fonts...
%ICON_PYTHON% sync_opus_icons.py
if errorlevel 1 goto :failed





















