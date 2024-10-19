IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720

# Параметры модели
NUM_CLASSES = 8
CONFIDENCE_THRESHOLD = 0.5  # порог уверенности для предсказаний
NMS_THRESHOLD = 0.4  # порог Non-Maximum Suppression

TRAIN_IMAGES_PATH = 'data/images/train/'
TRAIN_LABELS_PATH = 'data/labels/train/'
TEST_IMAGES_PATH = 'data/images/test/'
TEST_LABELS_PATH = 'data/labels/test/'


# Другие параметры
BATCH_SIZE = 16
LEARNING_RATE = 0.001          #скорость обучения
EPOCHS = 16
