import React, { useState, useEffect } from 'react';
import { predictFood, getNutritionByFoodName, getFoodClasses } from '../services/api';
import NutritionFacts from './NutritionFacts';
import NutritionalGuidance from './NutritionalGuidance';
import './FoodImageUpload.css';

interface NutritionInfo {
  food_product: string;
  amount: string;
  energy: string;
  carbohydrate: string;
  protein: string;
  total_fat: string;
  sodium: string;
  iron: string;
}

interface PredictionResult {
  predicted_food: string;
  confidence: number;
  nutrition: NutritionInfo | null;
  nutritional_guidance: string | null;
}

const FoodImageUpload: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [manualFoodName, setManualFoodName] = useState<string>('');
  const [isManualSearch, setIsManualSearch] = useState<boolean>(false);
  const [isSearching, setIsSearching] = useState<boolean>(false);
  const [foodClasses, setFoodClasses] = useState<string[]>([]);
  const [filteredSuggestions, setFilteredSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState<boolean>(false);
  const [isLoadingSuggestions, setIsLoadingSuggestions] = useState<boolean>(true);
  const [selectedSuggestionIndex, setSelectedSuggestionIndex] = useState<number>(-1);

  // Fetch food classes for suggestions
  useEffect(() => {
    const fetchFoodClasses = async () => {
      setIsLoadingSuggestions(true);
      try {
        const classes = await getFoodClasses();
        setFoodClasses(classes);
      } catch (err) {
        console.error('Error fetching food classes for suggestions:', err);
      } finally {
        setIsLoadingSuggestions(false);
      }
    };

    fetchFoodClasses();
  }, []);

  // Filter suggestions based on input
  useEffect(() => {
    if (manualFoodName.trim() === '') {
      setFilteredSuggestions([]);
      setShowSuggestions(false);
      return;
    }

    const normalizedInput = manualFoodName.toLowerCase().trim();
    const filtered = foodClasses
      .filter(food => 
        food.toLowerCase().includes(normalizedInput)
      )
      .slice(0, 5); // Limit to 5 suggestions
    
    setFilteredSuggestions(filtered);
    setShowSuggestions(filtered.length > 0);
  }, [manualFoodName, foodClasses]);

  // Reset selected index when suggestions change
  useEffect(() => {
    setSelectedSuggestionIndex(-1);
  }, [filteredSuggestions]);

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (!showSuggestions || filteredSuggestions.length === 0) {
      return;
    }

    // Arrow down
    if (event.key === 'ArrowDown') {
      event.preventDefault();
      setSelectedSuggestionIndex(prevIndex => 
        prevIndex < filteredSuggestions.length - 1 ? prevIndex + 1 : 0
      );
    }
    // Arrow up
    else if (event.key === 'ArrowUp') {
      event.preventDefault();
      setSelectedSuggestionIndex(prevIndex => 
        prevIndex > 0 ? prevIndex - 1 : filteredSuggestions.length - 1
      );
    }
    // Enter key
    else if (event.key === 'Enter') {
      event.preventDefault();
      if (selectedSuggestionIndex >= 0) {
        handleSuggestionClick(filteredSuggestions[selectedSuggestionIndex]);
      } else if (manualFoodName.trim()) {
        handleManualSearch();
      }
    }
    // Escape key
    else if (event.key === 'Escape') {
      event.preventDefault();
      setShowSuggestions(false);
      setSelectedSuggestionIndex(-1);
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      setSelectedFile(file);
      
      // Create a preview URL for the selected image
      const fileReader = new FileReader();
      fileReader.onload = () => {
        setPreviewUrl(fileReader.result as string);
      };
      fileReader.readAsDataURL(file);
      
      // Reset previous results and errors
      setResult(null);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    setIsUploading(true);
    setError(null);

    try {
      const data = await predictFood(selectedFile);
      setResult(data);
    } catch (err: any) {
      console.error('Upload error:', err);
      if (err.response) {
        setError(`Error: ${err.response.data.detail || 'Failed to process image'}`);
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setIsUploading(false);
    }
  };

  const handleManualFoodNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setManualFoodName(event.target.value);
  };

  const handleSuggestionClick = (suggestion: string) => {
    setManualFoodName(suggestion);
    setShowSuggestions(false);
  };

  const handleManualSearch = async () => {
    if (!manualFoodName.trim()) {
      setError('Please enter a food name');
      return;
    }

    setIsSearching(true);
    setError(null);
    setShowSuggestions(false);

    try {
      // Use the API service to fetch nutrition information by food name
      const data = await getNutritionByFoodName(manualFoodName.trim());
      
      // Create a result object similar to the image prediction result
      setResult({
        predicted_food: data.nutrition.food_product,
        confidence: 1.0, // 100% confidence since it's a manual entry
        nutrition: data.nutrition,
        nutritional_guidance: data.nutritional_guidance
      });
      
      setIsManualSearch(true);
    } catch (err: any) {
      console.error('Manual search error:', err);
      setError(`Error: ${err.response?.data?.detail || err.message || 'Failed to fetch nutrition information'}`);
    } finally {
      setIsSearching(false);
    }
  };

  const toggleSearchMethod = () => {
    setIsManualSearch(!isManualSearch);
    setResult(null);
    setError(null);
    setShowSuggestions(false);
  };

  return (
    <div className="food-image-upload">
      <div className="search-toggle">
        <button 
          className={`toggle-button ${!isManualSearch ? 'active' : ''}`} 
          onClick={() => !isManualSearch ? null : toggleSearchMethod()}
        >
          Image Upload
        </button>
        <button 
          className={`toggle-button ${isManualSearch ? 'active' : ''}`} 
          onClick={() => isManualSearch ? null : toggleSearchMethod()}
        >
          Manual Search
        </button>
      </div>

      {!isManualSearch ? (
        // Image Upload Section
        <div className="upload-container">
          <div className="upload-section">
            <h2>Upload Food Image</h2>
            <p>Take a photo of your meal to get nutrition information</p>
            
            <div className="file-input-container">
              <input 
                type="file" 
                accept="image/jpeg,image/jpg" 
                onChange={handleFileChange}
                id="food-image-input"
                className="file-input"
              />
              <label htmlFor="food-image-input" className="file-input-label">
                Choose Image
              </label>
              
              <button 
                onClick={handleUpload} 
                disabled={!selectedFile || isUploading}
                className="upload-button"
              >
                {isUploading ? 'Analyzing...' : 'Analyze Food'}
              </button>
            </div>
            
            {error && <div className="error-message">{error}</div>}
          </div>
          
          <div className="preview-section">
            {previewUrl ? (
              <div className="image-preview">
                <img src={previewUrl} alt="Food preview" />
              </div>
            ) : (
              <div className="no-preview">
                <p>Image preview will appear here</p>
              </div>
            )}
          </div>
        </div>
      ) : (
        // Manual Search Section
        <div className="manual-search-container">
          <div className="manual-search-section">
            <h2>Search Food by Name</h2>
            <p>Enter the name of the food to get nutrition information</p>
            
            <div className="manual-input-container">
              <div className="suggestion-wrapper">
                <input 
                  type="text" 
                  value={manualFoodName}
                  onChange={handleManualFoodNameChange}
                  onKeyDown={handleKeyDown}
                  placeholder="Enter food name exactly as shown in suggestions (e.g., butter_chicken)"
                  className="manual-input"
                  onBlur={() => {
                    // Delay hiding suggestions to allow for clicks
                    setTimeout(() => setShowSuggestions(false), 200);
                  }}
                  onFocus={() => {
                    if (filteredSuggestions.length > 0) {
                      setShowSuggestions(true);
                    }
                  }}
                />
                
                {showSuggestions && (
                  <ul className="suggestions-list">
                    {isLoadingSuggestions ? (
                      <li className="suggestion-loading">Loading suggestions...</li>
                    ) : filteredSuggestions.length > 0 ? (
                      filteredSuggestions.map((suggestion, index) => (
                        <li 
                          key={index} 
                          onClick={() => handleSuggestionClick(suggestion)}
                          className={`suggestion-item ${index === selectedSuggestionIndex ? 'selected' : ''}`}
                        >
                          {suggestion}
                        </li>
                      ))
                    ) : (
                      <li className="suggestion-no-results">No matching foods found</li>
                    )}
                  </ul>
                )}
              </div>
              
              <button 
                onClick={handleManualSearch} 
                disabled={!manualFoodName.trim() || isSearching}
                className="search-button"
              >
                {isSearching ? 'Searching...' : 'Get Nutrition Info'}
              </button>
            </div>
            
            {error && <div className="error-message">{error}</div>}
          </div>
        </div>
      )}
      
      {result && (
        <div className="result-container">
          <div className="food-info">
            <h3>Food Information</h3>
            <div className="food-name">{result.predicted_food}</div>
            
            {!isManualSearch && (
              <div className="confidence">
                Confidence: {(result.confidence * 100).toFixed(2)}%
              </div>
            )}
            
            {previewUrl && !isManualSearch && (
              <div className="detected-image">
                <img src={previewUrl} alt={result.predicted_food} />
              </div>
            )}
          </div>
          
          {result.nutrition ? (
            <div className="nutrition-info">
              <NutritionFacts nutrition={result.nutrition} />
              <NutritionalGuidance guidance={result.nutritional_guidance} />
            </div>
          ) : (
            <div className="no-nutrition">
              <p>No nutrition information available for this food.</p>
              <p>Try searching with a different name or check our list of supported foods.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default FoodImageUpload; 