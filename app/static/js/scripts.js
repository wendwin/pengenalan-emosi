// const colors = ["green", "blue", "yellow", "green", "blue", "yellow"];
// const colors = [
//   "#ffa500",
//   "#faeb36",
//   "#79c314",
//   "#487de7",
//   "#4b369d",
//   "#70369d",
// ];
// const randomColor = colors;
// const elements = document.querySelectorAll(".randomcolor");

// for (var i = 0; i < colors.length; i++) {
//   elements[i].style.color = colors[i];
//   elements[i].style.fontweight = "bold";
//   elements[i].style.fontsize = "30px";
// }

document.addEventListener("DOMContentLoaded", function () {
  if (!sessionStorage.getItem("modalShown")) {
    setTimeout(function () {
      var modalInfo = new bootstrap.Modal(document.getElementById("modalInfo"));
      modalInfo.show();

      // localStorage.setItem("modalShown", "true");
      sessionStorage.setItem("modalShown", "true");
    }, 2000);
  }
});

setTimeout(function () {
  // Jika belum pernah, tampilkan modal setelah 3 detik
  var myModal = new bootstrap.Modal(document.getElementById("myModal"));
  myModal.show();

  // Simpan status modal ke local storage agar tidak muncul lagi
  localStorage.setItem("modalShown", "true");
}, 3000); // Waktu tunggu 3 detik (3000 ms)

let timerDuration = 10;
let currentTime = timerDuration;
const interval = 1000;
const timerBar = document.getElementById("timerBar");
const totalWidth = timerBar.parentElement.offsetWidth;
let timerInterval;
let selectedButton1 = null;
let selectedButton2 = null;

const emosiData = document.getElementById("emosi-data");
const dataName = emosiData.getAttribute("data-name");
const emosi = emosiData.getAttribute("data-location");
let jenisEmosi = dataName;

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

  if (currentTime <= 0)
    setTimeout(() => {
      clearInterval(timerInterval);
      timerBar.style.backgroundColor = "red";
      if (jenisEmosi === "Gabungan") {
        showFeedbackGabunganSalah(
          "Gagal, waktu habis",
          "/static/img/emoji/jawabansalah.png",
          "belum berhasil"
        );
      } else {
        showFeedback(
          "Gagal, waktu habis",
          "/static/img/emoji/jawabansalah.png",
          "belum berhasil"
        );
      }
    }, 1000);
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
  document.getElementById("emojijawaban").classList.add("d-none");
  document.getElementById("emosigabungan").classList.remove("d-none");
  new bootstrap.Modal(document.getElementById("feedbackModal")).show();
}
function showFeedbackGabunganSalah(message, imageUrl, statusLatihan) {
  document.getElementById("katajawaban").innerText = message;
  document.getElementById("emojijawaban").src = imageUrl;
  document.getElementById("statuslatihan").value = statusLatihan;
  document.getElementById("emojijawaban").classList.remove("d-none");
  document.getElementById("emosigabungan").classList.add("d-none");
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
    const namaEmosi = emosi;

    if (emotion1 === namaEmosi && emotion2 === namaEmosi) {
      clearInterval(timerInterval);
      setTimeout(() => {
        if (jenisEmosi === "Gabungan") {
          runConfetti();
          showFeedbackGabungan("Wah, jawaban kamu sempurna!", "berhasil");
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
