import axios from 'axios';
import { API_CONFIG } from '../config';

interface ChatResponse {
  response: string;
}

export const chatWithBot = async (message: string): Promise<string> => {
  try {
    // Create a new axios instance without authentication
    const chatClient = axios.create({
      baseURL: API_CONFIG.BASE_URL,
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    const response = await chatClient.post<ChatResponse>(
      `${API_CONFIG.ENDPOINTS.CHAT}`,
      { message }
    );
    return response.data.response;
  } catch (error) {
    console.error('Error in chat service:', error);
    throw error;
  }
}; 