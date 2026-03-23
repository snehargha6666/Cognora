import { useState } from "react";

export default function SearchBar({ onSearch }) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        className="flex-1 p-3 border rounded-xl"
        placeholder="Ask anything..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <button className="px-4 bg-black text-white rounded-xl">
        Search
      </button>
    </form>
  );
}