import { GoogleGenerativeAI } from "@google/generative-ai";
import dotenv from "dotenv";
import { logInfo, logError } from "./logger.js";
import { extractKeywords } from "./dataProcessor.js";

dotenv.config();

const apiKey = process.env.GOOGLE_GENERATIVE_AI_KEY;
const genAI = new GoogleGenerativeAI(apiKey);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

/**
 * Generate content and log metrics.
 */
export async function generateContent(prompts) {
  let content = [];
  const startTime = Date.now();

  for (const prompt of prompts) {
    try {
      const response = await model.generateContent(prompt);
      const result = response.response?.text() || "No content generated.";

      const keywords = extractKeywords(result);
      content.push({ prompt, content: result, keywords });

      logInfo(`Generated content for prompt: "${prompt}"`);

    } catch (error) {
      logError(`Error generating content for prompt: "${prompt}"`, error, "GENERATION_ERROR");
    }
  }

  const endTime = Date.now();
  logInfo(`Total execution time: ${(endTime - startTime) / 1000}s`);

  return content;
}
