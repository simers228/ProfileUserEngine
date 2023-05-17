import React from "react";
export default function Domain({ setDomain }) {
  const handleDomainChange = (event) => {
    setDomain(event.target.value);
  };
  return (
    <div>
      <div className="textTitle">Insert Email Domain</div>
      <form>
        <input
          className="textbox"
          placeholder="SampsonConstruction@gmail.com"
          type="text"
          name="domain"
          onChange={handleDomainChange}
        ></input>
      </form>
    </div>
  );
}
