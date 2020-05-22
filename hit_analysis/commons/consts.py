# original fields of detection from JSON
ID = 'id'
DEVICE_ID = 'device_id'
TIMESTAMP = 'timestamp'

WIDTH = 'width'
HEIGHT = 'height'

X = 'x'
Y = 'y'

FRAME_CONTENT = 'frame_content'  # excluded in CSV


# added fields by processing functions (all excluded in CSV)
FRAME_DECODED = 'frame_decoded'
IMAGE = 'image'

# image basic stats
DARKNESS = 'image_darkness'  # bright of darkness pixel (0-255)
BRIGHTEST = 'image_brightest'  # bright of brightest pixel (0-255)
BRIGHTER_COUNT = 'image_brighter_count_%03d'  # count of pixels brighter or equal than %03d

# reconstruction dark filled area
EDGE = 'edge'
CROP_X = 'crop_x'
CROP_Y = 'crop_y'
CROP_SIZE = 'crop_size'

# classification
CLASSIFIED = 'classified'  # result of classification
CLASS_ARTIFACT = 'artifact'

# artifact filter values
ARTIFACT_TOO_OFTEN = 'artifact_too_often'  # count of occurrences for too_often filter
ARTIFACT_HOT_PIXEL = 'artifact_hot_pixel'  # count of occurrences for hot_pixel filter
ARTIFACT_NEAR_HOT_PIXEL = 'artifact_near_hot_pixel'  # count of occurrences for near_hot_pixel filter
ARTIFACT_NEAR_HOT_PIXEL_REFXY = 'artifact_near_hot_pixel_refxy'  # reference XY for near_hot_pixel, all hot pixels in radius to this XY are classified as near hot pixel, default radius: 5px
ARTIFACT_TOO_DARK = 'artifact_too_dark'  # BRIGHTEST - DARKNESS
ARTIFACT_TOO_LARGE_BRIGHT_AREA = 'artifact_too_large_bright_area'  # BRIGHTER_COUNT * 1000 / (WIDTH * HEIGHT) for used brighter threshold, default threshold: (BRIGHTEST - DARKNESS) / 4 + DARKNESS
