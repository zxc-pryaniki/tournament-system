import React, { useState } from "react";
import TournamentModal from "./Tournament/TournamentModal";

export default function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-100 p-6 flex justify-start items-start">
      <button
        onClick={() => setIsModalOpen(true)}
        className="bg-[#2563eb] hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg shadow-lg transition-all"
      >
        Створити турнір
      </button>

      <TournamentModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
      />
    </div>
  );
}
