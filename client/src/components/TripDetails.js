import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

function TripDetail() {
    const { id } = useParams(); // Get the trip ID from the URL
    const [trip, setTrip] = useState(null);
    const [activities, setActivities] = useState([]);
    const [expenses, setExpenses] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Fetch trip details
        fetch(`http://127.0.0.1:5555/trips/${id}`)
            .then((response) => response.json())
            .then((data) => {
                setTrip(data);
                setActivities(data.activities || []);
                setExpenses(data.expenses || []);
                setLoading(false);
            })
            .catch((error) => {
                console.error("Error fetching trip details:", error);
                setLoading(false);
            });
    }, [id]);

    if (loading) {
        return <p>Loading trip details...</p>;
    }

    if (!trip) {
        return <p>Trip not found!</p>;
    }

    return (
        <div>
            <h1>{trip.name}</h1>
            <p>Destination: {trip.destination}</p>
            <p>Start Date: {trip.start_date}</p>
            <p>End Date: {trip.end_date}</p>

            <h2>Activities</h2>
            {activities.length > 0 ? (
                <ul>
                    {activities.map((activity) => (
                        <li key={activity.id}>
                            <strong>{activity.name}</strong>
                            <p>{activity.description}</p>
                            <p>Location: {activity.location}</p>
                            <p>Time: {new Date(activity.time).toLocaleString()}</p>
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No activities added yet.</p>
            )}

            <h2>Expenses</h2>
            {expenses.length > 0 ? (
                <ul>
                    {expenses.map((expense) => (
                        <li key={expense.id}>
                            <strong>{expense.description || "No Description"}</strong>
                            <p>Amount: ${expense.amount.toFixed(2)}</p>
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No expenses recorded yet.</p>
            )}
        </div>
    );
}

export default TripDetail;
