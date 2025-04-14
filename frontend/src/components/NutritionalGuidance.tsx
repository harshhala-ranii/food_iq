import React, { useEffect } from 'react';
import './NutritionalGuidance.css';

interface RecommendationData {
  is_safe: boolean;
  warnings: string[];
  suggestions: string[];
  approval_message: string | null;
}

interface NutritionalGuidanceProps {
  guidance: RecommendationData;
}

const NutritionalGuidance: React.FC<NutritionalGuidanceProps> = ({ guidance }) => {
  useEffect(() => {
    console.log('NutritionalGuidance mounted with data:', guidance);
  }, [guidance]);

  console.log('NutritionalGuidance rendering with data:', guidance);

  if (!guidance) {
    console.log('No guidance data received');
    return <div>No nutritional guidance available.</div>;
  }

  // Ensure all properties exist
  const safeGuidance = {
    is_safe: guidance.is_safe !== undefined ? guidance.is_safe : true,
    warnings: Array.isArray(guidance.warnings) ? guidance.warnings : [],
    suggestions: Array.isArray(guidance.suggestions) ? guidance.suggestions : [],
    approval_message: guidance.approval_message || null
  };

  console.log('Processed guidance data:', safeGuidance);

  return (
    <div className="nutritional-guidance" style={{ border: '2px solid #4CAF50', padding: '15px', marginBottom: '15px' }}>
      <h3 style={{ color: '#2E7D32', marginBottom: '15px' }}>Nutritional Guidance</h3>
      
      {safeGuidance.approval_message && (
        <div className="approval-message" style={{ backgroundColor: '#E8F5E9', padding: '15px', marginBottom: '15px', borderRadius: '5px' }}>
          <p style={{ color: '#2E7D32', margin: 0, fontWeight: 'bold' }}>{safeGuidance.approval_message}</p>
        </div>
      )}
      
      {safeGuidance.warnings && safeGuidance.warnings.length > 0 && (
        <div className="warnings-section" style={{ backgroundColor: '#FFF3E0', padding: '15px', marginBottom: '15px', borderRadius: '5px' }}>
          <h4 style={{ color: '#E65100', marginBottom: '10px' }}>Warnings</h4>
          <ul style={{ margin: 0, paddingLeft: '20px' }}>
            {safeGuidance.warnings.map((warning, index) => (
              <li key={index} style={{ color: '#E65100', marginBottom: '5px' }}>{warning}</li>
            ))}
          </ul>
        </div>
      )}
      
      {safeGuidance.suggestions && safeGuidance.suggestions.length > 0 && (
        <div className="suggestions-section" style={{ backgroundColor: '#E3F2FD', padding: '15px', marginBottom: '15px', borderRadius: '5px' }}>
          <h4 style={{ color: '#1565C0', marginBottom: '10px' }}>Suggestions</h4>
          <ul style={{ margin: 0, paddingLeft: '20px' }}>
            {safeGuidance.suggestions.map((suggestion, index) => (
              <li key={index} style={{ color: '#1565C0', marginBottom: '5px' }}>{suggestion}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default NutritionalGuidance; 