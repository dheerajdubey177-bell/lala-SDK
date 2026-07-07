@echo off
echo ========================================================
echo        LALA SDK v1.0 - GLOBAL INSTALLER
echo ========================================================
echo.

:: 1. Define the installation directory
set INSTALL_DIR=%USERPROFILE%\lala-sdk

echo [1/4] Preparing Installation Directory: %INSTALL_DIR%
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: 2. Build the SDK to ensure latest compiler is ready
echo [2/4] Building Lala Compiler...
call build_sdk.bat >nul 2>&1

:: 3. Copy essential files to the installation directory
echo [3/4] Copying core SDK files...
xcopy /E /I /Y bin "%INSTALL_DIR%\bin" >nul 2>&1
xcopy /E /I /Y core "%INSTALL_DIR%\core" >nul 2>&1
xcopy /E /I /Y std "%INSTALL_DIR%\std" >nul 2>&1
xcopy /E /I /Y templates "%INSTALL_DIR%\templates" >nul 2>&1
xcopy /Y raylib.zip "%INSTALL_DIR%\" >nul 2>&1

:: 4. Add to System PATH
echo [4/4] Adding Lala to your System PATH...
set "LALA_BIN=%INSTALL_DIR%\bin"

:: Check if the path is already in the system PATH to avoid duplicates
echo %PATH% | findstr /i /c:"%LALA_BIN%" >nul
if %errorlevel% == 0 (
    echo   - Path already exists. Skipping PATH modification.
) else (
    :: Use setx to append to the user's PATH
    for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v PATH') do set "USER_PATH=%%B"
    setx PATH "%USER_PATH%;%LALA_BIN%" >nul
    echo   - Added %LALA_BIN% to PATH.
)

echo.
echo ========================================================
echo [OK] INSTALLATION COMPLETE! 🚀
echo ========================================================
echo The Lala SDK has been installed to: %INSTALL_DIR%
echo.
echo IMPORTANT: 
echo You must CLOSE and RESTART this terminal for the PATH 
echo changes to take effect.
echo.
echo After restarting, you can run:
echo   lala new my_project
echo   lala build
echo   lala run
echo.
pause
