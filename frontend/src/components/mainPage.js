import React from "react";
import RecruiterOptions from "./mainPage/recruiterOptions.js";
import LinkedinURL from "./mainPage/urlSubmit.js";
export default function MainPage() {
  return (
    <div>
      <div className="container">
        <div>
          <LinkedinURL />
        </div>
        <div>
          <RecruiterOptions />
        </div>
      </div>
    </div>
  );
}
