import React, { useState } from 'react';
import axios, { AxiosError } from 'axios';

const UploadFood: React.FC = () => {
  const [image, setImage] = useState<File | null>(null);
  const [result, setResult] = useState<{
    name: string;
    nutrients: string;
    ingredients: string;
  } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setImage(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!image) {
      setError('Please select an image first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', image);

    try {
      setError(null);
      const response = await axios.post('http://127.0.0.1:8000/upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setResult(response.data);
    } catch (error: unknown) {
      // Type guard to check if error is an AxiosError
      if (axios.isAxiosError(error)) {
        const axiosError = error as AxiosError<{ detail: string }>;
        setError(axiosError.response?.data?.detail || 'An error occurred during the request');
      } else {
        // For non-Axios errors
        setError('An unexpected error occurred');
      }
    }
  };

  return (
    <div className="p-4 border rounded-lg shadow-lg text-center max-w-md mx-auto">
      <h2 className="text-xl font-bold mb-4">Upload an Image</h2>
      <input type="file" accept="image/*" onChange={handleFileChange} className="mb-4" />
      <button onClick={handleUpload} className="bg-blue-500 text-white px-4 py-2 rounded-lg">
        Upload
      </button>

      {error && <p className="text-red-500 mt-2">{error}</p>}
      {result && (
        <div className="mt-4 p-2 border">
          <h3 className="text-lg font-semibold">Food Recognized: {result.name}</h3>
          <p>
            <strong>Nutrients:</strong> {result.nutrients}
          </p>
          <p>
            <strong>Ingredients:</strong> {result.ingredients}
          </p>
        </div>
      )}
    </div>
  );
};

export default UploadFood;
