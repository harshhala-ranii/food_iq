import React from 'react';
import './NutritionalGuidance.css';

interface NutritionalGuidanceProps {
  guidance: string | null;
}

const NutritionalGuidance: React.FC<NutritionalGuidanceProps> = ({ guidance }) => {
  if (!guidance) {
    return null;
  }

  // Split the guidance into paragraphs
  const paragraphs = guidance.split('\n\n').filter(p => p.trim() !== '');

  // Check if the guidance has a title (first line ending with a colon)
  const hasTitle = paragraphs.length > 0 && paragraphs[0].includes(':');
  
  // Extract title and content if there's a title
  let title = '';
  let content = [...paragraphs];
  
  if (hasTitle) {
    const titleParts = paragraphs[0].split(':');
    title = titleParts[0].trim();
    
    // Reconstruct the first paragraph without the title
    const firstParagraphContent = titleParts.slice(1).join(':').trim();
    content[0] = firstParagraphContent;
  }

  return (
    <div className="nutritional-guidance">
      <h3>Nutritional Guidance</h3>
      
      {hasTitle && <h4>{title}</h4>}
      
      {content.map((paragraph, index) => {
        // Check if this paragraph is a list (contains bullet points)
        if (paragraph.includes('\n-')) {
          const [listTitle, ...listItems] = paragraph.split('\n-');
          return (
            <div key={index} className="guidance-section">
              {listTitle && <p>{listTitle.trim()}</p>}
              <ul>
                {listItems.map((item, itemIndex) => (
                  <li key={itemIndex}>{item.trim()}</li>
                ))}
              </ul>
            </div>
          );
        }
        
        return <p key={index}>{paragraph}</p>;
      })}
    </div>
  );
};

export default NutritionalGuidance; 