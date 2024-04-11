use clap::Parser;
use tonic::transport::Channel;

use remotive_broker::{
    check_license,
    remotive_api::base::{
        network_service_client::NetworkServiceClient, system_service_client::SystemServiceClient,
        ClientId, NameSpace, SignalId, SignalIds, SubscriberConfig,
    },
};

use std::vec::Vec;

/// Rust subscribe example
#[derive(Parser, Debug)]
#[command(about)]
struct Args {
    /// Namespace
    #[arg(short, long, required = true)]
    namespace: String,

    #[arg(short, long, required = true)]
    signal: Vec<String>,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let channel = Channel::from_static("http://localhost:50051")
        .connect()
        .await?;

    let mut system_stub = SystemServiceClient::new(channel.clone());
    let mut network_stub = NetworkServiceClient::new(channel);

    check_license(&mut system_stub).await?;

    let signals = SignalIds {
        signal_id: args
            .signal
            .iter()
            .map(|name| SignalId {
                name: name.to_string(),
                namespace: Some(NameSpace {
                    name: args.namespace.to_string(),
                }),
            })
            .collect(),
    };

    let client_id = ClientId {
        id: "rusty_subscrib_example".to_string(),
    };

    let subscriber_config = SubscriberConfig {
        client_id: Some(client_id),
        signals: Some(signals),
        on_change: false,
    };

    println!("Waiting for signals...");

    let mut result = network_stub
        .subscribe_to_signals(subscriber_config.clone())
        .await?
        .into_inner();

    while let Some(next_message) = result.message().await? {
        println!("Received {:#?}", next_message.signal);
    }

    Ok(())
}
