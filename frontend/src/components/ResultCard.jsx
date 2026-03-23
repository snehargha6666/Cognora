export default function ResultCard({ result }) {
  return (
    <div className="p-4 border rounded-xl shadow-sm">
      <h2 className="font-semibold text-lg">{result.title}</h2>

      <p className="text-sm text-gray-600 mt-1">
        {result.snippet}
      </p>

      {result.url && (
        <a
          href={result.url}
          target="_blank"
          className="text-blue-500 text-sm mt-2 inline-block"
        >
          Visit →
        </a>
      )}
    </div>
  );
}