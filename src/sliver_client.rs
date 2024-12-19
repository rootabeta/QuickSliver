use anyhow::Result;
use serde::Deserialize;
use std::fs;
use std::path::PathBuf;

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
pub struct SliverClient {
    config: Config,
}

// TODO: Implement gRPC over mTLS connection with Tonic
// TODO: Implement Sliver client functionality from gRPC files
// TODO: Expose APIs to invoke gRPC functionality from GUI on-demand
// TODO: Expose APIs to fetch information from internal state, updated by server
impl SliverClient { 
    pub fn from(config: Config) -> Self { 
        Self { 
            config
        }
    }
}
