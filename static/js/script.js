document.addEventListener("DOMContentLoaded", () => {
    const optionsContainer = document.getElementById("options-container");
    const addOptionButton = document.getElementById("add-option");

  
    addOptionButton.addEventListener("click", () => {
        const optionRow = document.createElement("div");
        optionRow.classList.add("option-row");

        optionRow.innerHTML = `
            <input type="text" name="options[]" class="form-control" placeholder="Ex. Bleu" required />
            <button type="button" class="btn btn-danger btn-sm remove-option">−</button>
        `;

        optionsContainer.appendChild(optionRow);


        optionRow.querySelector(".remove-option").addEventListener("click", () => {
            optionRow.remove();
        });
    });


    optionsContainer.addEventListener("click", (event) => {
        if (event.target.classList.contains("remove-option")) {
            event.target.closest(".option-row").remove();
        }
    });
});
