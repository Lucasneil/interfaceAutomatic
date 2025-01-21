from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64

# 公钥
data = 'Sd2024'
# 加密方法
def encrypt_data(data):
    #公钥
    public_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCAmmOLsLvqW9puLqvdChcvUFZhtWAxqQ1nP+3uokDxGwWuh3hnJ4nk2vD9QlDQ/deOJPwo0kB2yL4XEe3OJ3rr1wUdcOvYEq7IXNnL98L0LDEHgj4RN9f72XE7h7thOgBCsPh9Eea3QkBa00RYg6VZNq9brioLNWE4QfWxq/QpdQIDAQAB'
    # 导入公钥
    rsakey = RSA.importKey('-----BEGIN PUBLIC KEY-----\n' + public_key + '\n-----END PUBLIC KEY-----\n')
    # 创建用于执行PKCS1_v1_5加密的密码
    cipher = PKCS1_v1_5.new(rsakey)
    # 加密并编码为base64
    encrypted_data = base64.b64encode(cipher.encrypt(data.encode('utf-8')))
    encrypted_data = encrypted_data.decode('utf-8').replace("+", "_")
    return encrypted_data

# 示例用法
if __name__ == "__main__":
    data = "Sd2024"
    encrypted = encrypt_data(data)
    print("Encrypted data:", encrypted)
