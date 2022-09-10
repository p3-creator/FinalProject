// this is for type (i.e. hospital or doctor) of pharmacy registration


// const menu = document.querySelector(".select-menu"),
//  select = menu.querySelector(".select-btn"),
//   options =menu.querySelectorAll(".option"),
//   selected = menu.querySelector(".selected");

//   select.addEventListener("click", ()=> {
//     menu.classList.toggle("active");
// });

//   options.forEach(option => {
//         option.addEventListener("click", () => {
//             let selectedoption = option.querySelector(".option-text").innerText;
//             //  selected.innerHTML = a.querySelector("label").innerHTML;
//              selected.innerText = selectedoption
//              optionsContainer.classList.remove("active");
//          });
//      });



const selected = document.querySelector(".selected");
const optionsContainer = document.querySelector(".options-container");
const optionsList = document.querySelectorAll(".option");

selected.addEventListener("click", ()=> {
    optionsContainer.classList.toggle("active");
});

optionsList.forEach(a => {
    a.addEventListener("click", () => {
        selected.innerHTML = a.querySelector("label").innerHTML;
        optionsContainer.classList.remove("active");
    });
});