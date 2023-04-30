import React from "react";
function Locations() {
  return (
    <div className="center textbox">
      Insert Linkedin URL
      <form action="http://localhost:5000" method="POST">
        <input
          placeholder="Illinois/Chicago"
          type="text"
          name="linkedinUrl"
        ></input>
        <input type="submit" value="Submit"></input>
      </form>
    </div>
  );
}

export default Locations;
