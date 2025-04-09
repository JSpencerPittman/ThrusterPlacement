from typing import Callable
import numpy as np
import cv2

from tp.entity import Hull
from tp.util import millimeters, Polygon, Rectangle, Point


def calc_cross_sec_area_of_submerged_hull(hull: Hull,
                                          submerged_depth: millimeters):
    def polygon_to_contour(polygon: Polygon) -> np.ndarray:
        return np.array([(point.x, point.y) for point in polygon])

    def calc_polygon_bounding_box(polygon: Polygon) -> Rectangle:
        poly_cnt = polygon_to_contour(polygon)
        return Rectangle(*cv2.boundingRect(poly_cnt))

    def find_closest_vertex_on_y_axis_in_filt_points(
            tgt_y: float,
            filt_func: Callable[[Point], bool]) -> Point:
        filt_vtxs = [vtx
                     for vtx in hull.cross_sec_shape
                     if filt_func(vtx)]
        return sorted(filt_vtxs,
                      key=lambda point: abs(point.y - tgt_y))[0]

    def line_equation_from_line_seg_points(p1: Point, p2: Point
                                           ) -> tuple[float, float]:
        rise = p2.y - p1.y
        run = p2.x - p1.x
        slope = rise / run
        intercept = p1.y - (slope * p1.x)
        return slope, intercept

    bbox = calc_polygon_bounding_box(hull.cross_sec_shape)
    water_level = bbox.bottom + submerged_depth

    # TODO: take advantage of counter-clockwise restriction to simplify algorithm

    # Identify where the hull cross section is intersected by the line representing water level
    intersect_left_line_seg_bot = find_closest_vertex_on_y_axis_in_filt_points(
        water_level,
        lambda point: point.y <= water_level and point.x < 0
    )
    intersect_left_line_seg_top = find_closest_vertex_on_y_axis_in_filt_points(
        water_level,
        lambda point: point.y > water_level and point.x < 0
    )
    intersect_right_line_seg_bot = find_closest_vertex_on_y_axis_in_filt_points(
        water_level,
        lambda point: point.y <= water_level and point.x > 0
    )
    intersect_right_line_seg_top = find_closest_vertex_on_y_axis_in_filt_points(
        water_level,
        lambda point: point.y > water_level and point.x > 0
    )

    left_line_seg_slope, left_line_seg_intercept = \
        line_equation_from_line_seg_points(intersect_left_line_seg_bot,
                                           intersect_left_line_seg_top)
    right_line_seg_slope, right_line_seg_intercept = \
        line_equation_from_line_seg_points(intersect_right_line_seg_bot,
                                           intersect_right_line_seg_top)

    left_intersect = Point((water_level - left_line_seg_intercept) / left_line_seg_slope,
                           water_level)
    right_intersect = Point((water_level - right_line_seg_intercept) / right_line_seg_slope,
                            water_level)

    """
    Now we need to create a new contour representing the submerged cross section of the hull
    1. Remove points above the water level.
    2. Insert the points in the correct spot of the remaining contour.
    """
    # <= was not used to prevent duplicate points at the intersection
    below_water_poly = [vtx
                        for vtx in hull.cross_sec_shape
                        if vtx.y < water_level] 
    submerged_poly = [right_intersect, left_intersect] + below_water_poly
    submerged_cnt = polygon_to_contour(submerged_poly)
    return cv2.contourArea(submerged_cnt)
