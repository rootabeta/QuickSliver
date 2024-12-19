use anyhow::Result;
use serde::Deserialize;
use std::fs;
use std::path::PathBuf;

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

// TODO: Implement gRPC over mTLS connection with Tonic
// TODO: Implement Sliver client functionality from gRPC files
// TODO: Expose APIs to invoke gRPC functionality (async) from GUI
impl Config {
}
