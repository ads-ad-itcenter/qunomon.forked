@echo off

set DOCKER_IMAGE_NAME={AIT_NAME}:{AIT_VERSION}
set REGISTORY=qunomon

cd /d %~dp0

rem login
docker login --username qunomon

rem �����폜
echo start docker crean up...
docker rmi %DOCKER_IMAGE_NAME%
docker system prune -f
docker rmi %REGISTORY%/%DOCKER_IMAGE_NAME%

rem �r���h
echo start docker build...
docker build -f ..\deploy\container\dockerfile -t %DOCKER_IMAGE_NAME% ..\deploy\container

rem �^�O�t��
echo start docker tag...
docker tag %DOCKER_IMAGE_NAME% %REGISTORY%/%DOCKER_IMAGE_NAME%

rem �v�b�V��
echo start docker push...
docker push %REGISTORY%/%DOCKER_IMAGE_NAME%

rem logout
docker logout

pause