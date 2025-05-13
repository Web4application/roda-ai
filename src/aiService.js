import { GoogleGenerativeAI } from "@google/generative-ai";
import axios from "axios";
import dotenv from "dotenv";
import { logInfo, logError } from "./logger.js";

dotenv.config();

const apiKey = process.env.GOOGLE_GENERATIVE_AI_KEY;
const environment = process.env.ENVIRONMENT || "production";

if (!apiKey) {
  logError("API Key is missing", new Error("Missing API Key"));
  process.exit(1);
}

const genAI = new GoogleGenerativeAI(apiKey);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

// Cache structure
const cache = new Map();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

/**
 * Fetch data with retry logic.
 * @param {Function} fn - The function to execute.
 * @param {number} retries - Number of retry attempts.
 */
async function withRetry(fn, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (error) {
      logError(`Retry ${i + 1} failed`, error);
      if (i === retries - 1) throw error;
    }
  }
}

/**
 * Generates content using Google Generative AI with caching and retry logic.
 * @param {string} prompt - The input prompt.
 * @returns {Promise<string>}
 */
export async function generateContent(prompt) {
  const cacheKey = prompt;
  const cachedData = cache.get(cacheKey);

  if (cachedData && Date.now() - cachedData.timestamp < CACHE_TTL) {
    logInfo("Returning cached data");
    return cachedData.content;
  }

  try {
    const response = await withRetry(() => model.generateContent(prompt));
    const content = response.response?.text();

    if (!content) {
      throw new Error("Empty response from the model.");
    }

    cache.set(cacheKey, { content, timestamp: Date.now() });
    logInfo("Content generated successfully");
    return content;

  } catch (error) {
    logError("Error generating content", error);
    return `Error: ${error.message}`;
  }
}
