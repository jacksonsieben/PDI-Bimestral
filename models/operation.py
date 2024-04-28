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
        else:
            return self.display_name
    
    def apply_method(self, image):
        if self.parameters and image is not None:
            if self.type != OperationType.EDGE_DETECTOR:
                self.image = self.method(image, *self.parameters)
                self.image = self.image if not isinstance(self.image, tuple) else self.image[1]
                return self.image
            elif self.display_name == "Detecção de bordas Canny":
                self.image = self.method(image, *self.parameters)
                return self.image
            else:
                if self.display_name == "Detecção de bordas Sobel":
                    x = self.method(image, self.parameters[0], 1, 0, self.parameters[3])
                    y = self.method(image, self.parameters[0], 0, 1, self.parameters[3])
                    image = cv2.magnitude(x, y)
                else:
                    image = self.method(image, *self.parameters)
                
                self.image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
                
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
        Operation("Filtro de gaussiano", ["Kernel Size", "SigmaX"], [None,None], OperationType.FILTER, cv2.GaussianBlur),
        Operation("Filtro de blur", ["Kernel Size"], [None], OperationType.FILTER, cv2.blur),
        Operation("Filtro bilateral", ["Diametro", "sigmaColor", "sigmaSpace"], [None,None,None], OperationType.FILTER, cv2.bilateralFilter),
    ],
    OperationType.EDGE_DETECTOR: [
        Operation("Detecção de bordas Canny", ["threshold1", "threshold2"], [None,None], OperationType.EDGE_DETECTOR, cv2.Canny),
        Operation("Detecção de bordas Sobel", [None, None, None, "ksize"], [cv2.CV_64F,None,None,None], OperationType.EDGE_DETECTOR, cv2.Sobel),
        Operation("Detecção de bordas Laplaciano", [None, "ksize"], [cv2.CV_64F,None], OperationType.EDGE_DETECTOR, cv2.Laplacian),
    ],
    OperationType.BINARIZATION: [
        Operation("Limiarização simples", ["thresh", "maxval"], [None,None,cv2.THRESH_BINARY], OperationType.BINARIZATION, cv2.threshold),
        Operation("Limiarização adaptativa", ["maxval", None, None, "blockSize", "C"], [None, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, None, None], OperationType.BINARIZATION, cv2.adaptiveThreshold),
    ],
    OperationType.MATH_MORPH: [
        Operation("Erosão", ["Kernel Size"], [None], OperationType.MATH_MORPH, cv2.erode),
        Operation("Dilatação", ["Kernel Size"], [None], OperationType.MATH_MORPH, cv2.dilate),
        Operation("Abertura", [None, "Kernel Size"], [cv2.MORPH_OPEN, None], OperationType.MATH_MORPH, cv2.morphologyEx),
        Operation("Fechamento", [None, "Kernel Size"], [cv2.MORPH_CLOSE, None], OperationType.MATH_MORPH, cv2.morphologyEx),
    ],
}