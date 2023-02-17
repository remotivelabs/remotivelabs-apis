# RemotiveLabs WEB-GRPC Stubs

For more info visit https://remotivelabs.com or https://github.com/remotivelabs

These are generated grpc-web stubs to be used in a browser context, not intended
to bu used with nodejs.

## Usage

### Installation
```
npm install remotivelabs-grpc-web
or
yarn add remotivelabs-grpc-web
```

### Import
```
import {SystemServiceClient} from 'remotivelabs-grpc-web'

const client = new SystemServiceClient(brokerUrl)

```

# Build from source 

## Build grpc-web-generator

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

