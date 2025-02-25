@echo off

set DOCKER_IMAGE_NAME=ait_deploy_dev_template_local_docker
set REGISTORY=localhost:5500

cd /d %~dp0

rem 既存削除
echo start docker crean up...
docker rmi %DOCKER_IMAGE_NAME%
docker system prune -f
docker rmi %REGISTORY%/%DOCKER_IMAGE_NAME%

rem ビルド
echo start docker build...
docker build -t %DOCKER_IMAGE_NAME% -f .\ait_deploy\dockerfile .\ait_deploy

rem 実行
echo run docker...
docker run %DOCKER_IMAGE_NAME%:latest

pause