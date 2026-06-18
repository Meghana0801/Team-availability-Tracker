async function loadUsers(){

    const response = await fetch('/users');
    const users = await response.json();

    const userList =
        document.getElementById('userList');

    userList.innerHTML = '';

    users.forEach(user => {

        userList.innerHTML += `
            <div class="card">

                <h3>${user.name}</h3>

                <p class="${
                    user.available
                    ? 'available'
                    : 'unavailable'
                }">

                    ${
                        user.available
                        ? 'Available'
                        : 'Unavailable'
                    }

                </p>

                <button
                onclick="toggleUser(${user.id})">
                    Toggle
                </button>

            </div>
        `;
    });
}

async function toggleUser(id){

    await fetch(`/toggle/${id}`, {
        method:'POST'
    });

    loadUsers();
}

loadUsers();