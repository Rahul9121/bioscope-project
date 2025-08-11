import React from "react";

const GlassButton = ({ text, onClick }) => {
  return (
    <button
      onClick={onClick}
      className="px-5 py-2 text-white rounded-lg border border-glassBorder backdrop-blur-md bg-glassWhite hover:backdrop-blur-xl transition-all"
    >
      {text}
    </button>
  );
};

export default GlassButton;
