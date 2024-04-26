from enum import Enum

class OperationType(Enum):
    CONVERTION_COLOR = "Conversão de cor"
    FILTER = "Filtros"
    EDGE_DETECTOR = "Detector de bordas"
    BINARIZATION = "Binarização"
    MATH_MORPH = "Morfologia matemática"
