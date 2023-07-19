# build all the docker images

DH_USER = "darkflib"
IMAGES = "geohash-api highlight-api markdown-api mermaid-api picotts-api"

for image in $IMAGES; do
    echo "Building $image\n"
    docker buildx build --platform linux/amd64,linux/arm64 -t $DH_USER/$image $image --push
done

