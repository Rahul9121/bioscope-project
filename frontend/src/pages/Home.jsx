import React from "react";
import GlassCard from "../components/GlassCard";
import GlassButton from "../components/GlassButton";

const Home = () => {
  return (
    <div className="h-screen flex flex-col items-center justify-center bg-gradient-to-r from-blue-900 via-purple-900 to-indigo-900">
      <GlassCard
        title="Biodiversity Risk Report"
        content="Explore potential biodiversity threats within your area."
      />
      <div className="mt-4">
        <GlassButton text="Start Assessment" onClick={() => alert("Assessment Started!")} />
      </div>
    </div>
  );
};

export default Home;
