use crate::sliver_client::SliverClient;

pub struct Interface {
    session: SliverClient,
}

impl Interface {
    // Take in a connection to the Sliver server
    // This is our conduit from the GUI to the "real world"
    // Using this, we can have callbacks in the interface run actions on the session
    // Conversely, we can fetch information from the session
    pub fn from_session(session: SliverClient) -> Self {
        Self { session }
    }

    pub fn update(&mut self, ctx: &egui::Context) {
        egui::CentralPanel::default().show(&ctx, |ui| {
            // Hello world, but with SliverClient integration PoC
            let text = format!("Hello, operator {}", &self.session.get_operator());
            ui.label(text);
        });
    }
}
