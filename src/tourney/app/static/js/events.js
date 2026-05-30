function submitEventForm() {

    const nameElement = document.getElementById("inputName")

    const data = {
        name: nameElement.value.trim(),
    };

    console.log("Sending data to Python Flask", data);

    // Send data to flask by using fetch.
    fetch('/api/createEvent', {
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

                console.log(data.message);
                window.location.reload();
            } else {
                // If response is not successful then output error.
                alert("Error: " + data.message);
            }
        })
}

function editEvent(id, name, ranks, multirank) {
    const editForm = document.getElementById("editEventForm");

    const editFormTableID = document.getElementById("tableEditEventForm-ID");
    const editFormTableName = document.getElementById("tableEditEventForm-Name");
    const editFormTableRanks = document.getElementById("tableEditEventForm-Ranks");
    const editFormTableMultiRanks = document.getElementById("tableEditEventForm-MultiRank");

    editForm.classList.add("visible");

    const ranksList = JSON.parse(ranks)

    editFormTableID.textContent = id;
    editFormTableName.textContent = name;
    editFormTableRanks.textContent =  ranksList.join(", ")
    editFormTableMultiRanks.textContent = multirank;
}

function submitEditEventForm() {
    const nameElement = document.getElementById("inputEditName");

    const eventID = document.getElementById("tableEditEventForm-ID");

    const data = {
        eventID: eventID.textContent,
        name: nameElement.value.trim(),
    }

    fetch('/api/editEvent', {
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
                document.getElementById("editEventForm").classList.remove("visible");
                window.location.reload();
            } else {
                // Else print error.
                alert("Error: " + data.message);
            }
        })
}

function submitDeleteEventForm() {
    const eventID = document.getElementById("tableEditEventForm-ID");
    const eventName = document.getElementById("tableEditEventForm-Name");

    const data = {
        eventID: eventID.textContent,
        name: eventName.textContent
    }

    fetch('/api/deleteEvent', {
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
                document.getElementById("editEventForm").classList.remove("visible");
                window.location.reload();
            } else {
                // Else print error.
                alert("Error: " + data.message);
            }
        })
}








function saveEvents() {
    fetch('/api/saveEvents', {
        method: 'POST',
    })
}