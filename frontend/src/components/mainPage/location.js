import React from "react";
export default function Location({ setLocation }) {
  const handleLocationChange = (event) => {
    setLocation(event.target.value);
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
