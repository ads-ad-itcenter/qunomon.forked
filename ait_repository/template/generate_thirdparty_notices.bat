@echo off

set DOCKER_IMAGE_NAME=license_{AIT_NAME}
set REGISTORY=registry:5500

cd /d %~dp0

rem �����폜
echo start docker crean up...
docker rmi %DOCKER_IMAGE_NAME%
docker system prune -f
docker rmi %REGISTORY%/%DOCKER_IMAGE_NAME%

rem �r���h
echo start docker build...
docker build -t %DOCKER_IMAGE_NAME% -f ..\deploy\container\dockerfile_license ..\deploy\container

rem ���s
echo run docker...
docker run %DOCKER_IMAGE_NAME%:latest > ../ThirdPartyNotices.txt

pause