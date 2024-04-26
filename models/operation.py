from utils.operation_type import OperationType
import cv2

class Operation:
    def __init__(self, display_name, input_parameters, parameters, type, method) -> None:
        self.display_name : str = display_name
        self.input_parameters : list = input_parameters
        self.parameters : list = parameters
        self.type : OperationType = type
        self.method : any = method
        self.image : any = None
        
    def get_display_name(self):
        if hasattr(self, 'input_values'):
            parameters = ", ".join([f"{name}: {self.input_values[name]}" for name in self.input_parameters])
        elif self.input_parameters:
            parameters = ", ".join(self.input_parameters)
            return f"{self.display_name} [{parameters}]"
        else:
            return self.display_name
    
    def apply_method(self):
        if self.method == cv2.cvtColor and self.parameters:
            self.method = lambda: cv2.cvtColor(self.image, self.parameters[0])


operation_list = {
    OperationType.CONVERTION_COLOR: [
        Operation("RGB para Cinza", None, [cv2.COLOR_RGB2GRAY],  OperationType.CONVERTION_COLOR, cv2.cvtColor),
        Operation("RGB para HSV",   None, [cv2.COLOR_RGB2HSV], OperationType.CONVERTION_COLOR, cv2.cvtColor),
        Operation("RGB para XYZ",   None, [cv2.COLOR_RGB2XYZ], OperationType.CONVERTION_COLOR, cv2.cvtColor),
        Operation("RGB para Luv",   None, [cv2.COLOR_RGB2Luv], OperationType.CONVERTION_COLOR, cv2.cvtColor),
    ],
    OperationType.FILTER: [
        Operation("Filtro de gaussiano", ["Kernel Size", "SigmaX"], [], OperationType.FILTER, None),
        Operation("Filtro de blur", ["Kernel Size"], [], OperationType.FILTER, None),
        Operation("Filtro bilateral", ["Diametro", "sigmaColor", "sigmaSpace"], [], OperationType.FILTER, None),
    ],
    OperationType.EDGE_DETECTOR: [
        Operation("Detecção de bordas Canny", [], [], OperationType.EDGE_DETECTOR, None),
        Operation("Detecção de bordas Sobel", [], [], OperationType.EDGE_DETECTOR, None),
        Operation("Detecção de bordas Laplaciano", [], [], OperationType.EDGE_DETECTOR, None),
    ],
    OperationType.BINARIZATION: [
        Operation("Limiarização simples", [], [], OperationType.BINARIZATION, None),
        Operation("Limiarização adaptativa", [], [], OperationType.BINARIZATION, None),
    ],
    OperationType.MATH_MORPH: [
        Operation("Erosão", [], [], OperationType.MATH_MORPH, None),
        Operation("Dilatação", [], [], OperationType.MATH_MORPH, None),
        Operation("Abertura", [], [], OperationType.MATH_MORPH, None),
        Operation("Fechamento", [], [], OperationType.MATH_MORPH, None),
    ],
}