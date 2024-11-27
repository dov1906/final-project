import React, { useState} from "react";

function AddActivityForm({ currentTripId }) {
    const [formData, setFormData] = useState({
        activityName: "",
        description: "",
        location: "",
        time: "",
    });
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setError("");
        setSuccess("");

        if (!currentTripId) {
            setError("No trip selected. Please select a trip first.");
            return;
        }

        fetch(`http://127.0.0.1:5555/trips/${currentTripId}/activities`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name: formData.activityName,
                description: formData.description,
                location: formData.location,
                time: formData.time,
            }),
        })
            .then((response) => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error("Failed to add activity");
                }
            })
            .then(() => {
                setSuccess("Activity added successfully!");
                setFormData({
                    activityName: "",
                    description: "",
                    location: "",
                    time: "",
                });
            })
            .catch(() => setError("An error occurred while adding the activity."));
    };

    return (
        <div>
            <h1>Add New Activity</h1>
            {error && <p style={{ color: "red" }}>{error}</p>}
            {success && <p style={{ color: "green" }}>{success}</p>}
            <form onSubmit={handleSubmit}>
                <label>
                    Activity Name:
                    <input
                        type="text"
                        name="activityName"
                        value={formData.activityName}
                        onChange={handleInputChange}
                        required
                    />
                </label>
                <br />
                <label>
                    Description:
                    <textarea
                        name="description"
                        value={formData.description}
                        onChange={handleInputChange}
                        required
                    ></textarea>
                </label>
                <br />
                <label>
                    Location:
                    <input
                        type="text"
                        name="location"
                        value={formData.location}
                        onChange={handleInputChange}
                        required
                    />
                </label>
                <br />
                <label>
                    Time:
                    <input
                        type="datetime-local"
                        name="time"
                        value={formData.time}
                        onChange={handleInputChange}
                        required
                    />
                </label>
                <br />
                <button type="submit">Add Activity</button>
            </form>
        </div>
    );
}

export default AddActivityForm;
