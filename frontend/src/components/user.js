import React from "react";
export default function Domain({ setUser }) {
  const handleDomainChange = (event) => {
    setUser(event.target.value);
  };
  return (
    <div>
      <div className="textTitle">Insert User</div>
      <form>
        <input
          className="textbox"
          placeholder="Calvin"
          type="text"
          name="domain"
          onChange={handleDomainChange}
        ></input>
      </form>
    </div>
  );
}
