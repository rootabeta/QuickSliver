use crate::sliver_client::SliverSession;

pub struct Interface {
    session: SliverSession,
}

impl Interface {
    // Take in a connection to the Sliver server
    // This is our conduit from the GUI to the "real world"
    // Using this, we can have callbacks in the interface run actions on the session
    // Conversely, we can fetch information from the session
    pub fn from_session(session: SliverSession) -> Self {
        Self { 
            session,
        }
    }


    pub fn update(&mut self, ctx: &egui::Context) {
        egui::CentralPanel::default().show(&ctx, |ui| {
            
            // Menubar
            egui::menu::bar(ui, |ui| { 
                /*    if ui.button("Version Test").clicked() {
                        self.version = self.session.
                            get_version()
                            .unwrap_or(
                                "ERR".to_string()
                            );
                    }
                */
                ui.menu_button("Connection", |_ui| {});
                ui.menu_button("Armory", |_ui| {});
                ui.menu_button("Listeners", |_ui| {});
                ui.menu_button("Profiles", |_ui| {});
                ui.menu_button("Generate", |_ui| {});
                ui.menu_button("Jobs", |_ui| {});
                ui.menu_button("Loot", |_ui| {});

            });

            // Workaround to prevent label wrapping
            ui.style_mut().wrap_mode = Some(egui::TextWrapMode::Extend);

            egui::Grid::new("agent_table").striped(true).show(ui, |ui| { 
                ui.label("Name");
                ui.label("Transport");
                ui.label("Username");
                ui.label("OS");
                ui.label("Last Checkin");
                ui.label("Next Checkin");
                ui.end_row();

                for beacon in &self.session.beacons { 
 //                   ui.label(&beacon.id);
                    ui.label(&beacon.name);
                    ui.label(&format!("{}://{}", 
                            &beacon.transport,
                            &beacon.remote_address));
                    ui.label(&format!("{}@{}",
                            &beacon.username,
                            &beacon.hostname));
                    ui.label(&beacon.os);
                    ui.label(&format!("{}", beacon.last_checkin));
                    ui.label(&format!("{}", beacon.next_checkin));
                    ui.end_row();
                }

                for session in &self.session.sessions { 
//                    ui.label(&session.id);
                    ui.label(&session.name);
                    ui.label(&format!("{}://{}", 
                            &session.transport,
                            &session.remote_address));
                    ui.label(&format!("{}@{}",
                            &session.username,
                            &session.hostname));
                    ui.label(&session.os);
                    ui.label(&format!("{}", session.last_checkin));
                    ui.label(match &session.is_dead { 
                        true => "[DEAD]",
                        false => "[ALIVE]"
                    });
                    ui.end_row();
                }
            });

            if ui.button("Update agents").clicked() { 
                if let Ok((_beacons, _sessions)) = self.session.update_agents() { 
                }
            }
        });
    }
}
