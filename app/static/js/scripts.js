const colors = ["green", "blue", "yellow"];
const randomColor = colors[Math.floor(Math.random() * colors.length)];
const elements = document.querySelectorAll(".randomcolor");
elements.forEach((element) => {
  const randomColor = colors[Math.floor(Math.random() * colors.length)];
  element.style.color = randomColor;
});

let timerDuration = 10;
let currentTime = timerDuration;
const interval = 1000;
const timerBar = document.getElementById("timerBar");
const totalWidth = timerBar.parentElement.offsetWidth;
let timerInterval;
let selectedButton1 = null;
let selectedButton2 = null;

const shopElement = document.getElementById("emosi-data");
const shopName = shopElement.getAttribute("data-name");
const shopLocation = shopElement.getAttribute("data-location");
let jenisEmosi = shopName; // Tambahkan ini di awal agar bisa diakses

function runConfetti() {
  const canvas = document.getElementById("confetti");
  var colors = [
    "#bb0000",
    "#ffffff",
    "#00FF00",
    "#0000FF",
    "#FFFF00",
    "#00FFFF",
  ];
  setTimeout(() => {
    confetti({
      particleCount: 200,
      angle: 60,
      spread: 100,
      origin: { x: 0 },
      ticks: 350,
      colors: colors,
      gravity: 2.2,
    });
    confetti({
      particleCount: 200,
      angle: 120,
      spread: 100,
      origin: { x: 1 },
      ticks: 350,
      colors: colors,
      gravity: 2.2,
    });
  }, 200);
}

function updateTimer() {
  currentTime--;
  const timerWidth = (currentTime / timerDuration) * totalWidth;
  timerBar.style.width = timerWidth + "px";

  if (currentTime > 6) {
    timerBar.style.backgroundColor = "#30FF2B";
  } else if (currentTime > 3) {
    timerBar.style.backgroundColor = "orange";
  } else {
    timerBar.style.backgroundColor = "red";
  }

  if (currentTime <= 0) {
    clearInterval(timerInterval);
    timerBar.style.backgroundColor = "red";
    if (jenisEmosi === "emosi-gabungan") {
      showFeedbackGabungan("Gagal, waktu habis", "belum berhasil");
    } else {
      showFeedback(
        "Gagal, waktu habis",
        "/static/img/emoji/jawabansalah.png",
        "belum berhasil"
      );
    }
  }
}

function showFeedback(message, imageUrl, statusLatihan) {
  document.getElementById("katajawaban").innerText = message;
  document.getElementById("emojijawaban").src = imageUrl;
  document.getElementById("statuslatihan").value = statusLatihan;
  new bootstrap.Modal(document.getElementById("feedbackModal")).show();
}

function showFeedbackGabungan(message, statusLatihan) {
  document.getElementById("katajawaban").innerText = message;
  document.getElementById("statuslatihan").value = statusLatihan;
  new bootstrap.Modal(document.getElementById("feedbackModal")).show();
}

function checkEmosi(button) {
  console.log("diklik");
  if (selectedButton2) return;

  button.classList.add("flipped");

  if (!selectedButton1) {
    selectedButton1 = button;
  } else {
    selectedButton2 = button;
    const emotion1 = selectedButton1.getAttribute("data-emotion");
    const emotion2 = selectedButton2.getAttribute("data-emotion");
    const namaEmosi = shopLocation;

    if (emotion1 === namaEmosi && emotion2 === namaEmosi) {
      setTimeout(() => {
        clearInterval(timerInterval);
        if (jenisEmosi === "emosi-gabungan") {
          runConfetti();
          showFeedbackGabungan("Berhasil", "berhasil");
        } else {
          runConfetti();
          showFeedback(
            "Wah, jawaban kamu sempurna!",
            "/static/img/emoji/jawabanbenar.png",
            "berhasil"
          );
        }
        selectedButton1 = null;
        selectedButton2 = null;
      }, 1000);
    } else {
      setTimeout(() => {
        selectedButton1.classList.remove("flipped");
        selectedButton2.classList.remove("flipped");
        selectedButton1 = null;
        selectedButton2 = null;
      }, 1000);
    }
  }
}

window.onload = () => {
  const welcomeModal = new bootstrap.Modal(
    document.getElementById("welcomeModal")
  );
  welcomeModal.show();

  document.getElementById("startButton").addEventListener("click", () => {
    timerBar.style.width = totalWidth + "px";
    currentTime = timerDuration;
    timerInterval = setInterval(updateTimer, interval);
  });
};
