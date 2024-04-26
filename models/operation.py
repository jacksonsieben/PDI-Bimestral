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
        if self.parameters:
            # if self.method == cv2.cvtColor:
            self.method = lambda: self.method(self.image, self.parameters[0])


operation_list = {
    OperationType.CONVERTION_COLOR: [
        Operation("RGB para Cinza", None, [cv2.COLOR_RGB2GRAY],  OperationType.CONVERTION_COLOR, cv2.cvtColor),
        Operation("RGB para HSV",   None, [cv2.COLOR_RGB2HSV], OperationType.CONVERTION_COLOR, cv2.cvtColor),
        Operation("RGB para XYZ",   None, [cv2.COLOR_RGB2XYZ], OperationType.CONVERTION_COLOR, cv2.cvtColor),
        Operation("RGB para Luv",   None, [cv2.COLOR_RGB2Luv], OperationType.CONVERTION_COLOR, cv2.cvtColor),
    ],
    OperationType.FILTER: [
        Operation("Filtro de gaussiano", ["Kernel Size", "SigmaX"], [], OperationType.FILTER, cv2.GaussianBlur),
        Operation("Filtro de blur", ["Kernel Size"], [], OperationType.FILTER, cv2.blur),
        Operation("Filtro bilateral", ["Diametro", "sigmaColor", "sigmaSpace"], [], OperationType.FILTER, cv2.bilateralFilter),
    ],
    OperationType.EDGE_DETECTOR: [
        Operation("Detecção de bordas Canny", ["threshold1", "threshold2"], [], OperationType.EDGE_DETECTOR, cv2.Canny),
        Operation("Detecção de bordas Sobel", ["dx", "dy", "ksize"], [], OperationType.EDGE_DETECTOR, cv2.Sobel),
        Operation("Detecção de bordas Laplaciano", ["ddepth", "ksize"], [], OperationType.EDGE_DETECTOR, cv2.Laplacian),
    ],
    OperationType.BINARIZATION: [
        Operation("Limiarização simples", ["thresh", "maxval"], [], OperationType.BINARIZATION, cv2.threshold),
        Operation("Limiarização adaptativa", ["maxval", "adaptiveMethod", "thresholdType", "blockSize", "C"], [], OperationType.BINARIZATION, cv2.adaptiveThreshold),
    ],
    OperationType.MATH_MORPH: [
        Operation("Erosão", ["kernel"], [], OperationType.MATH_MORPH, cv2.erode),
        Operation("Dilatação", ["kernel"], [], OperationType.MATH_MORPH, cv2.dilate),
        Operation("Abertura", ["kernel"], [], OperationType.MATH_MORPH, cv2.morphologyEx),
        Operation("Fechamento", ["kernel"], [], OperationType.MATH_MORPH, cv2.morphologyEx),
    ],
}