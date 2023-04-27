import React from "react";
function JobPosition() {
  return (
    <select name="jobField" className="center dropdown">
      <option id="choose" hidden>
        Choose a Position
      </option>
      <option value="projectManager">Project Manager</option>
      <option value="superintendent">Superintendent</option>
    </select>
  );
}
export default JobPosition;
