async function uploadResume() {
    const fileInput = document.getElementById("resumeFile");
    if (!fileInput.files.length) {
        alert("Please select a file!");
        return;
    }

    let formData = new FormData();
    formData.append("resume", fileInput.files[0]);

    try {
        let response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData
        });

        let data = await response.json();
        document.getElementById("parsedData").innerText = 
            `Name: ${data.name}, Skills: ${data.skills.join(", ")}`;
    } catch (error) {
        console.error("Error uploading file:", error);
    }
}
