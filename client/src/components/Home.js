import React from "react";
import { NavLink } from "react-router-dom";

function Home() {
    return (
        <div>
            <h1>Dashboard</h1>
            <p>Welcome to the AI-Assisted Travel Planner. Manage your trips, activities, and expenses seamlessly.</p>
            
            <section>
                <h2>Your Trips</h2>
                <p>Access your upcoming trips, plan new ones, and manage details.</p>
                <NavLink to="/trips">View Trips</NavLink>
            </section>

            <section>
                <h2>Plan Activities</h2>
                <p>Use AI to generate personalized activities for your trips.</p>
                <NavLink to="/trip/:id/activities">Plan Activities</NavLink>
            </section>

            <section>
                <h2>Manage Expenses</h2>
                <p>Track and split expenses among travelers for seamless cost sharing.</p>
                <NavLink to="/trip/:id/expenses">Manage Expenses</NavLink>
            </section>

            <section>
                <h2>Your Profile</h2>
                <p>Update your account settings and preferences.</p>
                <NavLink to="/profile">Go to Profile</NavLink>
            </section>
        </div>
    );
}

export default Home;
