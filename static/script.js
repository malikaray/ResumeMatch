// Job description character counter
const jobDescription = document.getElementById("job-description");
const characterCount = document.getElementById("character-count");

if (jobDescription && characterCount) {
    jobDescription.addEventListener("input", function () {
        characterCount.textContent =
            jobDescription.value.length + " characters";
    });
}

const deleteForms = document.querySelectorAll(".delete-form");

deleteForms.forEach(function (form) {
    form.addEventListener("submit", function (event) {
        const confirmed = confirm("Are you sure you want to delete this job?");

        if (!confirmed) {
            event.preventDefault();
        }
    });
});