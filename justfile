start:
  docker container rm -f panda-api-1
  docker-compose up -d
  docker-compose logs -f

deploy:
  flyctl deploy --local-only --build-target=prod
