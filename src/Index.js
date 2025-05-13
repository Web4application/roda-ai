import { generateContent } from "./aiService.js";

// Define a comprehensive prompt
const prompt = `
### Fantasy
1. "Describe a world where the seasons are controlled by mythical creatures."
2. "A young wizard discovers an ancient spellbook that can alter reality."
3. "A dragon and a knight form an unlikely alliance to save their kingdom."

### Science Fiction
1. "Write about a future where humans can upload their consciousness into a digital world."
2. "In a world where time travel is possible, a historian accidentally changes a major event in history."
3. "In a future where humans live on Mars, a scientist discovers a hidden alien civilization."
`;

/**
 * Main function to initiate content generation.
 */
async function main() {
  console.log("[INFO] Generating content...");
  const content = await generateContent(prompt);
  console.log("\nGenerated Content:\n", content);
}

main();
