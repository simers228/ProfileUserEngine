import React from "react";
function Header() {
  return (
    <div className=" header">
      <img
        src={process.env.PUBLIC_URL + "/banner.png"}
        className="banner"
      ></img>
    </div>
  );
}
export default Header;
