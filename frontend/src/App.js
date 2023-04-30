import "./App.css";
import React from "react";
import JobPosition from "./components/jobPosition.js";
import ButtonUse from "./components/buttonUse.js";
import Header from "./components/header.js";
import Locations from "./components/locations.js";

export default function App() {
  return (
    <div className="flex">
      <title>Sequoia Recruitment Tool</title>
      <body>
        <div className="container">
          <Header />
        </div>
        <div className="container">
          <ButtonUse />
        </div>
        <div className="container">
          <JobPosition />
        </div>
        <div className="container">
          <Locations />
        </div>
      </body>
    </div>
  );
}
