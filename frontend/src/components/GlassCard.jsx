import React from "react";

const GlassCard = ({ title, content }) => {
  return (
    <div className="glass p-6 text-white w-80">
      <h2 className="text-xl font-semibold">{title}</h2>
      <p className="mt-2 text-sm">{content}</p>
    </div>
  );
};

export default GlassCard;
