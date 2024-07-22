const deleteButtons = document.querySelectorAll(".delete-button");
const modal = document.querySelector("#deleteModal");
const noButton = document.querySelector("#no-button");

deleteButtons.forEach((deleteButton) => {
    deleteButton.addEventListener("click", () => {
        modal.style.display = "block";
    })
})

noButton.addEventListener("click", () => {
    modal.style.display = "none";
})