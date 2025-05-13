import winston from "winston";
import dotenv from "dotenv";
import Sentry from "@sentry/node";

dotenv.config();

const environment = process.env.ENVIRONMENT || "production";
const sentryDsn = process.env.SENTRY_DSN;

// Sentry initialization
if (sentryDsn) {
  Sentry.init({ dsn: sentryDsn, environment });
}

const logger = winston.createLogger({
  level: "info",
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.printf(({ timestamp, level, message }) => {
      return `[${timestamp}] ${level.toUpperCase()}: ${message}`;
    })
  ),
  transports: [new winston.transports.Console()],
});

export function logInfo(message) {
  logger.info(message);
}

export function logError(message, error) {
  logger.error(`${message}: ${error.message}`);
  if (sentryDsn) {
    Sentry.captureException(error);
  }
}
