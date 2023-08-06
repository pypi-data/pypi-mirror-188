# shopcloud-serverless-cli

Serverless API

## install

````sh
$ pip install shopcloud-serverless
````

## usage

```sh
$ serverless init
$ serverless gateway init
$ serverless services list
$ serverless services deploy hello_world
$ serverless gateway deploy
```

## services

Create a new service endpoint for every path.

```sh
$ serverless serverless services create hello_world
```

Add the Endpoint in the `api.yaml` the `operation_id`must be unqie and is the identifier for the library.
You can change the `<service-name>.yaml` with the parameters
- `memory`: memory in MB
- `runtime`: runtime of the function "python310"

for development you can use the [functions-framework](https://github.com/GoogleCloudPlatform/functions-framework-python)

```sh
$ functions-framework --source="hello_world.py" --target main --debug --port=8080
```

then deploy the function

```sh
$ serverless serverless services deploy hello_world
```

and then deploy the gateway

```sh
$ serverless gateway deploy
```
