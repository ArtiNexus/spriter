use serde::{Deserialize, Serialize};
use std::io::BufRead;
use std::process::{Command, Stdio};
use tauri::{AppHandle, Emitter};

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct PipelineParams {
    pub image_path: String,
    pub actions: Vec<ActionItem>,
    pub settings: PipelineSettings,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct ActionItem {
    pub name: String,
    pub prompt: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct PipelineSettings {
    pub api_provider: String,
    pub api_key: String,
    pub api_url: Option<String>,
    pub fps: u32,
    pub frame_size: u32,
}

#[derive(Debug, Serialize, Clone)]
pub struct ProgressEvent {
    pub step: String,
    pub percent: u32,
    pub message: String,
}

#[tauri::command]
pub async fn run_pipeline(app: AppHandle, params: PipelineParams) -> Result<String, String> {
    let json_params = serde_json::to_string(&params).map_err(|e| e.to_string())?;
    let python_dir = std::env::current_dir()
        .unwrap_or_default()
        .parent()
        .map(|p| p.join("python"))
        .unwrap_or_default();

    let mut child = Command::new("python3")
        .arg(python_dir.join("pipeline.py"))
        .arg("--params")
        .arg(&json_params)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("启动 Python 失败: {}", e))?;

    let stdout = child.stdout.take().unwrap();
    let reader = std::io::BufReader::new(stdout);

    let mut result_path = String::new();

    for line in reader.lines() {
        let line = line.map_err(|e| e.to_string())?;
        if line.starts_with("PROGRESS:") {
            let parts: Vec<&str> = line[9..].splitn(2, ':').collect();
            if parts.len() == 2 {
                let percent: u32 = parts[0].parse().unwrap_or(0);
                let message = parts[1].to_string();
                let _ = app.emit("pipeline-progress", ProgressEvent {
                    step: format!("S{:02}", percent / 10),
                    percent,
                    message,
                });
            }
        } else if line.starts_with("COMPLETE:") {
            result_path = line[9..].to_string();
            let _ = app.emit("pipeline-complete", serde_json::json!({
                "zip_path": result_path,
                "frame_dir": std::env::temp_dir().join("sprite-maker").join("frames").to_string_lossy()
            }));
        } else if line.starts_with("ERROR:") {
            let msg = line[6..].to_string();
            let _ = app.emit("pipeline-error", serde_json::json!({ "message": msg }));
            return Err(msg);
        }
    }

    child.wait().map_err(|e| e.to_string())?;

    if result_path.is_empty() {
        Err("未收到完成信号".to_string())
    } else {
        Ok(result_path)
    }
}
