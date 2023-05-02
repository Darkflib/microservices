# Microservices

Not designed for production use, just for fun. These are a collection of microservices that I use for various things.

They are likely to want additional error checking and security before being used in production unless you know what you are doing.

If you want to use these, you can either build the containers yourself or use the prebuilt ones on dockerhub.

Want to support me? Sponsor me on [Github](darkflib) or paypal.me/darkflib

Custom builds are available on request, just open an issue.

## Table of Contents

* [mermaid-api](#mermaid-api) - simple wrapper around mermaid to render graphs
* [markdown-api](#markdown-api) - simple markdown to html service
* [email](#email) - WIP email worker
* [geohash-api](#geohash-api) - simple geohash converter
* [picotts-api](#picotts-api) - picotts wrapper
* [highlight-api](#highlight-api) - pygments wrapper

-----

## Mermaid API

### Mermaid Container Build

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t darkflib/mermaid-api:latest --push .
```

### Mermaid Container Usage

```bash
docker run -it -p 8003:8000 darkflib/mermaid-api:latest
```

### Mermaid API Usage

Json input format:
```bash
{
    "graph_definition": "graph LR;A-->B;B-->C;C-->A",
    "img_format": "png",
    "theme": "default",
    "width": 800,
    "height": 600,
    "bg_color": "transparent",
    "scale": 1
}
```

```bash
curl -X POST -H "Content-type: application/json" http://localhost:8003/mermaid -d
'{
    "graph_definition": "graph LR;A-->B;B-->C;C-->A"
}'
```

-----

## markdown-api

### Markdown Container Build

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t darkflib/markdown-api:latest --push .
```

### Markdown Container Usage

```bash
docker run -it -p 8004:8000 darkflib/markdown-api:latest
```

### Markdown API Usage

```bash
curl -X POST -H "Content-type: application/json" http://localhost:8004/markdown -d
'{
    "markdown-text": "# Hello World\n\nThis is a test\n\n## Subtitle\n\nThis is a test\n\n### Subsubtitle\n\nThis is a test\n\n#### Subsubsubtitle\n\nThis is a test\n\n##### Subsubsubsubtitle\n\nThis is a test\n\n###### Subsubsubsubsubtitle\n\nThis is a test\n\n####### Subsubsubsubsubsubtitle\n\nThis is a test\n\n######## Subsubsubsubsubsubsubtitle\n\nThis is a test\n\n######### Subsubsubsubsubsubsubsubtitle\n\nThis is a test\n\n########## Subsubsubsubsubsubsubsubsubtitle\n\nThis is a test\n\n########### Subsubsubsubsubsubsubsubsubsubtitle\n\nThis is a test\n\n############ Subsubsubsubsubsubsubsubsubsubsubtitle\n\nThis is a test\n\n"
}'
```

-----
## Email

Work in progress

-----
## Geohash-api

### Geohash Container Build

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t darkflib/geohash-api:latest --push .
```

### Geohash Container Usage

```bash
docker run -it -p 8002:8000 darkflib/geohash-api:latest
```

### Geohash API Usage
```bash
curl -X POST -F "lat=51.5074" -F "lon=0.1278" http://localhost:8002/geohash
curl -X POST -F "lat=51.5074" -F "lon=0.1278" -F "precision=5" http://localhost:8002/geohash
curl -X POST -F "geohash=<geohash>" http://localhost:8002/ungeohash
```

-----

## picoTTS API

### PicoTTS Container Build

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t darkflib/picotts-flask:latest --push .
```

### PicoTTS Container Usage

```bash
docker run -it -p 8001:8000 darkflib/picotts-flask:latest
```

### PicoTTS API Usage
```bash
curl -X POST -F "text=Hello, how are you?" -o output.wav http://localhost:8001/synthesize
```

-----

## Highlight API

### Highlight Container Build

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t darkflib/highlight-api:latest --push .
```

### Highlight Container Usage

```bash
docker run -it -p 8005:8000 darkflib/highlight-api:latest
```

### Highlight API Usage
```bash
curl -X POST -H "Content-type: application/json" http://localhost:8005/highlight -d
'{
    "code": "print('Hello World')",
    "language": "python",
    "style": "default", # todo
    "output_format": "html",
    "line_numbers": true, # todo
    "download": false # todo
}'
```
