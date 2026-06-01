 function openTourney(id) {
    window.location.href = "/tourney/manager/" + id;
 }

 function cancelChanges() {
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