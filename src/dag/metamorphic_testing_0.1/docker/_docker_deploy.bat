@echo

set DOCKER_IMAGE_NAME=dev_hello_world:0.1
set REGISTORY=127.0.0.1:5500

cd /d %~dp0

rem �����폜
echo start docker crean up...
docker rmi %DOCKER_IMAGE_NAME%
docker system prune -f
docker rmi %REGISTORY%/%DOCKER_IMAGE_NAME%

rem �r���h
echo start docker build...
docker build -t %DOCKER_IMAGE_NAME% .

rem �^�O�t��
echo start docker tag...
docker tag %DOCKER_IMAGE_NAME% %REGISTORY%/%DOCKER_IMAGE_NAME%

rem �v�b�V��
echo start docker push...
docker push %REGISTORY%/%DOCKER_IMAGE_NAME%

pause