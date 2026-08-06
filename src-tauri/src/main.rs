// Prevent additional console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::Manager;
use tauri_plugin_shell::process::CommandEvent;
use tauri_plugin_shell::ShellExt;

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .setup(|app| {
            // Cartella dati scrivibile (fuori da Program Files, dove l'app non ha
            // permessi di scrittura). Il backend Python deve leggere questa
            // variabile d'ambiente per decidere dove salvare database.sqlite e le
            // immagini, invece di usare un percorso relativo "data/".
            let app_data_dir = app
                .path()
                .app_data_dir()
                .expect("impossibile ottenere la cartella dati dell'app");

            std::fs::create_dir_all(&app_data_dir)
                .expect("impossibile creare la cartella dati dell'app");

            let data_dir_str = app_data_dir.to_string_lossy().to_string();

            // Avvia il backend FastAPI impacchettato (vedi backend/sidecar_entry.py
            // + PyInstaller) come processo "sidecar" gestito da Tauri.
            let sidecar_command = app
                .shell()
                .sidecar("promptarchive-backend")
                .expect("impossibile creare il comando sidecar (controlla il nome del binario)")
                .env("PROMPTARCHIVE_DATA_DIR", data_dir_str)
                .env("PROMPTARCHIVE_HOST", "127.0.0.1")
                .env("PROMPTARCHIVE_PORT", "8000");

            let (mut rx, _child) = sidecar_command
                .spawn()
                .expect("impossibile avviare il backend sidecar");

            // Inoltra i log del backend Python alla console per debug
            tauri::async_runtime::spawn(async move {
                while let Some(event) = rx.recv().await {
                    match event {
                        CommandEvent::Stdout(line) => {
                            print!("[backend] {}", String::from_utf8_lossy(&line));
                        }
                        CommandEvent::Stderr(line) => {
                            eprint!("[backend:err] {}", String::from_utf8_lossy(&line));
                        }
                        _ => {}
                    }
                }
            });

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("errore durante l'esecuzione dell'app Tauri");
}
