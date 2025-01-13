from settings import Settings
from file_handler import FileHandler

settings = Settings()

# fail for file
try:
    section = settings.read_sections("../settings.config", "files")
    print(section)
except Exception:
    print("Exception raise for file")
    pass

# fail for section
try:
    section = settings.read_sections("settings.config", "pizza")
    print(section)
except Exception:
    print("Exception raise for section")
    pass

# pass
section = settings.read_sections("settings.config", "files")
print(section)

fh = FileHandler()

# read file fail
try:
    fh.read_file("pizza.txt")
except Exception:
    print("File Not Found")
    pass

# read file pass
fh.read_file("settings.config")