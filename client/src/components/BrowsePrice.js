import React, { useState } from "react";

function BrowsePrice() {
    const [option, setOption] = useState(""); // Track if flight or hotel is selected
    const [formData, setFormData] = useState({
        cityName: "",
        checkin: "",
        checkout: "",
        rooms: 1,
        adults: 2,
        children: 0,
        departureAirport: "",
        arrivalAirport: "",
        departureDate: "",
        returnDate: "",
        passengers: 1,
        cabinClass: "Economy",
    });
    const [results, setResults] = useState(null);
    const [error, setError] = useState("");

    const handleOptionChange = (e) => {
        setOption(e.target.value);
        setResults(null); // Clear results when option changes
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setError("");
        setResults(null);

        if (option === "hotel") {
            fetch(
                `/api/get_hotels?city_name=${formData.cityName}&checkin=${formData.checkin}&checkout=${formData.checkout}&rooms=${formData.rooms}&adults=${formData.adults}&children=${formData.children}`
            )
                .then((response) => response.json())
                .then((data) => {
                    // Filter out only relevant hotel information
                    const formattedHotels = data.map((hotel) => ({
                        name: hotel.name,
                        price: hotel.price1 || hotel.price2 || "Not Available",
                        
                    }));
                    setResults(formattedHotels);
                })
                .catch(() => setError("Error fetching hotel data."));
        } else if (option === "flight") {
            fetch(
                `/api/roundtrip?departure_airport_code=${formData.departureAirport}&arrival_airport_code=${formData.arrivalAirport}&departure_date=${formData.departureDate}&arrival_date=${formData.returnDate}&number_of_adults=${formData.passengers}&cabin_class=${formData.cabinClass}`
            )
                .then((response) => response.json())
                .then((data) => {
                    // Filter out only relevant flight information
                    const formattedFlights = data.map((flight) => ({
                        departure: flight.departure,
                        arrival: flight.arrival,
                        price: flight.price || "Not Available",
                        duration: `${Math.floor(flight.duration_minutes / 60)}h ${flight.duration_minutes % 60}m`,
                        stops: flight.stops,
                    }));
                    setResults(formattedFlights);
                })
                .catch(() => setError("Error fetching flight data."));
        } else {
            setError("Please select an option.");
        }
    };

    return (
        <div>
            <h1>Browse Prices</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>
                        Select Option:
                        <select value={option} onChange={handleOptionChange}>
                            <option value="">-- Select --</option>
                            <option value="hotel">Hotel</option>
                            <option value="flight">Flight</option>
                        </select>
                    </label>
                </div>

                {option === "hotel" && (
                    <div>
                        <h2>Hotel Search</h2>
                        <label>
                            City Name:
                            <input
                                type="text"
                                name="cityName"
                                value={formData.cityName}
                                onChange={handleInputChange}
                                required
                            />
                        </label>
                        <label>
                            Check-in Date:
                            <input
                                type="date"
                                name="checkin"
                                value={formData.checkin}
                                onChange={handleInputChange}
                                required
                            />
                        </label>
                        <label>
                            Check-out Date:
                            <input
                                type="date"
                                name="checkout"
                                value={formData.checkout}
                                onChange={handleInputChange}
                                required
                            />
                        </label>
                        <label>
                            Rooms:
                            <input
                                type="number"
                                name="rooms"
                                value={formData.rooms}
                                onChange={handleInputChange}
                                min="1"
                                required
                            />
                        </label>
                        <label>
                            Adults:
                            <input
                                type="number"
                                name="adults"
                                value={formData.adults}
                                onChange={handleInputChange}
                                min="1"
                                required
                            />
                        </label>
                        <label>
                            Children:
                            <input
                                type="number"
                                name="children"
                                value={formData.children}
                                onChange={handleInputChange}
                                min="0"
                            />
                        </label>
                    </div>
                )}

                {option === "flight" && (
                    <div>
                        <h2>Flight Search</h2>
                        <label>
                            Departure Airport:
                            <input
                                type="text"
                                name="departureAirport"
                                value={formData.departureAirport}
                                onChange={handleInputChange}
                                required
                            />
                        </label>
                        <label>
                            Arrival Airport:
                            <input
                                type="text"
                                name="arrivalAirport"
                                value={formData.arrivalAirport}
                                onChange={handleInputChange}
                                required
                            />
                        </label>
                        <label>
                            Departure Date:
                            <input
                                type="date"
                                name="departureDate"
                                value={formData.departureDate}
                                onChange={handleInputChange}
                                required
                            />
                        </label>
                        <label>
                            Return Date:
                            <input
                                type="date"
                                name="returnDate"
                                value={formData.returnDate}
                                onChange={handleInputChange}
                                required
                            />
                        </label>
                        <label>
                            Passengers:
                            <input
                                type="number"
                                name="passengers"
                                value={formData.passengers}
                                onChange={handleInputChange}
                                min="1"
                                required
                            />
                        </label>
                        <label>
                            Cabin Class:
                            <select
                                name="cabinClass"
                                value={formData.cabinClass}
                                onChange={handleInputChange}
                            >
                                <option value="Economy">Economy</option>
                                <option value="Business">Business</option>
                                <option value="First">First</option>
                            </select>
                        </label>
                    </div>
                )}

                <button type="submit">Search</button>
            </form>

            {error && <p style={{ color: "red" }}>{error}</p>}

            {results && (
                <div>
                    <h2>Results</h2>
                    <ul>
                        {results.map((result, index) => (
                            <li key={index}>
                                <strong>{result.name || `Flight ${index + 1}`}</strong>
                                <p>Price: {result.price}</p>
                                {result.reviews && <p>Reviews: {result.reviews}</p>}
                                {result.duration && <p>Duration: {result.duration}</p>}
                                {result.stops !== undefined && <p>Stops: {result.stops}</p>}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default BrowsePrice;
