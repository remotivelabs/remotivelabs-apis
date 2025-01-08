use remotivelabs_broker::{
    generated::base::{ClientId, NameSpace, SignalId, SignalIds, SubscriberConfig},
    Connection,
};
use std::{thread, time};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut con = Connection::new("http://localhost:50051".to_string(), None).await?;

    println!("Checking license...");
    con.check_license().await?;
    println!("Uploading configuration...");
    con.upload_folder("examples/configuration").await?;
    println!("Reloading configuration...");
    con.reload_configuration().await?;

    let client_id = Some(ClientId {
        id: "rusty_subscriber".to_string(),
    });

    let signals = generate_signal_ids("VirtualInterface", &["virtual_signal"]);

    let subscriber_config = SubscriberConfig {
        client_id,
        signals,
        on_change: true,
        initial_empty: false,
    };

    // Read message from stream and print it out
    loop {
        let mut result = con
            .network_stub
            .subscribe_to_signals(subscriber_config.clone())
            .await?
            .into_inner();

        while let Some(next_message) = result.message().await? {
            println!("Received {:#?}", next_message.signal);
        }

        {
            println!("Subscription dropped, retrying");
            let duration = time::Duration::from_secs(1);
            thread::sleep(duration);
        }
    }
}

/// generate signal ids for subscribe config
fn generate_signal_ids(namespace: &str, signals: &[&str]) -> Option<SignalIds> {
    let generate_namespace = |namespace: &str| {
        Some(NameSpace {
            name: namespace.to_string(),
        })
    };

    let signal_id = signals
        .iter()
        .map(|name| SignalId {
            name: name.to_string(),
            namespace: generate_namespace(namespace),
        })
        .collect::<Vec<SignalId>>();

    Some(SignalIds { signal_id })
}
