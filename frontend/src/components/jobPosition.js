import React from "react";
function JobPosition() {
  return (
    <div>
      Job fields
      <br></br>
      <form action="http://localhost:5000" method="POST">
        <select name="jobField" className="jobs">
          <option id="choose" hidden>
            Choose a Position
          </option>
          <option value="projectManager">Project Manager</option>
          <option value="superintendent">Superintendent</option>
          <option value="chiefEstimator">Chief Estimator</option>
          <option value="projectEngineer">Project Engineer</option>
          <option value="projectCoordinator">Project Coordinator</option>
        </select>
      </form>
    </div>
  );
}
export default JobPosition;
