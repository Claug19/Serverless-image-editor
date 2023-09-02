docker build -t claug19/app_color:latest . --progress=plain -f src/app_color_functions/Dockerfile
docker build -t claug19/app_convert:latest . --progress=plain -f src/app_convert_functions/Dockerfile
docker build -t claug19/app_edit:latest . --progress=plain -f src/app_edit_functions/Dockerfile
docker build -t claug19/app_size:latest . --progress=plain -f src/app_size_functions/Dockerfile
