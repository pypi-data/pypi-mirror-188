"""Mappings between cell type indices and corresponding names"""


# We use the cell types as defined/used by VTK
# https://vtk.org/doc/nightly/html/vtkCellType_8h_source.html
_CELL_TYPE_INDEX_TO_STR = {
    0: "EMPTY_CELL",
    1: "VERTEX",
    2: "POLY_VERTEX",
    3: "LINE",
    4: "POLY_LINE",
    5: "TRIANGLE",
    6: "TRIANGLE_STRIP",
    7: "POLYGON",
    8: "PIXEL",
    9: "QUAD",
    10: "TETRA",
    11: "VOXEL",
    12: "HEXAHEDRON",
    13: "WEDGE",
    14: "PYRAMID",
    15: "PENTAGONAL_PRISM",
    16: "HEXAGONAL_PRISM",
    21: "QUADRATIC_EDGE",
    22: "QUADRATIC_TRIANGLE",
    23: "QUADRATIC_QUAD",
    36: "QUADRATIC_POLYGON",
    24: "QUADRATIC_TETRA",
    25: "QUADRATIC_HEXAHEDRON",
    26: "QUADRATIC_WEDGE",
    27: "QUADRATIC_PYRAMID",
    28: "BIQUADRATIC_QUAD",
    29: "TRIQUADRATIC_HEXAHEDRON",
    37: "TRIQUADRATIC_PYRAMID",
    30: "QUADRATIC_LINEAR_QUAD",
    31: "QUADRATIC_LINEAR_WEDGE",
    32: "BIQUADRATIC_QUADRATIC_WEDGE",
    33: "BIQUADRATIC_QUADRATIC_HEXAHEDRON",
    34: "BIQUADRATIC_TRIANGLE",
    35: "CUBIC_LINE",
    41: "CONVEX_POINT_SET",
    42: "POLYHEDRON",
    51: "PARAMETRIC_CURVE",
    52: "PARAMETRIC_SURFACE",
    53: "PARAMETRIC_TRI_SURFACE",
    54: "PARAMETRIC_QUAD_SURFACE",
    55: "PARAMETRIC_TETRA_REGION",
    56: "PARAMETRIC_HEX_REGION",
    60: "HIGHER_ORDER_EDGE",
    61: "HIGHER_ORDER_TRIANGLE",
    62: "HIGHER_ORDER_QUAD",
    63: "HIGHER_ORDER_POLYGON",
    64: "HIGHER_ORDER_TETRAHEDRON",
    65: "HIGHER_ORDER_WEDGE",
    66: "HIGHER_ORDER_PYRAMID",
    67: "HIGHER_ORDER_HEXAHEDRON",
    68: "LAGRANGE_CURVE",
    69: "LAGRANGE_TRIANGLE",
    70: "LAGRANGE_QUADRILATERAL",
    71: "LAGRANGE_TETRAHEDRON",
    72: "LAGRANGE_HEXAHEDRON",
    73: "LAGRANGE_WEDGE",
    74: "LAGRANGE_PYRAMID",
    75: "BEZIER_CURVE",
    76: "BEZIER_TRIANGLE",
    77: "BEZIER_QUADRILATERAL",
    78: "BEZIER_TETRAHEDRON",
    79: "BEZIER_HEXAHEDRON",
    80: "BEZIER_WEDGE",
    81: "BEZIER_PYRAMID",
}

_CELL_TYPE_STR_TO_INDEX = {v: k for k, v in _CELL_TYPE_INDEX_TO_STR.items()}
