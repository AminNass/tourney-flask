function submitTourneyForm() {
    const nameElement = document.getElementById("inputName")

    const data = {
        name: nameElement.value.trim(),
    };

    console.log("Sending data to Python Flask", data);

    // Send data to flask by using fetch.
    fetch('/api/createTourney', {
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

function openTourney(id) {
    window.location.href = "/tourney/manager/" + id;
 }

 function Close() {
    window.location.href = "/tourneys";
 }

 function submitEventChanges(tourneyID, eventID) {
    const nameElement = document.getElementById("inputName-" + eventID);

    const data = {
        tourneyID: tourneyID,
        eventID: eventID,
        eventName: nameElement.value.trim(),
    }

    fetch('/api/changeTourneyEvent', {
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

 function updateStatus(tourneyID, eventID, status) {

    const data = {
        tourneyID: tourneyID,
        eventID: eventID,
        status: status
    }

    fetch('/api/changeTourneyEventStatus', {
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
                console.log(data.message);
                window.location.reload();
            } else {
                // If response is not successful then output error.
                alert("Error: " + data.message);
            }
        })
 }

 function getEventLength(tourneyID, eventID) {
   const timeElement = document.getElementById("timeBox-" + eventID);

   // Passing data inside the URL string using query parameters
   const url = `/api/getTourneyEventLength?tourneyID=${tourneyID}&eventID=${eventID}`;

   fetch(url, {
       method: 'GET'
   })
       .then(response => response.json())
       .then(data => {
           if (data.status === "success") {
               timeElement.textContent = data.message;
           } else {
               alert("Error: " + data.message);
           }
       })
       .catch(error => {
           console.error("Fetch error:", error);
       });
}

function submitAddTeam(tourneyID, eventID) {

    const teamNameElement = document.getElementById("inputTeam-" + eventID);

    const data = {
        tourneyID: tourneyID,
        eventID: eventID,
        teamName: teamNameElement.value.trim()
    }

    fetch('/api/addTeamToEventTourney', {
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
                console.log(data.message);
                window.location.reload();
            } else {
                // If response is not successful then output error.
                alert("Error: " + data.message);
            }
        })
}

function addRankToTeam(tourneyID, eventID) {

    const teamSelectionElement = document.getElementById("teamAddRank-" + eventID);
    const rankSelectionElement = document.getElementById("rankAddRank-" + eventID);

    const selectedTeam = teamSelectionElement.value;
    const selectedRank = rankSelectionElement.value;

    const data = {
        tourneyID: tourneyID,
        eventID: eventID,
        selectedTeam: selectedTeam,
        selectedRank: selectedRank
    }

    fetch('/api/AddRankToTeam', {
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
                console.log(data.message);
                window.location.reload();
            } else {
                // If response is not successful then output error.
                alert("Error: " + data.message);
            }
        })
}

function resetTeamPoints(tourneyID, eventID, teamID) {

    const data = {
        tourneyID: tourneyID,
        eventID: eventID,
        teamID: teamID
    }

    fetch('/api/resetTeamPointsForTourneyEvent', {
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
                console.log(data.message);
                window.location.reload();
            } else {
                // If response is not successful then output error.
                alert("Error: " + data.message);
            }
        })
}

function submitRemoveTeam(tourneyID, eventID) {

    const teamRemoveSelectionElement = document.getElementById("reamRemoveSelection-" + eventID);

    const data = {
        tourneyID: tourneyID,
        eventID: eventID,
        teamID: teamRemoveSelectionElement.value.trim()
    }

    fetch('/api/removeTeamFromTourneyEvent', {
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
                console.log(data.message);
                window.location.reload();
            } else {
                // If response is not successful then output error.
                alert("Error: " + data.message);
            }
        })
}

function addEventToTourney(tourneyID) {

    const inputEventNameElement = document.getElementById("inputAddEvent")
    const inputEventNewNameElement = document.getElementById("inputAddEventNewName")

    const data = {
        tourneyID: tourneyID,
        eventName: inputEventNameElement.value.trim(),
        eventNewName: inputEventNewNameElement.value.trim()
    }

    fetch('/api/addEventToTourney', {
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
                console.log(data.message);
                window.location.reload();
            } else {
                // If response is not successful then output error.
                alert("Error: " + data.message);
            }
        })
}

function deleteTourney(tourneyID) {

    const data = {
        tourneyID: tourneyID
    }

    fetch('/api/deleteTourney', {
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
                console.log(data.message);
                window.location.reload();
            } else {
                // If response is not successful then output error.
                alert("Error: " + data.message);
            }
        })
}

function saveTourneys() {
    fetch('/api/saveTourneys', {
        method: 'POST',
    })
}