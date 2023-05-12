import "./App.css";
import React from "react";
import RecruiterOptions from "./components/recruiterOptions.js";
import LinkedinURL from "./components/urlSubmit.js";
import Header from "./components/header.js";

export default function App() {
  return (
    <div>
      <title>Sequoia Recruitment Tool</title>
      <body>
        <div className="container">
          <div className="container">
            <Header />
          </div>
          <div className="container">
            <div>
              <LinkedinURL />
            </div>
            <div>
              <RecruiterOptions />
            </div>
          </div>
        </div>
      </body>
    </div>
  );
}
