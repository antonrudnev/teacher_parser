# MONGO_HOST = "54.89.173.224"
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DATABASE = "teacher_db"
MONGO_COLLECTION = "pages"

PAGE_SERVER_URL = "http://ec2-52-90-158-67.compute-1.amazonaws.com:28888/"


EMAIL_PATTERN = r"[a-z0-9_.-]+@(?:[a-z0-9_-]+\.)+[a-z]+"
PHONE_PATTERN = r"(\+?\d?[\( -]{0,2}\d{3}[\) -]{0,2}\d{3}[ -]?\d{2}[ -]?\d{2}|\be?x?\.?\s?\d{4})"
SCHOOL_NAME_PATTERN = r"(?:(?:[A-Z][A-Za-z.-]+)%EDGE_PATTERN%\s)+(?:School|Elementary|Academy)"
SCHOOL_NAME_BLACKLIST = ["Middle School", "High School"]
SCHOOL_NAME_EDGE_WORDS = ["A", "About", "After", "Also", "An", "As", "Before", "Bus", "Email", "My", "No", "Our",
                          "Safe", "Sister", "Summer", "The", "Your", "Will"]


STANFORD_LNG_MODEL_PATH = "resources/stanford-ner-3.9.1/classifiers/english.all.3class.distsim.crf.ser.gz"
STANFORD_NER_PATH = "resources/stanford-ner-3.9.1/stanford-ner.jar"
NOT_A_NAME_DICTIONARY_PATH = "resources/not_a_name.dic"

MAX_PAGE_SIZE = 4700000  # MacOS 16Gb RAM
WORKERS = 3  # scaling factor
MIN_CONF_EXPORT = 0.3  # default threshold for confidence score to export
