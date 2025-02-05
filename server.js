// Import the http module
const http = require('http');

// Define the port to listen on
const PORT = 8000;

// Create the server
const server = http.createServer((req, res) => {
  // Set the response header with status and content type
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  
  // Send the response body
  res.end('Hello, World!\n');
});

// Make the server listen on the specified port
server.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});
