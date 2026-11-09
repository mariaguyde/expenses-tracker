
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

        console.log(response);
        if (response.status == 200) {
            const result = await response.json();
            addItemToExpensesTable(result);
            addForm.reset();
        }
    });


    document.querySelectorAll('.delete-btn').forEach((item) => {
        item.addEventListener('click', async function (event) {
            let id = event.target.getAttribute('id');
            const response = await deleteRow(id);
            if (response.status == 200) 
                event.target.closest('tr').style.display = 'none';
            
        })
    });

    document.querySelector('.download-btn').addEventListener('click', function() {
        const overlay = document.querySelector('.overlay');
        const downloadForm = overlay.querySelector('#downloadForm');
        overlay.classList.add('overlay-visible');

        downloadForm.querySelector('.close-btn').addEventListener('click', function() {
            closedDownloadPopin();
        });

        downloadForm.querySelector('button').addEventListener('click', function() {
            closedDownloadPopin();
        });

    });
}

function addItemToExpensesTable(expenseDetails) {

    const table = document.querySelector('table tbody');
    const row = document.createElement('tr');

    for (let item in expenseDetails) {

        if (item === 'actions') { 
            let column = document.createElement('td');
            let imgDelete = document.createElement('img');
            imgDelete.src = '../static/assets/imgs/trash.svg';
            imgDelete.classList.add('icon-trash');
            imgDelete.classList.add('delete-btn');
            imgDelete.setAttribute('id', expenseDetails[item]);
            column.appendChild(imgDelete);
            row.append(column);
            imgDelete.addEventListener('click', async function() {
                const response = await deleteRow(expenseDetails[item]);
                if (response.status == 200)
                    row.style.display = 'none';
            });
        }
        else {
            let column = document.createElement('td');
            column.textContent = expenseDetails[item];
            row.append(column);
        }
    }
    table.append(row);
}

function closedDownloadPopin() {
    document.querySelector('.overlay').classList.remove('overlay-visible');
}

async function deleteRow(id) {
    return await fetch("/delete/" + id, {method: "POST"});
}