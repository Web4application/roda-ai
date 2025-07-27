/**
 * Extract keywords from content.
 * @param {string} content - The generated content.
 * @returns {string[]} - Extracted keywords.
 */
export function extractKeywords(content) {
  const words = content.match(/\b\w+\b/g);
  const wordCount = {};

  words.forEach((word) => {
    word = word.toLowerCase();
    wordCount[word] = (wordCount[word] || 0) + 1;
  });

  return Object.keys(wordCount)
    .filter((word) => wordCount[word] > 1 && word.length > 3)
    .slice(0, 10); // Limit to top 10 keywords
}
