import { GoogleGenerativeAI } from "@google/generative-ai";
import dotenv from "dotenv";

dotenv.config();

const apiKey = process.env.GOOGLE_GENERATIVE_AI_KEY;
const environment = process.env.ENVIRONMENT || "production";

if (!apiKey) {
  console.error("[ERROR] Missing Google Generative AI API key.");
  process.exit(1);
}

// Initialize the Google Generative AI client
const genAI = new GoogleGenerativeAI(apiKey);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

/**
 * Generates content based on a given prompt.
 * @param {string} prompt - The prompt to generate content for.
 * @returns {Promise<string>} - Generated content or error message.
 */
export async function generateContent(prompt) {
  try {
    const response = await model.generateContent(prompt);
    const content = response.response?.text();
    
    if (!content) {
      throw new Error("Empty response from the model.");
    }

    logMessage("[SUCCESS] Content generated successfully.");
    return content;

  } catch (error) {
    logError("[ERROR] Failed to generate content", error);
    return `Error: ${error.message}`;
  }
}

/**
 * Logs messages based on the environment.
 * @param {string} message - The message to log.
 */
function logMessage(message) {
  if (environment === "development") {
    console.log(`[LOG] ${message}`);
  }
}

/**
 * Logs errors with additional context.
 * @param {string} message - The error message.
 * @param {Error} error - The error object.
 */
function logError(message, error) {
  console.error(`${message}: ${error.message}`);
  if (environment === "development") {
    console.error(error.stack);
  }
}
