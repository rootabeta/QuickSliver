mod sliver_client;
mod sliver_ui;

use anyhow::Result;
use clap::Parser;
use sliver_client::{load_config, SliverClient};
use sliver_ui::Interface;

#[derive(Parser, Debug)]
struct Args {
    /// Path to sliver configuration file
    config_file: std::path::PathBuf,
}

fn main() -> Result<()> {
    let args = Args::parse();

    // TODO: Automatically search for and load config file
    // TODO: Use rfd to prompt for config if != 1 found
    // TODO: Consider custom prompt instead of RFD?
    let config = load_config(args.config_file)?;
    println!(
        "Loaded config for {}@{}:{}",
        config.operator, config.lhost, config.lport
    );

    println!(
        "Establishing connection to {}:{}",
        config.lhost, config.lport
    );

    let session = SliverClient::from(config);
    session.connect()?;

    // Instantiate GUI wrapper around our now armed-and-ready connection
    let native_options = eframe::NativeOptions::default();
    let mut application = Interface::from_session(session);

    // Launch GUI and allow operator to take control
    println!("Connection established, starting user interface");
    println!("Happy hunting!");
    match eframe::run_simple_native("QuickSliver", native_options, move |ctx, _frame| {
        application.update(ctx)
    }) {
        Ok(_) => Ok(()),
        Err(reason) => panic!("Fatal error: {reason}"),
    }
}
