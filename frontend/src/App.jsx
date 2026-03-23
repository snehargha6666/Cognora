import { useState } from "react";
import SearchBar from "./components/SearchBar";
import ResultCard from "./components/ResultCard";
import Loader from "./components/Loader";
import { searchQuery } from "./services/api";

export default function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (query) => {
    setLoading(true);
    try {
      const data = await searchQuery(query);
      setResults(data.results || []);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-white p-6 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold text-center mb-6">
        Semantic Browser
      </h1>

      <SearchBar onSearch={handleSearch} />

      <div className="mt-6 space-y-4">
        {loading && <Loader />}
        {results.map((r, i) => (
          <ResultCard key={i} result={r} />
        ))}
      </div>
    </div>
  );
}