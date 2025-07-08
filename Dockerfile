# Dockerfile for RodaAI
FROM golang:1.21-alpine

WORKDIR /app

# Copy all project files
COPY . .

# Build your Go project
RUN go mod tidy && go build -o rodaai

# Expose port 8080 for Vercel runtime
EXPOSE 8080

# Start the server
CMD ["./rodaai"]
