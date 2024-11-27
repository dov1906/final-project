import React from "react";
import App from "./components/App";
import ErrorPage from "./components/ErrorPage";
import Home from "./components/Home";
import TripList from "./components/TripList";
import TripDetails from "./components/TripDetails";
import ActivityPlanner from "./components/ActivityPlanner";
import AddActivityForm from "./components/AddActivityForm";
import ExpenseList from "./components/ExpenseList";
import Profile from "./components/Profile";
import BrowsePrice from './components/BrowsePrice';

const routes = [
    {
        path: "/",
        element: <App />,
        errorElement: <ErrorPage />,
        children: [
            { path: "/", element: <Home /> }, // Home route
            { path: "/trips", element: <TripList /> }, // List of trips
            { path: "/trip/:id", element: <TripDetails /> }, // Trip details
            { path: "/trip/:id/activities", element: <ActivityPlanner /> }, // Activities
            { path: "/trip/:id/add-activity", element: <AddActivityForm /> }, // Add activity
            { path: "/trip/:id/expenses", element: <ExpenseList /> }, // Expenses
            { path: "/profile", element: <Profile /> }, // Profile
            { path: "/browse-prices", element: <BrowsePrice /> },
        ],
    },
];

export default routes;
