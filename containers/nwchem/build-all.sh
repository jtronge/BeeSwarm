#!/bin/sh
# VERSIONS="tags/v6.8-release tags/v7.0.0-release tags/v7.0.1-release tags/v7.0.2-release"
VERSIONS="1411fef7b73acebb9451b0345fcd3fd8159d20a3"
CH_IMAGE_USERNAME=jtronge
CH_IMAGE_PASSWORD=87217eb0-758f-413e-aead-ad17f148bde8

for version in $VERSIONS; do
	# tag=jtronge/nwchem:`echo $version | cut -d'/' -f2`
	tag=jtronge/nwchem:$version
	ch-image build --force -t $tag --build-arg VERSION=$version .
	ch-image push $tag
	# ch-image reset
done
