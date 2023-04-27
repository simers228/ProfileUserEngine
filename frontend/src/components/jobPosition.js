import React from "react";
function JobPosition() {
  return (
    <div>
      Job fields
      <br></br>
      <select name="jobField" className="">
        <option id="choose" hidden>
          Choose a Position
        </option>
        <option value="projectManager">Project Manager</option>
        <option value="superintendent">Superintendent</option>
      </select>
    </div>
  );
}
export default JobPosition;
