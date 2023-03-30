# RemotiveLabs WEB-GRPC Stubs

These are generated grpc-web stubs to be used in a browser context, not intended
to bu used with nodejs, read more here https://github.com/grpc/grpc-web

## RemotiveLabs

For more info visit https://remotivelabs.com or https://github.com/remotivelabs


## Usage

### Installation
```
npm install remotivelabs-grpc-web-stubs
or
yarn add remotivelabs-grpc-web-stubs
```

### Import
```
import {SystemServiceClient} from 'remotivelabs-grpc-web-stubs'

const client = new SystemServiceClient(brokerUrl)

```

# Build from source 

## Build grpc-web-generator

This image is on dockerhub so you do not have to build it
```
docker build -t remotivelabs/grpc-web-generator .
```

## Generate stubs

From this directory

### Typescript

```sh
sh ./generate-ts.sh
```

### Javascript

```sh
sh ./generate-js.sh
```

