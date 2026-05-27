// Submit member form
function submitMemberForm() {

    // Get the HTML input elements
    const usernameElement = document.getElementById("inputUsername");
    const firstnameElement = document.getElementById("inputFirstname");
    const lastnameElement = document.getElementById("inputLastname");

    // Creating an object so it can be sent clearly
    const data = {
        username: usernameElement.value.trim(),
        firstname: firstnameElement.value.trim(),
        lastname: lastnameElement.value.trim(),
    };

    console.log("Sending data to Python Flask", data);

    // Send data to flask by using fetch.
    fetch('/api/createMember', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            // Get response from flask.
            return response.json();
        })
        .then(data => {
            // Check if response says success
            if (data.status === "success") {
                usernameElement.value = "";
                firstnameElement.value = "";
                lastnameElement.value = "";

                console.log(data.message);
                window.location.reload();
            } else {
                // If response is not successful then output error.
                alert("Error: " + data.message);
            }
        })
}

// EditUser

function editMember(id, username, firstname, lastname) {
    const editForm = document.getElementById("editMemberForm");

    const editFormTableID = document.getElementById("tableEditMemberForm-ID");
    const editFormTableUsername = document.getElementById("tableEditMemberForm-Username");
    const editFormTableFirstname = document.getElementById("tableEditMemberForm-Firstname");
    const editFormTableLastname = document.getElementById("tableEditMemberForm-Lastname");

    editForm.classList.add("visible");

    editFormTableID.textContent = id
    editFormTableUsername.textContent = username
    editFormTableFirstname.textContent = firstname
    editFormTableLastname.textContent = lastname
}

// Change information
function submitEditMemberForm() {
    const usernameElement = document.getElementById("inputEditUsername");
    const firstnameElement = document.getElementById("inputEditFirstname");
    const lastnameElement = document.getElementById("inputEditLastname");

    const memberID = document.getElementById("tableEditMemberForm-ID");

    const data = {
        memberID: memberID.textContent,
        username: usernameElement.value.trim(),
        firstname: firstnameElement.value.trim(),
        lastname: lastnameElement.value.trim(),
    }

    console.log("Sending data to Python Flask", data);

    fetch('/api/editMember', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            // get response from flask.
            return response.json();
        })
        .then(data => {
            // If successful then:
            if (data.status === "success") {
                console.log(data.message);
                document.getElementById("editMemberForm").classList.remove("visible");
                window.location.reload();
            } else {
                // Else print error.
                alert("Error: " + data.message);
            }
        })
}

// Delete Member

function deleteMember() {
    const memberID = document.getElementById("tableEditMemberForm-ID");
    const usernameElement = document.getElementById("tableEditMemberForm-Username");

    const data = {
        memberID: memberID.textContent,
        username: usernameElement.textContent
    }

    console.log("Sending data to Python Flask", data);

    fetch('/api/deleteMember', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            // get response from flask.
            return response.json();
        })
        .then(data => {
            // If successful then:
            if (data.status === "success") {
                console.log(data.message);
                document.getElementById("editMemberForm").classList.remove("visible");
                window.location.reload();
            } else {
                // Else print error.
                alert("Error: " + data.message);
            }
        })
}

function saveMembers() {
    fetch('/api/saveMembers', {
        method: 'POST',
    })
}

