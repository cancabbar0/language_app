document.getElementById("quizButton").addEventListener("click", function () {
    window.location.href = "http://localhost:8000/language_app/quiz/"; // Buraya gitmek istediğiniz URL'yi yazın
});

document.getElementById("addWordButton").addEventListener("click", function () {
    window.location.href = "http://localhost:8000/language_app/add_word/"; // Buraya gitmek istediğiniz URL'yi yazın
});

document.getElementById("settingsButton").addEventListener("click", function () {
    window.location.href = "http://localhost:8000/language_app/settings/"; // Buraya gitmek istediğiniz URL'yi yazın
});

document.getElementById("logoutButton").addEventListener("click", function () {
    window.location.href = "http://localhost:8000/logout/"; // Buraya gitmek istediğiniz URL'yi yazın
});

document.getElementById("analyzeReportButton").addEventListener("click", function () {
    window.location.href = "http://localhost:8000/language_app/analyze_report/"; // Buraya gitmek istediğiniz URL'yi yazın
});
