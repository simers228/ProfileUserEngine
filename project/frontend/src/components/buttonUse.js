import React from "react";
function ButtonUse() {
  return (
    <div className="center textbox">
      <form action="http://localhost:5000" method="POST">
        <input
          placeholder="https://linkedin.com"
          type="url"
          name="linkedinUrl"
        ></input>
        <input type="submit" value="Submit"></input>
      </form>
    </div>
  );
}

export default ButtonUse;
