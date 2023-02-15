# WEB-GRPC Stubs

**Important! Code is working but not yet fully packaged or documented**

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

## Usage in code

This is not an npm module yet so you will need to copy your generated-ts or generate-js
directories to your project.

```
import {SystemServiceClient} from './generated-ts/system_api_grpc_web_pb'
```

# TODO

* webpack
* npm module

