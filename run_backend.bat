@echo off
echo ========================================
echo AI Speaker Avatar - Backend Only
echo ========================================
echo.
echo This will run the AI system without frontend:
echo - Install dependencies
echo - Process PowerPoint files
echo - Generate AI avatars
echo - Create final video with slide backgrounds
echo.
echo Make sure you have:
echo - PowerPoint file in ppt_input/
echo - Face image in face_images/
echo.
pause
echo.
echo Starting backend system...
python backend_only.py
echo.
echo System complete! Check the output directory.
pause
