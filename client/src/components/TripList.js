import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const TripList = () => {
  const [trips, setTrips] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch trips from the API
    fetch("http://127.0.0.1:5555/trips")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch trips");
        }
        return response.json();
      })
      .then((data) => setTrips(data))
      .catch((err) => setError(err.message));
  }, []);

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (trips.length === 0) {
    return <div>Loading trips...</div>;
  }

  return (
    <div>
      <h1>Your Trips</h1>
      <ul>
        {trips.map((trip) => (
          <li key={trip.id}>
            <Link to={`/trip/${trip.id}`}>
              {trip.name} - {trip.destination} ({trip.start_date} to {trip.end_date})
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TripList;
