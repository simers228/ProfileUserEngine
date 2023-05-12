import React from "react";
export default function LinkedUrl() {
  return (
    <div className="container">
      <form
        className="prompts"
        action="http://localhost:5000/userengine"
        method="POST"
      >
        <div className="textTitle">URL Submit</div>
        <div className="container">
          <input
            placeholder="https://linkedin.com"
            type="url"
            name="linkedinUrl"
            className="textbox textbox1"
          ></input>
        </div>
        <div className="container">
          <button className="button">Submit</button>
        </div>
      </form>
    </div>
  );
}
