import React, { useState } from "react";

function ActivityPlanner() {
    const [destination, setDestination] = useState("");
    const [duration, setDuration] = useState(3);
    const [interests, setInterests] = useState("");
    const [itinerary, setItinerary] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleGenerateItinerary = () => {
        setLoading(true);
        setError("");
        setItinerary("");

        fetch(`/generate-itinerary?destination=${destination}&duration=${duration}&interests=${interests}`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to generate itinerary");
                }
                return response.json();
            })
            .then((data) => {
                if (data.itinerary) {
                    setItinerary(data.itinerary);
                } else {
                    setError("Could not generate itinerary. Please try again.");
                }
            })
            .catch((err) => setError(err.message))
            .finally(() => setLoading(false));
    };

    return (
        <div>
            <h1>Activity Planner</h1>
            <div>
                <label>
                    Destination:
                    <input
                        type="text"
                        value={destination}
                        onChange={(e) => setDestination(e.target.value)}
                        placeholder="Enter destination"
                    />
                </label>
            </div>
            <div>
                <label>
                    Duration (days):
                    <input
                        type="number"
                        value={duration}
                        onChange={(e) => setDuration(e.target.value)}
                        min="1"
                        max="7"
                    />
                </label>
            </div>
            <div>
                <label>
                    Interests:
                    <input
                        type="text"
                        value={interests}
                        onChange={(e) => setInterests(e.target.value)}
                        placeholder="e.g., food, museums, hiking"
                    />
                </label>
            </div>
            <button onClick={handleGenerateItinerary} disabled={loading}>
                {loading ? "Generating..." : "Generate Itinerary"}
            </button>

            {error && <p style={{ color: "red" }}>{error}</p>}
            {itinerary && (
                <div>
                    <h2>Generated Itinerary</h2>
                    <pre>{itinerary}</pre>
                </div>
            )}
        </div>
    );
}

export default ActivityPlanner;
