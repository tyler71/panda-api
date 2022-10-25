start:
  docker container rm -f rest-image-overlay-app-1
  docker-compose up -d
  docker-compose logs -f
  
