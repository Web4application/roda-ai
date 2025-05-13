import winston from "winston";
import dotenv from "dotenv";

dotenv.config();

const logger = winston.createLogger({
  level: "info",
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.printf(({ timestamp, level, message }) => `[${timestamp}] ${level.toUpperCase()}: ${message}`)
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: "./logs/error.log", level: "error" })
  ]
});

export function logInfo(message) {
  logger.info(message);
}

export function logError(message, error, code = "UNEXPECTED_ERROR") {
  logger.error(`[${code}] ${message}: ${error.message}`);
}
