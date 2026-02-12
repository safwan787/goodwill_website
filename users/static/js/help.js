document.addEventListener("DOMContentLoaded", function () {
    const helpBtn = document.getElementById("help-btn");
    const helpBox = document.getElementById("help-box");
    const helpClose = document.getElementById("help-close");

    if (!helpBtn || !helpBox) return;

    helpBtn.addEventListener("click", function () {
        helpBox.style.display =
            helpBox.style.display === "block" ? "none" : "block";
    });

    if (helpClose) {
        helpClose.addEventListener("click", function () {
            helpBox.style.display = "none";
        });
    }

    // Close when clicking outside
    document.addEventListener("click", function (e) {
        if (!helpBox.contains(e.target) && !helpBtn.contains(e.target)) {
            helpBox.style.display = "none";
        }
    });
});
