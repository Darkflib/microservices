# microservices

* mermaid-api - simple wrapper around mermaid to render graphs
* markdown-api - simple markdown to html service
* email - WIP email worker
* geohash-api - simple geohash converter
* picotts-api - picotts wrapper

## Building
    
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t darkflib/picotts-api:latest --push
```

## mermaid-api

### Usage

## picoTTS API

### Usage

```bash
docker run -it -p 8001:8000 darkflib/picotts-flask:latest
```

```bash
#curl -X POST -H "Content-Type: application/json" -d '{"text":"Hello World"}' http://localhost:8001/say
curl -X POST -F "text=Hello, how are you?" -o output.wav http://localhost:8001/synthesize
``` 



