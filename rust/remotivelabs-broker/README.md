# RemotiveLabs Broker
Rust library with gRPC-bindings and utility functions.

gRPC bindings are generated from [this source](../../proto/) when compiling the project.

This project is contributed by _Niclas Lind_ (@niclaslind).

## Publish / Subscribe example
See `examples/pub_client.rs` and `examples/sub_client.rs` for a sample on how to use the library.

These samples work together and will connect to a _RemotiveBroker_ running on `localhost`. The sample `sub_client.rs` will listen to the virtual network `VirtualInterface` configured in `interfaces.json` and the sample `pub_client.rs` send write messages on the same network. First start the subscription sample:

    cargo run --example sub_client

This will upload a configuration to the broker. The configuration directory is found [here](examples/configuration/).
Now the sample `sub_client` is running and waiting for signals. To produce signals run the next sample in a separate terminal:

    cargo run --example pub_client

Now follow the prompt instruction and input numbers. The numbers will be received and printed by the subscription sample.
