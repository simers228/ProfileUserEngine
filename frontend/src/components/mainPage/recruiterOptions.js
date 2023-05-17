import React, { useState } from "react";
import Location from "./location.js";
import JobPositions from "./jobPositions.js";
import JobDescription from "./jobDescription";
import Domain from "./domain.js";

export default function RecruiterOptions() {
  const [jobPosition, setJobPosition] = useState("");
  const [location, setLocation] = useState("");
  const [domain, setDomain] = useState("");
  const [jobDescription, setJobDescription] = useState("");

  const handleJobPositionChange = (value) => {
    setJobPosition(value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!jobPosition || !jobDescription) {
      alert("Please fill out both Job Position and Job Description fields");
      return;
    }
    try {
      const requestBody = {
        jobPosition,
      };
      if (location) {
        requestBody.location = location;
      }
      if (jobDescription) {
        requestBody.jobDescription = jobDescription;
      }
      if (domain) {
        requestBody.domain = domain;
      }
      const response = await fetch("http://localhost:5000/recruiter", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Request-ID": "User-Input",
        },
        body: JSON.stringify(requestBody),
      });
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  };
  return (
    <div>
      <div className="prompts row">
        <div>
          <JobPositions setJobPosition={handleJobPositionChange} />
        </div>
        <div className="container2">
          <Location setLocation={setLocation} />
        </div>
        <div>
          <Domain setDomain={setDomain} />
        </div>
      </div>
      <div className="prompts">
        <JobDescription setJobDescription={setJobDescription} />
      </div>
      <div className="button2">
        <button id="filterButton" className="button" onClick={handleSubmit}>
          Submit
        </button>
      </div>
    </div>
  );
}
