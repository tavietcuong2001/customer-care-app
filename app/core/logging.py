import logging

# 1. Tạo một logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # Đặt mức thấp nhất cho logger

# 2. Tạo handler cho console
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG) # Xử lý tất cả các mức

# 3. Tạo handler cho file
f_handler = logging.FileHandler('error.log')
f_handler.setLevel(logging.ERROR) # Chỉ xử lý ERROR và CRITICAL

# 4. Tạo formatter và thêm vào handlers
c_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# 5. Thêm handlers vào logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)