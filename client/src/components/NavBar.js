import React, { useState, useEffect } from "react";
import { NavLink, useNavigate } from "react-router-dom";

function NavBar() {
    const [currentTripId, setCurrentTripId] = useState(null);
    const [trips, setTrips] = useState([]);
    const navigate = useNavigate(); // For programmatic navigation

    useEffect(() => {
        // Fetch all trips from the backend
        fetch("http://127.0.0.1:5555/trips")
            .then((response) => response.json())
            .then((data) => setTrips(data))
            .catch((error) => console.error("Error fetching trips:", error));
    }, []);

    const handleTripSelection = (id) => {
        setCurrentTripId(id);
        if (id) {
            navigate(`/trip/${id}`); // Automatically navigate to the selected trip details
        }
    };

    return (
        <nav>
            <NavLink to="/">Home</NavLink>
            {currentTripId && (
                <>
                    <NavLink to={`/trip/${currentTripId}`}>Trip Details</NavLink>
                    <NavLink to={`/trip/${currentTripId}/activities`}>Activity Planner</NavLink>
                    <NavLink to={`/trip/${currentTripId}/add-activity`}>Add Activity</NavLink>
                    <NavLink to={`/trip/${currentTripId}/expenses`}>Expenses</NavLink>
                    <NavLink to="/browse-prices">Browse Prices</NavLink>
                </>
            )}
            <NavLink to="/profile">Profile</NavLink>

            {/* Dropdown to select a trip */}
            <div>
                <label htmlFor="trip-select">Select Trip:</label>
                <select
                    id="trip-select"
                    value={currentTripId || ""}
                    onChange={(e) => handleTripSelection(e.target.value)}
                >
                    <option value="">--Select a Trip--</option>
                    {trips.map((trip) => (
                        <option key={trip.id} value={trip.id}>
                            {trip.name}
                        </option>
                    ))}
                </select>
            </div>
        </nav>
    );
}

export default NavBar;
