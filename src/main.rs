mod sliver_client;

use anyhow::Result;
use clap::Parser;
use sliver_client::{load_config, SliverClient};

#[derive(Parser, Debug)]
struct Args { 
    /// Path to sliver configuration file
    config_file: std::path::PathBuf
}

fn main() -> Result<()> {
    let args = Args::parse();

    // TODO: Automatically search for and load config file
    // TODO: Use rfd to prompt for config if != 1 found
    // TODO: Consider custom prompt instead of RFD?
    let config = load_config(args.config_file)?;
    println!("Loaded config for {}@{}:{}",
        config.operator,
        config.lhost,
        config.lport
    );

    let _session = SliverClient::from(config);

    // TODO: Create egui interface that can take in a 
    // Sliver client instance and invoke/respond to APIs
    // to perform actions and receive information
    Ok(())
}
