function appendStatus(message) {
  const output = document.getElementById("statusOutput");
  output.innerText += `[${new Date().toLocaleTimeString()}] ${message}\n`;
  output.scrollTop = output.scrollHeight;
}

function startPlayback() {
  const screenshots = document.getElementById("screenshotToggle").checked;
  appendStatus("Starting playback...");

  fetch("http://localhost:8080/start-playback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ screenshots: screenshots }),
  })
    .then((res) => res.text())
    .then((msg) => {
      appendStatus(msg);
      document.getElementById("spinner").style.display = "none";
      document.getElementById("nowPlaying").innerText = "🎞️ Now Playing...";
    })
    .catch((err) => appendStatus("Error: " + err));

  document.getElementById("spinner").style.display = "block";
}

function stopPlayback() {
  fetch("http://localhost:8080/stop", { method: "POST" })
    .then((res) => res.text())
    .then((msg) => appendStatus(msg))
    .catch((err) => appendStatus("Error: " + err));
}

function viewLogs() {
  fetch("http://localhost:8080/logs")
    .then((res) => res.json())
    .then((logs) => {
      appendStatus("---- Video Logs ----");
      logs.forEach((log) => {
        appendStatus(`${log.timestamp}: ${log.video_title}`);
      });
    })
    .catch((err) => appendStatus("Error: " + err));
}

function toggleDarkMode() {
  const body = document.body;
  const isDark = body.classList.toggle("dark-mode");
  localStorage.setItem("darkMode", isDark);
}

function setInitialTheme() {
  const prefersDark = localStorage.getItem("darkMode") === "true";
  if (prefersDark) {
    document.body.classList.add("dark-mode");
  } else {
    document.body.classList.remove("dark-mode");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  setInitialTheme();
  document
    .getElementById("darkModeToggle")
    .addEventListener("click", toggleDarkMode);
});

function saveToLocalFolder() {
  const input = document.getElementById("videoUpload");
  const statusOutput = document.getElementById("statusOutput");
  const spinner = document.getElementById("spinner");

  spinner.style.display = "block";

  if (input.files.length === 0) {
    statusOutput.innerText = "No file selected.";
    spinner.style.display = "none";
    return;
  }

  const fileArray = Array.from(input.files).map((f) => f.name);
  statusOutput.innerText =
    "Please manually move selected files to the 'videos' folder:";
  fileArray.forEach((file) => {
    statusOutput.innerText += `\n• ${file}`;
  });

  spinner.style.display = "none";
}

function uploadVideos() {
  const input = document.getElementById("videoUpload");
  const statusOutput = document.getElementById("statusOutput");
  const spinner = document.getElementById("spinner");

  if (input.files.length === 0) {
    statusOutput.innerText = "No video selected.";
    return;
  }

  spinner.style.display = "block";
  appendStatus("Uploading videos...");

  const formData = new FormData();
  for (const file of input.files) {
    formData.append("videos[]", file);
  }

  fetch("http://localhost:8080/upload", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.text())
    .then((msg) => {
      appendStatus(msg);
      spinner.style.display = "none";
    })
    .catch((err) => {
      appendStatus("Error: " + err);
      spinner.style.display = "none";
    });
}
