# RemotiveBroker WEB-GRPC API

`remotivelabs-grpc-web-stubs` - Javascript SDK for interacting with the RemotiveBroker API in a browser context. Not intended to be used
with NodeJS.

Published to npm on [https://www.npmjs.com/package/remotivelabs-grpc-web-stubs](https://www.npmjs.com/package/remotivelabs-grpc-web-stubs).

## Getting started

```bash
cd grpc-web/grpc-web-stubs

# install dependencies
yarn install

# TODO
```

## Building

```bash
cd grpc-web/grpc-web-stubs

# Build docker image
docker build -t remotivelabs/grpc-web-generator .

# Generate typescript
./generate-ts.sh

# Generate javascript
./generate-js.sh
```

## Versioning

Versioning is done using `npm version`, see [Publishing](#publishing).

Follow [Semantic versioning](https://semver.org/). Beta versions should be suffixed with `-beta*`, example `0.2.0-beta1`.

## Publishing

Published to npm on [https://www.npmjs.com/package/remotivelabs-grpc-web-stubs](https://www.npmjs.com/package/remotivelabs-grpc-web-stubs).

```bash
# generate stubs
./generate-ts.sh

# update version
npm version x.y.z

# commit version
git add .
git commit -m "release: Prepare a release for version x.y.z"

# publish
npm publish
```
