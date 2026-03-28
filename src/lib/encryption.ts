import * as crypto from 'crypto'

const algorithm = 'aes-256-cbc'

// SECURITY FIX #1: Correct env var name (was API_ENCRY_KEY)
// SECURITY FIX #2: Fail hard if not set - no random fallback (prevents data loss on restart)
const encryptionKeyEnv = process.env.API_ENCRYPTION_KEY
if (!encryptionKeyEnv) {
  throw new Error(
    'CRITICAL: API_ENCRYPTION_KEY environment variable is required. ' +
    'Set it before starting the application. ' +
    'Generate with: node -e "console.log(require(\'crypto\').randomBytes(32).toString(\'hex\'))"'
  )
}

// SECURITY FIX #3: Derive salt from encryption key instead of hardcoded 'salt'
// This ensures deterministic salt (same on every restart) while avoiding trivial values
const saltBytes = crypto.createHash('sha256').update(encryptionKeyEnv + ':encryption-salt').digest()

export async function encrypt(text: string): Promise<string> {
  const iv = crypto.randomBytes(16) // Generate new IV for each encryption
  // Use string salt to avoid Buffer type issues with scryptSync
  const key = crypto.scryptSync(encryptionKeyEnv, saltBytes.toString('hex'), 32)
  const cipher = crypto.createCipheriv(algorithm, key, iv)
  let encrypted = cipher.update(text, 'utf8', 'hex')
  encrypted += cipher.final('hex')
  return iv.toString('hex') + ':' + encrypted
}

export async function decrypt(encryptedData: string): Promise<string> {
  const [ivHex, encryptedHex] = encryptedData.split(':')
  // Use string salt to match encrypt function
  const key = crypto.scryptSync(encryptionKeyEnv, saltBytes.toString('hex'), 32)
  const decipher = crypto.createDecipheriv(algorithm, key, Buffer.from(ivHex, 'hex'))
  // Use explicit Buffer input and string output encoding
  const decrypted: string = decipher.update(Buffer.from(encryptedHex, 'hex'), undefined, 'utf8') + decipher.final('utf8')
  return decrypted
}
