use crate::sliver_client::SliverSession;

pub struct Interface {
    session: SliverSession,
    version: String
}

impl Interface {
    // Take in a connection to the Sliver server
    // This is our conduit from the GUI to the "real world"
    // Using this, we can have callbacks in the interface run actions on the session
    // Conversely, we can fetch information from the session
    pub fn from_session(session: SliverSession) -> Self {
        Self { 
            session,
            version: "???".to_string()
        }
    }

    pub fn update(&mut self, ctx: &egui::Context) {
        egui::CentralPanel::default().show(&ctx, |ui| {
            // Hello world, but with SliverClient integration PoC
            let text = format!("Hello, operator {}", &self.session.get_operator());
            ui.label(text);
            let text = format!("Connected to {}:{}, version={}", 
                &self.session.config.lhost, 
                &self.session.config.lport,
                &self.version
            );
            ui.label(text);

            if ui.button("Version test").clicked() {
                self.version = self.session.get_version().unwrap_or("ERR".to_string());
            }

            if ui.button("Update agents").clicked() { 
                if let Ok((beacons, sessions)) = self.session.update_agents() { 
                    for beacon in beacons {
                        println!("Got beacon {:?}", beacon);
                    }

                    for session in sessions { 
                        println!("Got session {:?}", session);
                    }
                }
            }
        });
    }
}
