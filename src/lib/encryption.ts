import crypto from 'crypto'

const algorithm = 'aes-256-cbc'
const secretKey = process.env.API_ENCRY_KEY || crypto.randomBytes(32).toString('hex')

export async function encrypt(text: string): Promise<string> {
  const iv = crypto.randomBytes(16) // Generate new IV for each encryption
  const key = crypto.scryptSync(secretKey, 'salt', 32)
  const cipher = crypto.createCipheriv(algorithm, key, iv)
  let encrypted = cipher.update(text, 'utf8', 'hex')
  encrypted += cipher.final('hex')
  return iv.toString('hex') + ':' + encrypted
}

export async function decrypt(encryptedData: string): Promise<string> {
  const [ivHex, encryptedHex] = encryptedData.split(':')
  const key = crypto.scryptSync(secretKey, 'salt', 32)
  const decipher = crypto.createDecipheriv(algorithm, key, Buffer.from(ivHex, 'hex'))
  let decrypted = decipher.update(Buffer.from(encryptedHex, 'hex'), 'utf8', false)
  decrypted += decipher.final('utf8')
  return decrypted
}
