import React from "react";
export default function Locations({ setLocations }) {
  const handleLocationChange = (event) => {
    setLocations(event.target.value);
  };
  return (
    <div>
      <div className="textTitle">Insert State or City (OPTIONAL)</div>
      <form>
        <input
          className="textbox textbox2"
          placeholder="Illinois/Chicago"
          type="text"
          name="location"
          onChange={handleLocationChange}
        ></input>
      </form>
    </div>
  );
}
