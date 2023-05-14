import React from "react";
export default function Header() {
  return (
    <div className="header">
      <img
        src={process.env.PUBLIC_URL + "/banner.png"}
        className="banner"
        alt="Sequoia Recruitment"
      ></img>
    </div>
  );
}
