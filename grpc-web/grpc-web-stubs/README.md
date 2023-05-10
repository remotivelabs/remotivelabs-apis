# RemotiveLabs WEB-GRPC Stubs

[![npm version](https://img.shields.io/npm/v/remotivelabs-grpc-web-stubs.svg)](https://www.npmjs.com/package/remotivelabs-grpc-web-stubs)

These are generated grpc-web stubs to be used in a browser context, not intended
to bu used with nodejs, read more here https://github.com/grpc/grpc-web

## Usage

### Installation
```
npm install --save remotivelabs-grpc-web-stubs
```
or
```
yarn add remotivelabs-grpc-web-stubs
```

### Import
```
import {SystemServiceClient} from 'remotivelabs-grpc-web-stubs'

const client = new SystemServiceClient(brokerUrl)
```

## Development

### Build grpc-web-generator

This image is on dockerhub so you do not have to build it
```sh
docker build -t remotivelabs/grpc-web-generator .
```

### Generate stubs

From this directory run the following commands and update `src/index.ts` to explicitly export types.

```sh
sh ./generate-ts.sh
```
