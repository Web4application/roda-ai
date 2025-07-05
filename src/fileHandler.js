import fs from "fs-extra";
import path from "path";
import { createObjectCsvWriter } from "csv-writer";
import { logInfo, logError } from "./logger.js";

/**
 * Save content to a text file.
 */
export async function saveAsText(content, filename) {
  const filePath = path.join(process.cwd(), filename);

  try {
    await fs.outputFile(filePath, content);
    logInfo(`Content saved as text at ${filePath}`);
  } catch (error) {
    logError("Failed to save text file", error);
  }
}

/**
 * Save content as JSON.
 */
export async function saveAsJson(content, filename) {
  const filePath = path.join(process.cwd(), filename);

  try {
    await fs.writeJson(filePath, { content });
    logInfo(`Content saved as JSON at ${filePath}`);
  } catch (error) {
    logError("Failed to save JSON file", error);
  }
}

/**
 * Save content as CSV.
 */
export async function saveAsCsv(content, filename) {
  const filePath = path.join(process.cwd(), filename);

  const csvWriter = createObjectCsvWriter({
    path: filePath,
    header: [{ id: "prompt", title: "Prompt" }, { id: "content", title: "Generated Content" }]
  });

  try {
    await csvWriter.writeRecords(content);
    logInfo(`Content saved as CSV at ${filePath}`);
  } catch (error) {
    logError("Failed to save CSV file", error);
  }
}
