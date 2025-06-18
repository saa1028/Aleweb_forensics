import hashlib

# 计算文件的哈希值
def calculate_hash(file_path):
    with open(file_path, 'rb') as f:
        md5 = hashlib.md5()
        sha256 = hashlib.sha256()
        while True:
            data = f.read(8192)
            if not data:
                break
            md5.update(data)
            sha256.update(data)
    return md5.hexdigest(), sha256.hexdigest()

# 记录哈希值到文件
def record_hash(file_path, hash_file_path):
    md5, sha256 = calculate_hash(file_path)
    with open(hash_file_path, 'a') as f:
        f.write(f'md5:{md5}  {file_path}\n')
        f.write(f'sha256:{sha256}  {file_path}\n')

