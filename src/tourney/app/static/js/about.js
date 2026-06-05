
function debug() {

    const data = {
        message: "Debugging"
    }

    fetch('/api/debug', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
}