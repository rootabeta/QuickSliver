use crate::sliver_client::SliverSession;
use egui_extras::Column;

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

            // Table of beacons/sessions
            egui_extras::TableBuilder::new(ui)
                .column(Column::auto().resizable(true))
                .column(Column::auto().resizable(true))
                .header(20.0, |mut header| { 
                    header.col(|ui| { 
                        ui.heading("Name");
                    });
                    header.col(|ui| { 
                        ui.heading("Remote Address");
                    });
                })
                .body(|mut body| { 
                    for session in &self.session.sessions { 
                        body.row(30.0, |mut row| { 
                            row.col(|ui| { 
                                ui.label(&session.name);
                            });
                            row.col(|ui| {
                                ui.label(&session.remote_address);
                            });
                        })
                    }
                });

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
