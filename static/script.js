
init();

function init() {
    initEventListeners();
}

function initEventListeners() {

    const addForm = document.getElementById("expenseForm");
    addForm.addEventListener("submit", async function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        const response = await fetch("/add", {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            addItemToExpensesTable(result);
            addForm.reset();
        }
    });


    document.querySelectorAll('button.delete-btn').forEach((item) => {
        item.addEventListener('click', async function (event) {
            let id = event.target.getAttribute('id');
            const response = await fetch("/delete/" + id, {
                method: "POST",
            });
            if (response.ok) {
                event.target.closest('tr').style.display = 'none';
            }
        })
    });
}

function addItemToExpensesTable(expenseDetails) {

    const table = document.querySelector('table');
    const row = document.createElement('tr');

    for (let item in expenseDetails) {

        if (item === 'actions') {
            let column = document.createElement('td');
            let btnDelete = document.createElement('button');
            btnDelete.textContent = 'Delete';
            btnDelete.classList.add('delete-btn');
            btnDelete.setAttribute('id', expenseDetails[item]);
            column.appendChild(btnDelete);
            row.append(column);
        }
        else {
            let column = document.createElement('td');
            column.textContent = expenseDetails[item];
            row.append(column);
        }
    }
    table.append(row);
}