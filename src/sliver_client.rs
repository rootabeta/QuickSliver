use anyhow::Result;
use rpcpb::sliver_rpc_client::SliverRpcClient;
use serde::Deserialize;
use std::fs;
use std::path::PathBuf;
use tokio::runtime::Runtime;
use tonic::transport::{Certificate, Channel, ClientTlsConfig, Identity};

pub mod commonpb {
    tonic::include_proto!("commonpb");
}

pub mod clientpb {
    tonic::include_proto!("clientpb");
}

pub mod sliverpb {
    tonic::include_proto!("sliverpb");
}

pub mod rpcpb {
    tonic::include_proto!("rpcpb");
}

/// Struct to read in values from Sliver client config file
#[derive(Debug, Deserialize)]
pub struct Config {
    pub operator: String,
    pub lhost: String,
    pub lport: u16,
    token: String,
    ca_certificate: String,
    private_key: String,
    certificate: String,
}

/// Given a configuration file, return a Config object
pub fn load_config(file: PathBuf) -> Result<Config> {
    let config_contents = fs::read_to_string(file)?;
    let config: Config = serde_json::from_str(&config_contents)?;
    Ok(config)
}

/// Struct to handle Sliver session from a config file.
/// Includes generator to take in a config file,
/// log into the server, and perform commands.
/// Handles commands coming in from gRPC by updating internal state,
/// which can then be referenced elsewhere by accessing the state
pub struct SliverSession {
    config: Config,
    runtime: Runtime,
    session: SliverRpcClient<Channel>, //    channel: Channel,
}

// TODO: Expose APIs to invoke gRPC functionality from GUI on-demand
// TODO: Expose APIs to fetch information from internal state, updated by server
/*
    let request = tonic::Request::new(GreetRequest {
        name: "Tim".into(),
    });

    let response = client.say_hello(request).await?;
    println!("Response: {:?}", response);
*/
impl SliverSession {
    // Create a session from a configuration file
    pub fn connect(config: Config) -> Result<Self> {
        let runtime = Runtime::new().expect("Failed to open runtime");

        let ca_cert = Certificate::from_pem(&config.ca_certificate);
        let client_cert = Certificate::from_pem(&config.certificate);
        let client_key = Certificate::from_pem(&config.private_key);
        let client_identity = Identity::from_pem(client_cert, client_key);

        let tls = ClientTlsConfig::new()
            .domain_name("multiplayer")
            .ca_certificate(ca_cert)
            .identity(client_identity);

        let connection_string = format!("https://{}:{}", &config.lhost, &config.lport);
        let channel = Channel::from_shared(connection_string)?.tls_config(tls)?;

        // Open handle to runtime and order channel to connect
        let handle = runtime.handle();
        let channel = handle.block_on(async { channel.connect().await })?;
        let session = SliverRpcClient::new(channel);

        Ok(Self {
            config,
            runtime,
            session,
        })
    }

    // Basic PoC to demonstrate getting values from config/session -> GUI
    pub fn get_operator(&self) -> &str {
        &self.config.operator
    }
}
