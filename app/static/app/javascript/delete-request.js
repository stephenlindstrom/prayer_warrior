const deleteButtons = document.querySelectorAll(".delete-button");
const noButtons = document.querySelectorAll(".no-button");
const addAnsweredPrayerButtons = document.querySelectorAll(".answered-prayer-button");
const cancelButtons = document.querySelectorAll(".cancel-button");

deleteButtons.forEach((deleteButton) => {
    const val = deleteButton.value;
    const deleteModal= document.querySelector("#delete-" + val);
    deleteButton.addEventListener("click", () => {
        deleteModal.style.display = "block";
    })
})


addAnsweredPrayerButtons.forEach((addAnsweredPrayerButton) => {
    const val = addAnsweredPrayerButton.value;
    const addAnsweredPrayerModal = document.querySelector("#add-answer-" + val);
    addAnsweredPrayerButton.addEventListener("click", () => {
        addAnsweredPrayerModal.style.display = "block";
    })
})

noButtons.forEach((noButton) => {
    const val = noButton.value;
    const deleteModal = document.querySelector("#delete-" + val);
    noButton.addEventListener("click", () => {
        deleteModal.style.display = "none";
    })
})

cancelButtons.forEach((cancelButton) => {
    const val = cancelButton.value;
    const addAnsweredPrayerModal = document.querySelector("#add-answer-" + val);
    cancelButton.addEventListener("click", () => {
        addAnsweredPrayerModal.style.display = "none";
    })
})