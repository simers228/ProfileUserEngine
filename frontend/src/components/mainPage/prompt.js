import React, { useState } from "react";
export default function Prompt({ setPrompt }) {
  const handlePromptChange = (event) => {
    setPrompt(event.target.value);
  };
  return (
    <div>
      <div className="textTitle">Input Your Job Description</div>
      <form>
        <textarea
          placeholder="Compose an email from recruiter Simer Singh at Sequoia Recruitment Partners. The role is based in the Greater Omaha area. Do not mention the name of the company or client in the email. Use a slightly informal language style. In the email, emphasize the benefits of the role and explain why the client is a good fit for the candidate. Please avoid using any placeholder information."
          type="text"
          name="prompt"
          className="textbox4 textbox"
          onChange={handlePromptChange}
        ></textarea>
      </form>
    </div>
  );
}
