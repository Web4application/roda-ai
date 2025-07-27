import { generateContent } from "./aiService.js";
import { saveAsText, saveAsJson, saveAsCsv } from "./fileHandler.js";
import readline from "readline";
import { logInfo } from "./logger.js";

/**
 * Prompt user for input.
 */
function getUserInput() {
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    rl.question("Enter prompts separated by ';': ", (input) => {
      const prompts = input.split(";").map(p => p.trim()).filter(Boolean);
      rl.question("Enter output format (txt/json/csv): ", (format) => {
        rl.question("Enter output filename: ", (filename) => {
          rl.close();
          resolve({ prompts, format, filename });
        });
      });
    });
  });
}

(async () => {
  try {
    const { prompts, format, filename } = await getUserInput();
    const content = await generateContent(prompts);

    switch (format.toLowerCase()) {
      case "txt":
        await saveAsText(JSON.stringify(content, null, 2), `${filename}.txt`);
        break;
      case "json":
        await saveAsJson(content, `${filename}.json`);
        break;
      case "csv":
        await saveAsCsv(content, `${filename}.csv`);
        break;
      default:
        console.log("Invalid format. Please choose txt, json, or csv.");
    }
  } catch (error) {
    console.error("An unexpected error occurred:", error.message);
  }
})();

