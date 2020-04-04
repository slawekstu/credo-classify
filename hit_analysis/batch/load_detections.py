from typing import List

from hit_analysis.classification.artifact.hot_pixel import group_for_hot_pixel, hot_pixel_process
from hit_analysis.classification.artifact.near_hot_pixel import near_hot_pixel_process, group_for_near_hot_pixel
from hit_analysis.classification.artifact.too_dark import too_dark
from hit_analysis.classification.artifact.too_large_bright_area import too_large_bright_area
from hit_analysis.classification.artifact.too_often import group_for_too_often, too_often_process
from hit_analysis.commons.config import Config
from hit_analysis.commons.consts import CLASSIFIED, CLASS_ARTIFACT, DEVICE_ID, FRAME_DECODED, ARTIFACT_NEAR_HOT_PIXEL_REFXY, X, Y, ARTIFACT_HOT_PIXEL, \
    ARTIFACT_NEAR_HOT_PIXEL, ID, ARTIFACT_TOO_OFTEN, TIMESTAMP, ARTIFACT_TOO_DARK, ARTIFACT_TOO_LARGE_BRIGHT_AREA, FRAME_CONTENT
from hit_analysis.commons.grouping import group_by_device_id
from hit_analysis.commons.utils import get_resolution_key, join_tuple
from hit_analysis.image.cut_reconstruction import check_all_artifacts, do_reconstruct
from hit_analysis.image.image_utils import load_image
from hit_analysis.io.io_utils import decode_base64


def store_debug_pngs(detections, config: Config):
    if not config.out_dir:
        return

    timing = config.print_log('store debug PNGs...')

    for d in detections:
        _id = d.get(ID)
        kd = d.get(DEVICE_ID)
        img = d.get(FRAME_DECODED) or decode_base64(d.get(FRAME_CONTENT))

        if d.get(CLASSIFIED) == CLASS_ARTIFACT:
            rk = get_resolution_key(d)
            rk_str = join_tuple(rk)
            xyk = (d.get(X), d.get(Y))
            xyk_str = join_tuple(xyk)

            if d.get(ARTIFACT_HOT_PIXEL):
                config.store_png(['rejected', 'by_hot_pixel', str(kd), rk_str, xyk_str], _id, img)
                config.store_png(['rejected', 'by_hot_pixel', 'by_count', str(d.get(ARTIFACT_HOT_PIXEL))], _id, img)

            if d.get(ARTIFACT_NEAR_HOT_PIXEL):
                near_xyk = d.get(ARTIFACT_NEAR_HOT_PIXEL_REFXY)
                near_xyk_str = join_tuple(near_xyk)
                config.store_png(['rejected', 'by_near_hot_pixel', str(kd), rk_str, near_xyk_str], _id, img)
                config.store_png(['rejected', 'by_near_hot_pixel', 'by_count', str(d.get(ARTIFACT_NEAR_HOT_PIXEL))], _id, img)

            if d.get(ARTIFACT_TOO_OFTEN):
                config.store_png(['rejected', 'by_too_often', str(kd), str(d.get(TIMESTAMP) // config.too_often_time_division)], _id, img)
                config.store_png(['rejected', 'by_too_often', 'by_count', str(d.get(ARTIFACT_TOO_OFTEN))], _id, img)

            if d.get(ARTIFACT_TOO_DARK):
                n = '%d_%d' % (d.get(ARTIFACT_TOO_DARK), _id)
                config.store_png(['rejected', 'by_too_dark', str(kd)], n, img)
                config.store_png(['rejected', 'by_too_dark'], n, img)
            if d.get(ARTIFACT_TOO_LARGE_BRIGHT_AREA):
                n = '%d_%d' % (d.get(ARTIFACT_TOO_LARGE_BRIGHT_AREA), _id)
                config.store_png(['rejected', 'by_too_large_bright_area', str(kd)], n, img)
                config.store_png(['rejected', 'by_too_large_bright_area'], n, img)

        else:
            config.store_png(['accepted', str(kd)], _id, img)
            config.store_png(['accepted', d.get('class') or 'unclassified'], _id, img)

    config.print_log('... done', timing)


def filter_artifacts_and_reconstruct(detections: List[dict], config: Config) -> None:
    timing = config.print_log('hot_pixel filter with hot_pixel_often=%d...' % config.hot_pixel_often)
    hot_pixel_process(group_for_hot_pixel(detections), config.hot_pixel_often)
    config.print_log('... hot_pixel done', timing)

    timing = config.print_log('near_hot_pixel filter with near_hot_pixel_often=%d, near_hot_pixel_distance=%d...' % (config.near_hot_pixel_often, config.near_hot_pixel_distance))
    near_hot_pixel_process(group_for_near_hot_pixel(detections, config.near_hot_pixel_distance), config.near_hot_pixel_often)
    config.print_log('... near_hot_pixel done', timing)

    timing = config.print_log('too_often filter with too_often=%d...' % config.too_often)
    by_minute_by_timestamp = group_for_too_often(detections, config.too_often_time_division)
    too_often_process(by_minute_by_timestamp, config.too_often)
    config.print_log('... too_often done', timing)

    timing = config.print_log('reconstruct black fills...')
    for minute, by_timestamp in by_minute_by_timestamp.items():
        for timestamp, dcs in by_timestamp.items():
            if len(dcs) > 1 and not check_all_artifacts(dcs):
                timing2 = config.print_log(' reconstruct black fills for timestamp %d...' % timestamp)
                do_reconstruct(dcs, config)
                config.print_log(' ... reconstruct done', timing2)
    config.print_log('... reconstruct black fills done', timing)


def image_simple_classify(detections: List[dict], config: Config) -> None:
    timing = config.print_log('simple classify...')
    count = 0
    for d in detections:
        do_process = True
        if config.simple_classify_ignore_artifacts and d.get(CLASSIFIED) == CLASS_ARTIFACT:
            do_process = False

        if do_process:
            too_dark(d, config.too_dark_spread)
            too_large_bright_area_threshold = config.too_large_bright_area_threshold
            too_large_bright_area(d, too_large_bright_area_threshold(detection=d), config.too_large_bright_area_bac)
            count += 1
    config.print_log('... simple classify %d done' % count, timing)


def analyse_detections_batch(detections: List[dict], config: Config) -> None:
    timing = timing_full = config.print_log('Load detections batch for %d detections...' % len(detections))

    config.change_log_indent(1)
    by_device_id = group_by_device_id(detections)
    config.print_log('... grouped by device_id...', timing)
    for device_id, dcs in by_device_id.items():
        timing = config.print_log('Processing for device_id %d...' % device_id)

        config.change_log_indent(1)
        filter_artifacts_and_reconstruct(dcs, config)
        image_simple_classify(dcs, config)
        store_debug_pngs(dcs, config)
        config.change_log_indent(-1)

        config.print_log('... processing for device_id %d done' % device_id, timing)

    config.change_log_indent(-1)

    config.print_log('... load detections batch finish', timing_full)