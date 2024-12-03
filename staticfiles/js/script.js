document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("menuToggle");
    const sidebar = document.querySelector(".sidebar");
    const mainContent = document.querySelector(".main-content");

    toggleButton.addEventListener("click", function () {
        sidebar.classList.toggle("open");
        document.body.classList.toggle("sidebar-open");
    });
});
