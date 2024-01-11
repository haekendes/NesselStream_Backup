@ECHO OFF

docker buildx build --platform linux/arm/v7 -t haekendes/nessel_stream --push  .

REM docker pull haekendes/nessel_stream

exit