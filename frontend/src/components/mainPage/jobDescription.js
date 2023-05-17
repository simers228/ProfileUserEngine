import React, { useState } from "react";
export default function JobDescription({ setJobDescription }) {
  const [setSelectedFile] = useState(null);
  const handleJobDescriptionChange = (event) => {
    setJobDescription(event.target.value);
  };
  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);

    const reader = new FileReader();
    reader.onload = (e) => {
      const fileContent = e.target.result;
      setJobDescription(fileContent);
    };
    reader.readAsText(file);
  };
  return (
    <div>
      <div className="textTitle">Input Your Job Description</div>
      <form>
        <textarea
          placeholder="POSITION: Enterprise Sales Director, Bangalore
          BANGALORE /GROWTH – SALES /FULL TIME/ ON-SITE
          Job Objective:
          A go-getter and visionary who is ready to bring 9+ years of sales experience to help a growing company take things to the next level. Knowledge, networking abilities and passion for the healthcare industry inform daily work. Experience from a general insurance or insurance broking background would be an added advantage.
          
          Job Responsibilities
          Build and manage a team of high performing sales executives by providing strong, experience-led mentorship
          Successfully engage with some of the largest and most strategic accounts to ensure meaningful and sizable wins
          Be the voice of the customer internally to continuously improve go-to-market execution strategy
          Co-develop the quarterly targets, incentives, and sales plan for the regional team, including multiple AEs and SDRs
          Implement a metrics-driven approach to performance management, rewards and recognition
          Drive ICP recognizing mindset for opportunity prioritization and optimized sales effort
          Ensure the proper use of CRM and other internal tools for effective data management
          Set up upskilling & training programs for the team in collaboration with sales trainers
          Foster strong collaborative relationships with internal stakeholders for faster quote generation and post-win hand-offs to operations function
          Contribute to our overall Sales & Growth strategy by working with the VP Sales, CRO, CEO and the executive team on cross-geography projects
          
          Job Specifications
          9+ years of B2B based experience, preferably in SaaS, software, or insurance
          Well-established contacts within the market & ability to create new relationships
          Ability to thrive in a high velocity environment
          Capable of communicating with a diverse range of individuals
          Strong negotiation skills & attention to detail with a CAN DO attitude
          Capacity to think beyond traditional sales mindset
          Familiarity with G Suite and Microsoft office, including Excel
          Fluency in English, Hindi &/or other relevant regional languages Excited to travel, meet people, and build life-long relationships "
          type="text"
          name="jobDescription"
          className="textbox3 textbox"
          onChange={handleJobDescriptionChange}
        ></textarea>
        <input
          type="file"
          className="text"
          name="jobDescriptionFile"
          accept=".txt"
          onChange={handleFileUpload}
        />
      </form>
    </div>
  );
}
