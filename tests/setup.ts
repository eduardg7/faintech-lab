// Test setup file - runs before all tests
// Set required environment variables for testing

// Set a test encryption key for API key encryption tests
// This is a fixed test key - DO NOT use in production
process.env.API_ENCRYPTION_KEY = 'test-encryption-key-32-bytes-long-do-not-use-in-production'
