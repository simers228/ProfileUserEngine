import React from "react";

export default function JobPositions(props) {
  const handleJobPositionChange = (event) => {
    props.setJobPosition(event.target.value);
  };

  return (
    <div>
      <div className="textTitle">Job Position</div>
      <form>
        <select
          className="textbox selection"
          name="jobPosition"
          onChange={handleJobPositionChange}
        >
          <option hidden>Choose a Position</option>
          <option value="project Manager">Project Manager</option>
          <option value="Super Intendent">Superintendent</option>
          <option value="Chief Estimator">Chief Estimator</option>
          <option value="Project Engineer">Project Engineer</option>
          <option value="Project Coordinator">Project Coordinator</option>
        </select>
      </form>
    </div>
  );
}
