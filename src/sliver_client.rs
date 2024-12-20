use anyhow::Result;
use serde::Deserialize;
use std::fs;
use std::path::PathBuf;

/// Struct to read in values from Sliver client config file
/* TODO: This disables warning for dead code, specifically fields
 * like private_key or ca_certificate which will be used to open an mTLS
 * connection to the C2 server. These will be used in the future, but for now,
 * they just need to hang out and look pretty until I implement the client/server
 * communications stack. Once I do, dead code warnings will be re-enabled.
 * This comment is here to remind me to do just that. */
#[allow(dead_code)]
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
    // Will contain a session to communicate over, with
    // structs for beacons, sessions, loot, messages, etc.
    // - each subcomponent exposing its own functions, such as
    // let interactive_session = SliverClient::Beacons::get(beacon_id).go_interactive();
}

// TODO: Implement gRPC over mTLS connection with Tonic
// TODO: Implement Sliver client functionality from gRPC files
// TODO: Expose APIs to invoke gRPC functionality from GUI on-demand
// TODO: Expose APIs to fetch information from internal state, updated by server
impl SliverClient {
    pub fn from(config: Config) -> Self {
        Self { config }
    }

    /// Activate the connection to the server
    pub fn connect(&self) -> Result<()> {
        // Skeleton code, will later house mTLS negotation and write back
        // opened connection to struct for use
        Ok(())
    }

    // Basic PoC to demonstrate getting values from config/session -> GUI
    pub fn get_operator(&self) -> &str {
        &self.config.operator
    }
}
