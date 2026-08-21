use std::net::TcpListener;
use std::path::PathBuf;
use std::process::{Child, Command};
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;
use tauri::{AppHandle, Manager, RunEvent, WebviewUrl, WebviewWindowBuilder};

/// Finds an available ephemeral port on the 127.0.0.1 loopback interface
fn find_free_port() -> u16 {
    TcpListener::bind("127.0.0.1:0")
        .and_then(|listener| listener.local_addr())
        .map(|addr| addr.port())
        .unwrap_or(8000)
}

/// Resolves the absolute path to the backend executable
fn resolve_sidecar_path(app: &AppHandle) -> PathBuf {
    // 1. Try bundled production binary
    if let Ok(resource_dir) = app.path().resource_dir() {
        let bundled_path = resource_dir
            .join("binaries")
            .join("labelsort-engine")
            .join(if cfg!(windows) { "labelsort-engine.exe" } else { "labelsort-engine" });
        if bundled_path.exists() {
            return bundled_path;
        }
    }

    // 2. Try development build in backend/dist/labelsort-engine/
    let dev_dist_path = PathBuf::from(r"..\backend\dist\labelsort-engine\labelsort-engine.exe");
    if dev_dist_path.exists() {
        return dev_dist_path;
    }

    // 3. Fallback to current executable directory
    let current_exe_dir = std::env::current_exe()
        .ok()
        .and_then(|p| p.parent().map(|p| p.to_path_buf()))
        .unwrap_or_else(|| PathBuf::from("."));
    
    current_exe_dir
        .join("labelsort-engine")
        .join(if cfg!(windows) { "labelsort-engine.exe" } else { "labelsort-engine" })
}

/// Polls the health check endpoint until the backend is fully responsive
fn wait_for_backend_ready(port: u16, max_attempts: u32) -> bool {
    let health_url = format!("http://127.0.0.1:{}/health/", port);
    let client = reqwest::blocking::Client::builder()
        .timeout(Duration::from_millis(500))
        .build()
        .unwrap_or_default();

    for _ in 0..max_attempts {
        if let Ok(resp) = client.get(&health_url).send() {
            if resp.status().is_success() {
                return true;
            }
        }
        thread::sleep(Duration::from_millis(100));
    }
    false
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let sidecar_holder = Arc::new(Mutex::new(None));
    let sidecar_setup = Arc::clone(&sidecar_holder);
    let sidecar_exit = Arc::clone(&sidecar_holder);

    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .setup(move |app| {
            let port = find_free_port();
            let parent_pid = std::process::id();
            let app_handle = app.handle();
            let sidecar_path = resolve_sidecar_path(app_handle);

            println!("[Tauri Supervisor] Starting sidecar on port {} (Parent PID: {})", port, parent_pid);
            println!("[Tauri Supervisor] Sidecar path: {:?}", sidecar_path);

            // Spawn the Python sidecar process
            let mut command = Command::new(&sidecar_path);
            command.arg("--port").arg(port.to_string());
            command.arg("--parent-pid").arg(parent_pid.to_string());

            #[cfg(windows)]
            {
                use std::os::windows::process::CommandExt;
                const CREATE_NO_WINDOW: u32 = 0x08000000;
                command.creation_flags(CREATE_NO_WINDOW);
            }

            match command.spawn() {
                Ok(child) => {
                    let mut lock = sidecar_setup.lock().unwrap();
                    *lock = Some(child);
                    println!("[Tauri Supervisor] Sidecar spawned successfully.");
                }
                Err(err) => {
                    eprintln!("[Tauri Supervisor] Failed to spawn sidecar: {:?}", err);
                }
            }

            // Wait for backend to be ready before displaying the webview
            let is_ready = wait_for_backend_ready(port, 50);
            if is_ready {
                println!("[Tauri Supervisor] Backend is ready and responding on port {}.", port);
            } else {
                eprintln!("[Tauri Supervisor] Warning: Backend did not respond to health check in time.");
            }

            // Inject the dynamic API URL into the React Webview context
            let api_url = format!("http://127.0.0.1:{}", port);
            let init_script = format!(
                "window.__LABELSORT_API_URL__ = '{}'; window.__LABELSORT_PORT__ = {};",
                api_url, port
            );

            WebviewWindowBuilder::new(app, "main", WebviewUrl::default())
                .title("LabelSort Pro")
                .inner_size(1280.0, 820.0)
                .min_inner_size(1024.0, 700.0)
                .center()
                .initialization_script(&init_script)
                .build()?;

            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("Error while building Tauri application")
        .run(move |_app_handle, event| {
            if let RunEvent::Exit = event {
                // Ensure Python sidecar child process is terminated cleanly
                if let Ok(mut lock) = sidecar_exit.lock() {
                    if let Some(mut child) = lock.take() {
                        println!("[Tauri Supervisor] Terminating sidecar child process on exit...");
                        let _ = child.kill();
                    }
                }
            }
        });
}
