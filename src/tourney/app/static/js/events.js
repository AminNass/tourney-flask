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
                nameElement.value = "";

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

    const allowMultipleRanksEditForm = document.getElementById("inputEditAllowMultipleRanks");

    editForm.classList.add("visible");

    const rankDic = JSON.parse(ranks);
    const ranksList = Object.keys(rankDic);

    editFormTableID.textContent = id;
    editFormTableName.textContent = name;
    editFormTableRanks.textContent =  ranksList.join(", ")
    editFormTableMultiRanks.textContent = multirank;

    document.getElementById("rankPointsInputContainer").innerHTML = "";

    allowMultipleRanksEditForm.checked = (multirank.toLowerCase() === "true");

    // Loop through dictionary and append matching pairs as inputs
    for (const [rank, points] of Object.entries(rankDic)) {
        addRankPointRow(rank, points);
    }
}

function submitEditEventForm() {
    const nameElement = document.getElementById("inputEditName");
    const eventID = document.getElementById("tableEditEventForm-ID");
    const allowMultipleRanks = document.getElementById("inputEditAllowMultipleRanks");

    // Scrape inputs from all remaining active row nodes
    const rowElements = document.querySelectorAll(".rank-point-row");
    const updatedRankPoints = {};

    rowElements.forEach(row => {
        const rankKey = row.querySelector(".input-rank-key").value.trim();
        const pointsValue = parseInt(row.querySelector(".input-rank-points").value.trim(), 10);

        if (rankKey !== "") {
            updatedRankPoints[rankKey] = isNaN(pointsValue) ? 0 : pointsValue;
        }
    });

    const data = {
        eventID: eventID.textContent,
        name: nameElement.value.trim(),
        rankPoints: updatedRankPoints,
        allowMultipleRanks: allowMultipleRanks.checked,
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

function addRankPointRow(rankKey = '', pointsValue = '') {
    const container = document.getElementById("rankPointsInputContainer");

    // Create a raw structural div wrapper for this row
    const rowDiv = document.createElement("div");
    rowDiv.className = "rank-point-row";

    // Create the raw text inputs
    const rankInput = document.createElement("input");
    rankInput.type = "text";
    rankInput.className = "input-rank-key";
    rankInput.placeholder = "Rank";
    rankInput.value = rankKey;

    const pointsInput = document.createElement("input");
    pointsInput.type = "number";
    pointsInput.className = "input-rank-points";
    pointsInput.placeholder = "Points";
    pointsInput.value = pointsValue;

    // Create a raw text removal button
    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.textContent = "Remove";
    removeBtn.onclick = function() {
        container.removeChild(rowDiv);
    };

    // Assemble the elements sequentially
    rowDiv.appendChild(rankInput);
    rowDiv.appendChild(pointsInput);
    rowDiv.appendChild(removeBtn);
    container.appendChild(rowDiv);
}






function saveEvents() {
    fetch('/api/saveEvents', {
        method: 'POST',
    })
}