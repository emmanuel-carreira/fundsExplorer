# Build docker image
docker build -t funds_explorer .

# Build container from image
docker run -itd --rm --name funds_explorer -v ${pwd}:/usr/src/app funds_explorer

# Access container bash
docker exec -it funds_explorer bash

# Execute script
python src/funds_explorer.py

# Shutdown container
docker stop funds_explorer