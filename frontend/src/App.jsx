import { useState } from "react";
import SearchBar from "./components/SearchBar";
import ResultCard from "./components/ResultCard";
import Loader from "./components/Loader";
import { searchQuery } from "./services/api";

export default function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState("search"); // 🔥 NEW (search | upload)

  // 🔹 Normal search
  const handleSearch = async (query) => {
    setMode("search");
    setLoading(true);

    try {
      const data = await searchQuery(query);
      setResults(data.results || []);
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  // 🔹 File upload results (NEW)
  const handleFileUpload = (data) => {
    setMode("upload");
    setResults(data.papers || []);
  };

  return (
    <div className="min-h-screen bg-white p-6 max-w-3xl mx-auto">
      
      <h1 className="text-3xl font-bold text-center mb-6">
        Semantic Browser
      </h1>

      {/* 🔹 Search + Upload */}
      <SearchBar 
        onSearch={handleSearch} 
        onFileUpload={handleFileUpload} 
      />

      {/* 🔹 Mode Indicator (NEW) */}
      {mode === "upload" && (
        <p className="text-sm text-gray-500 mt-2 text-center">
          Showing results based on your uploaded file
        </p>
      )}

      {/* 🔹 Results */}
      <div className="mt-6 space-y-4">
        {loading && <Loader />}

        {!loading && results.length === 0 && (
          <p className="text-center text-gray-400">
            No results yet. Try searching or uploading a file.
          </p>
        )}

        {results.map((r, i) => (
          <ResultCard key={i} result={r} />
        ))}
      </div>
    </div>
  );
}