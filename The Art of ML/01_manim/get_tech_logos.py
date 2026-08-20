from manim import *

def get_tech_logos(self):
    python_path = "python_logo.svg"
    pytorch_path = "pytorch_logo.svg"
            
    py_img = SVGMobject(python_path)
    pt_img = SVGMobject(pytorch_path)
            
    py_img.height = 1.0
    pt_img.height = 1.0

    if len(py_img) >= 2:
        py_img[0].set_color("#306998")  
        py_img[1].set_color("#FFD43B")  
    else:
        py_img.set_color_by_gradient("#306998", "#FFD43B")

    return VGroup(py_img, pt_img).arrange(RIGHT, buff=0.8)