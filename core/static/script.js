function startVoiceInput() {
  alert("🎤 Voice input feature coming soon!");
}

document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("accessibilityToggle");
  if (toggle) {
    toggle.addEventListener("change", () => {
      document.body.style.background = toggle.checked ? "#000" : "#f4f4f4";
      document.body.style.color = toggle.checked ? "#fff" : "#000";
    });
  }
});

// After successful login
localStorage.setItem("username", document.getElementById("name").value);
