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
            parameters = ", ".join([f"{name}: {self.input_values[name]}" for name in self.input_parameters if name is not None])
            return f"{self.display_name} [{parameters}]"
        elif self.input_parameters:
            parameters = ", ".join(self.input_parameters)
            return f"{self.display_name} [{parameters}]"
        else:
            return self.display_name
    
    def apply_method(self, image):
        if self.parameters and image is not None:
            self.image = self.method(image, *self.parameters)
            self.image = self.image if not isinstance(self.image, tuple) else self.image[1]
            return self.image
        else:
            print("Operação sem parâmetros ou imagem não carregada")


operation_list = {
    OperationType.CONVERTION_COLOR: [
        Operation("RGB para Cinza", None, [cv2.COLOR_RGB2GRAY],  OperationType.CONVERTION_COLOR, cv2.cvtColor),
        Operation("RGB para HSV",   None, [cv2.COLOR_RGB2HSV], OperationType.CONVERTION_COLOR, cv2.cvtColor),
        Operation("RGB para XYZ",   None, [cv2.COLOR_RGB2XYZ], OperationType.CONVERTION_COLOR, cv2.cvtColor),
        Operation("RGB para Luv",   None, [cv2.COLOR_RGB2Luv], OperationType.CONVERTION_COLOR, cv2.cvtColor),
    ],
    OperationType.FILTER: [
        Operation("Filtro de gaussiano", ["Kernel Size", "SigmaX"], [0,0], OperationType.FILTER, cv2.GaussianBlur),
        Operation("Filtro de blur", ["Kernel Size"], [0], OperationType.FILTER, cv2.blur),
        Operation("Filtro bilateral", ["Diametro", "sigmaColor", "sigmaSpace"], [0,0,0], OperationType.FILTER, cv2.bilateralFilter),
    ],
    OperationType.EDGE_DETECTOR: [
        Operation("Detecção de bordas Canny", ["threshold1", "threshold2"], [0,0], OperationType.EDGE_DETECTOR, cv2.Canny),
        Operation("Detecção de bordas Sobel", ["dx", "dy", "ksize"], [0,0,0], OperationType.EDGE_DETECTOR, cv2.Sobel),
        Operation("Detecção de bordas Laplaciano", ["ddepth", "ksize"], [0,0], OperationType.EDGE_DETECTOR, cv2.Laplacian),
    ],
    OperationType.BINARIZATION: [
        Operation("Limiarização simples", ["thresh", "maxval"], [0,0,cv2.THRESH_BINARY], OperationType.BINARIZATION, cv2.threshold),
        Operation("Limiarização adaptativa", ["maxval", None, None, "blockSize", "C"], [0, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 0, 0], OperationType.BINARIZATION, cv2.adaptiveThreshold),
    ],
    OperationType.MATH_MORPH: [
        Operation("Erosão", ["Kernel Size"], [0], OperationType.MATH_MORPH, cv2.erode),
        Operation("Dilatação", ["Kernel Size"], [0], OperationType.MATH_MORPH, cv2.dilate),
        Operation("Abertura", ["Kernel Size"], [0], OperationType.MATH_MORPH, cv2.morphologyEx),
        Operation("Fechamento", ["Kernel Size"], [0], OperationType.MATH_MORPH, cv2.morphologyEx),
    ],
}