mod interceptor;
mod sliver_client;
mod sliver_ui;

use anyhow::Result;
use clap::Parser;
use sliver_client::{Config, SliverSession};
use sliver_ui::Interface;

#[derive(Parser, Debug)]
struct Args {
    /// Path to sliver configuration file
    config_file: std::path::PathBuf,
}

fn main() -> Result<()> {
    let args = Args::parse();

    // TODO: Use select_config instead of load_config to allow dynamic selection
    let config = Config::from(args.config_file)?;
    println!(
        "Loaded config for {}@{}:{}",
        config.operator, config.lhost, config.lport
    );

    println!(
        "Establishing connection to {}:{}",
        config.lhost, config.lport
    );

    let session = SliverSession::connect(config)?;

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
