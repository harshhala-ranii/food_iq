import React, { useState, useEffect } from 'react';
import { predictFood, getNutritionByFoodName, getFoodClasses } from '../services/api';
import NutritionFacts from './NutritionFacts';
import NutritionalGuidance from './NutritionalGuidance';
import './FoodImageUpload.css';

interface NutritionInfo {
  food_product: string;
  amount: string;
  energy: number;
  carbohydrate: number;
  protein: number;
  total_fat: number;
  sodium: number;
  iron: number;
}

interface Recommendations {
  is_safe: boolean;
  warnings: string[];
  suggestions: string[];
  approval_message: string | null;
}

interface PredictionResult {
  predicted_food: string;
  confidence: number;
  nutrition: NutritionInfo;
  volume_estimation: number | null;
  masked_image: string | null;
  recommendations: Recommendations;
}

interface VolumeResult {
  food: string;
  volume_estimation: number;
  adjusted_nutrition: {
    volume_estimate_g: number;
    energy: number;
    carbohydrate: number;
    protein: number;
    total_fat: number;
    sodium: number;
    iron: number;
  };
  masked_image: string;
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
  const [volumeResult, setVolumeResult] = useState<VolumeResult | null>(null);

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

  const handleImageUpload = async (file: File) => {
    setIsUploading(true);
    setError(null);
    
    try {
      const data = await predictFood(file);
      
      setResult({
        predicted_food: data.predicted_food,
        confidence: data.confidence,
        nutrition: {
          food_product: data.nutrition.food_product,
          amount: data.nutrition.amount,
          energy: data.nutrition.energy,
          carbohydrate: data.nutrition.carbohydrate,
          protein: data.nutrition.protein,
          total_fat: data.nutrition.total_fat,
          sodium: data.nutrition.sodium,
          iron: data.nutrition.iron
        },
        volume_estimation: data.volume_estimation,
        masked_image: data.masked_image,
        recommendations: {
          is_safe: data.recommendations.is_safe,
          warnings: data.recommendations.warnings || [],
          suggestions: data.recommendations.suggestions || [],
          approval_message: data.recommendations.approval_message
        }
      });

      // Set volume result from the main prediction response
      if (data.volume_estimation && data.masked_image) {
        setVolumeResult({
          food: data.predicted_food,
          volume_estimation: data.volume_estimation,
          adjusted_nutrition: data.nutrition,
          masked_image: data.masked_image
        });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to process image');
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
      const response = await getNutritionByFoodName(manualFoodName.trim());
      
      setResult({
        predicted_food: manualFoodName,
        confidence: 1.0,
        nutrition: response.nutrition,
        volume_estimation: null,
        masked_image: null,
        recommendations: response.recommendations
      });
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

  const displayResults = () => {
    if (!result) return null;
    
    return (
      <div className="results-container">
        <h3>Analysis Result</h3>
        <p>Identified Food: {result.predicted_food}</p>
        <p>Confidence: {(result.confidence * 100).toFixed(2)}%</p>
        
        {volumeResult && (
          <div className="volume-result">
            <h4>Volume Estimation</h4>
            <p>Estimated Volume: {volumeResult.volume_estimation.toFixed(2)}g</p>
            <div className="masked-image-container">
              <h4>Food Mask</h4>
              <img 
                src={volumeResult.masked_image} 
                alt="Masked Food" 
                className="masked-image"
              />
            </div>
          </div>
        )}
        
        <div className="nutrition-and-recommendations">
          <div className="nutrition-section">
            {result.nutrition && (
              <NutritionFacts 
                nutrition={{
                  ...result.nutrition,
                  energy: result.nutrition.energy.toString(),
                  carbohydrate: result.nutrition.carbohydrate.toString(),
                  protein: result.nutrition.protein.toString(),
                  total_fat: result.nutrition.total_fat.toString(),
                  sodium: result.nutrition.sodium.toString(),
                  iron: result.nutrition.iron.toString()
                }} 
              />
            )}
          </div>
          
          <div className="recommendations-section" style={{ border: '1px solid #ccc', padding: '20px', marginTop: '20px' }}>
            <h4 style={{ color: '#333', marginBottom: '15px' }}>Nutritional Recommendations</h4>
            {result.recommendations ? (
              <div style={{ backgroundColor: '#f5f5f5', padding: '15px', borderRadius: '5px' }}>
                <NutritionalGuidance guidance={result.recommendations} />
              </div>
            ) : (
              <p>No recommendations available for this food item.</p>
            )}
          </div>
        </div>
      </div>
    );
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
                onClick={() => selectedFile && handleImageUpload(selectedFile)} 
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
      
      {displayResults()}
    </div>
  );
};

export default FoodImageUpload; 