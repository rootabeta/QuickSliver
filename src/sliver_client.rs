use crate::interceptor::TokenAuthInterceptor;
use anyhow::Result;
use rpcpb::sliver_rpc_client::SliverRpcClient;
use serde::Deserialize;
use std::fs;
use std::path::PathBuf;
use tokio::runtime::Runtime;
use tonic::service::interceptor::InterceptedService;
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
impl Config {
    pub fn from(file: PathBuf) -> Result<Self> {
        let config_contents = fs::read_to_string(file)?;
        let config: Config = serde_json::from_str(&config_contents)?;
        Ok(config)
    }

    pub fn get_token(&self) -> String {
        self.token.clone()
    }
}

/// Struct to handle Sliver session from a config file.
/// Includes generator to take in a config file,
/// log into the server, and perform commands.
/// Handles commands coming in from gRPC by updating internal state,
/// which can then be referenced elsewhere by accessing the state
pub struct SliverSession {
    pub config: Config,
    runtime: Runtime,
    // I'm sorry for the typing mess here
    session: SliverRpcClient<InterceptedService<Channel, TokenAuthInterceptor>>,
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

        // Emulate Go's PerRPCCredentials system with a custom interceptor
        let interceptor = TokenAuthInterceptor::new(config.get_token());

        // Open handle to runtime and order channel to connect
        let handle = runtime.handle();
        let channel = handle.block_on(async { channel.connect().await })?;

        // Make the session using the authenticator-attached channel, instead of the raw one
        //        let session = SliverRpcClient::new(intercepted_channel);
        let session = SliverRpcClient::with_interceptor(channel, interceptor);

        Ok(Self {
            config,
            runtime,
            session,
        })
    }

    pub fn get_version(&mut self) -> Result<String> {
        let execution_handle = self.runtime.handle();
        let version_request = tonic::Request::new(commonpb::Empty {});
        let response =
            execution_handle.block_on(async { self.session.get_version(version_request).await })?;
        println!("Got response {:?}", response);
        let major = response.get_ref().major;
        let minor = response.get_ref().minor;
        let patch = response.get_ref().patch;
        let version: String = format!("{}.{}p{}", major, minor, patch);
        Ok(version)
    }

    // Basic PoC to demonstrate getting values from config/session -> GUI
    pub fn get_operator(&self) -> &str {
        &self.config.operator
    }
}
