import "./App.css";
import JobPosition from "./components/jobPosition.js";
import ButtonUse from "./components/buttonUse.js";
import React from "react";

export default function App() {
  return (
    <div className="center">
      <body>
        <div id="linkedin">
          Insert Linkedin URL
          <ButtonUse />
        </div>
        <div>
          Job Field
          <br></br>
          <JobPosition />
        </div>
      </body>
    </div>
  );
}
