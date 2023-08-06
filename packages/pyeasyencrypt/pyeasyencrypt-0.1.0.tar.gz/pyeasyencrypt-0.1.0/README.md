
# pyeasyencrypt

## Description 

The purpose of this module is to simplify the way of encrypting and decrypting strings at python with a simple password

## Example of Python code
```python
import logging, os
# pip install pyeasyencrypt
from pyeasyencrypt.pyeasyencrypt import encrypt_string, decrypt_string

level = os.getenv("LOGGER", "INFO")
logging.basicConfig(level=level)
logger = logging.getLogger(__name__)

def main():
    logger.info("Example")
    clear_string = 'stringA'
    password = "my password"
    encrypted_string = encrypt_string(clear_string, password)
    decrypted_string = decrypt_string(encrypted_string, password)
    logger.info(f"clear_string={clear_string} decrypted_string={decrypt_string} password={password}  encrypted_string={encrypted_string}")
    logger.debug("Done")

if __name__ == '__main__':
    main()
```

## Author

Name: Jordi Redondo 
Email: jordipromotions@gmail.com
git repo: https://github.com/redcorjo/pyeasyencrypt.git

## Install

pip install pyeasyencrypt


Version: 2023010803