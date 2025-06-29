function appendStatus(message) {
  const output = document.getElementById("statusOutput");
  output.innerText += `[${new Date().toLocaleTimeString()}] ${message}\n`;
  output.scrollTop = output.scrollHeight;
}

function startDownload() {
  const apiUrl = document.getElementById("apiUrl").value;
  fetch("/download", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ api_url: apiUrl }),
  })
    .then((res) => res.text())
    .then((msg) => appendStatus(msg))
    .catch((err) => appendStatus("Error: " + err));
}

function startPlayback() {
  const endTime = document.getElementById("endTime").value;
  const screenshots = document.getElementById("screenshotToggle").checked;
  fetch("/start-playback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ end_time: endTime, screenshots: screenshots }),
  })
    .then((res) => res.text())
    .then((msg) => appendStatus(msg))
    .catch((err) => appendStatus("Error: " + err));
  document.getElementById("spinner").style.display = "block";
  appendStatus("Starting playback...");
  fetch("/start-playback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ end_time: endTime, screenshots: screenshots }),
  })
    .then((res) => res.text())
    .then((msg) => {
      appendStatus(msg);
      document.getElementById("spinner").style.display = "none";
      document.getElementById("nowPlaying").innerText = "🎞️ Now Playing...";
    });
}

function stopPlayback() {
  fetch("/stop", { method: "POST" })
    .then((res) => res.text())
    .then((msg) => appendStatus(msg))
    .catch((err) => appendStatus("Error: " + err));
}

function viewLogs() {
  fetch("/logs")
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
  document.body.classList.toggle("dark-mode");
  // Optional: Save preference
  const isDark = document.body.classList.contains("dark-mode");
  localStorage.setItem("darkMode", isDark);
}

// Load preference on page load
window.onload = function () {
  if (localStorage.getItem("darkMode") === "true") {
    document.body.classList.add("dark-mode");
  }
};
