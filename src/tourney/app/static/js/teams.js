function submitTeamForm() {

    const nameElement = document.getElementById("inputName")
    const iTeamCheck = document.getElementById("ITeamChecked")

    const data = {
        name: nameElement.value.trim(),
        iTeam: iTeamCheck.checked
    };

    console.log("Sending data to Python Flask", data);

    // Send data to flask by using fetch.
    fetch('/api/createTeam', {
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
                name.value = "";
                iTeamCheck.checked = false;

                console.log(data.message);
                window.location.reload();
            } else {
                // If response is not successful then output error.
                alert("Error: " + data.message);
            }
        })
}

function editTeam(id, name, members) {
    const editForm = document.getElementById("editTeamForm");

    const editFormTableID = document.getElementById("tableEditTeamForm-ID");
    const editFormTableName = document.getElementById("tableEditTeamForm-Name");
    const editFormTableMembers = document.getElementById("tableEditTeamForm-Members");

    const EditFormTableMemberSelect = document.getElementById("tableEditTeamForm-MemberList-Select");

    // Clear out old data in selection.
    EditFormTableMemberSelect.innerHTML = "";

    members.forEach((member) => {

        const option = document.createElement("option");

        option.text = member[1];
        option.value = member[0];

        EditFormTableMemberSelect.appendChild(option);
    })

    const memberUsernames = []

    for (const member of members) {
        memberUsernames.push(member[1]);
    }

    editForm.classList.add("visible");

    editFormTableID.textContent = id;
    editFormTableName.textContent = name;
    editFormTableMembers.textContent =  memberUsernames;
}

function submitEditTeamForm() {
    const nameElement = document.getElementById("inputEditName");

    const teamID = document.getElementById("tableEditTeamForm-ID");

    const data = {
        teamID: teamID.textContent,
        name: nameElement.value.trim(),
    }

    fetch('/api/editTeam', {
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
                document.getElementById("editTeamForm").classList.remove("visible");
                window.location.reload();
            } else {
                // Else print error.
                alert("Error: " + data.message);
            }
        })
}

function submitDeleteTeamForm() {
    const teamID = document.getElementById("tableEditTeamForm-ID");
    const teamName = document.getElementById("tableEditTeamForm-Name");

    const data = {
        teamID: teamID.textContent,
        name: teamName.textContent
    }

    fetch('/api/deleteTeam', {
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
                document.getElementById("editTeamForm").classList.remove("visible");
                window.location.reload();
            } else {
                // Else print error.
                alert("Error: " + data.message);
            }
        })
}

function submitRemoveMemberForm() {
    const teamID = document.getElementById("tableEditTeamForm-ID");

    const selectionBox = document.getElementById("tableEditTeamForm-MemberList-Select");
    const selectedMember = selectionBox.value;

    const editForm = document.getElementById("editTeamForm");

    const data = {
        teamID: teamID.textContent,
        memberID: selectedMember
    }

    fetch('/api/removeTeamMember', {
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
                window.location.reload();
            } else {
                // Else print error.
                alert("Error: " + data.message);
            }
        })
}

function submitAddMemberForm() {
    const inputUsernameElement = document.getElementById("inputAddMember");
    const teamID = document.getElementById("tableEditTeamForm-ID");

    const data = {
        teamID: teamID.textContent,
        username: inputUsernameElement.value.trim(),
    }

    fetch('/api/addTeamMember', {
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
                window.location.reload();
            } else {
                // Else print error.
                alert("Error: " + data.message);
            }
        })
}

function saveTeams() {
    fetch('/api/saveTeams', {
        method: 'POST',
    })
}