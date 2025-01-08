use clap::Parser;
use std::error::Error;
use std::fmt;

use remotivelabs_broker::{
    generated::base::{ClientId, NameSpace, SignalId, SignalIds, SubscriberConfig},
    Connection,
};

use std::vec::Vec;

/// Rust subscribe example
#[derive(Parser, Debug)]
#[command(about, version)]
struct Args {
    /// Subscribe to signals. Use syntax [namespace]:[frame.signal or signal].
    #[arg(short, long, required = true)]
    signal: Vec<String>,

    /// RemotiveBroker URL
    #[arg(short, long, default_value_t = String::from("http://localhost:50051"))]
    url: String,

    /// API key is required when accessing brokers running in the cloud
    #[arg(short, long)]
    x_api_key: Option<String>,
}

#[derive(Debug)]
struct ParseSignalError {
    identifier: String,
}

impl fmt::Display for ParseSignalError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Failed to parse signal '{}'", self.identifier)
    }
}

impl Error for ParseSignalError {}

fn parse_signal(identifier: &String) -> Result<SignalId, Box<dyn Error>> {
    if let Some((namespace, signal)) = identifier.split_once(":") {
        Ok(SignalId {
            name: signal.to_string(),
            namespace: Some(NameSpace {
                name: namespace.to_string(),
            }),
        })
    } else {
        let err = ParseSignalError {
            identifier: identifier.to_string(),
        };
        Err(Box::<dyn Error>::from(err))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();

    let signal_ids: Vec<SignalId> = args
        .signal
        .iter()
        .map(parse_signal)
        .collect::<Result<_, _>>()?;

    let mut con = Connection::new(args.url, args.x_api_key.clone()).await?;

    con.check_license().await?;

    let client_id = ClientId {
        id: "rusty_subscrib_example".to_string(),
    };

    let subscriber_config = SubscriberConfig {
        client_id: Some(client_id),
        signals: Some(SignalIds {
            signal_id: signal_ids,
        }),
        on_change: false,
        initial_empty: false,
    };

    println!("Waiting for signals...");

    let mut result = con
        .network_stub
        .subscribe_to_signals(subscriber_config.clone())
        .await?
        .into_inner();

    while let Some(next_message) = result.message().await? {
        println!("Received {:#?}", next_message.signal);
    }

    Ok(())
}
