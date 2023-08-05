from .model_detection import scrfd, retinaface_torch, retinaface_insightface, blazeface, blazeface640
from .model_landmark import tddfa, pipnet,det2d106
from .model_attribute import arcface_GenderAge,arcface_Race
from .model_recognition import arcface_modify as arcface


def get_detection_model(name,path,**kwargs):
    model=None
    if type(path)==list:
        model_format = "openvino"
    else:
        model_format = path.split(".")[-1]

    if model_format=='trt':
        print("model format error")
        return None


    if name=="scrfd":
        model = scrfd.SCRFD_CV(model_format,path,**kwargs)
    elif name=='blaze':
        isfront = kwargs.get("isfront",False)
        model = blazeface.BlazeFace(model_format,path,isfront,**kwargs)
    elif name=='blaze640':
        model = blazeface640.BlazeFace640(model_format,path,**kwargs)
    elif name=='retinaface_torch':
        model = retinaface_torch.RetinaFace(model_format,path,**kwargs)
    elif name=='retinaface_insightface':
        model = retinaface_insightface.RetinaFace(model_format,path,**kwargs)
    

    if model is None:
        print("{} is None".format(name))
        return None
    else:
        print("{} {} loaded".format(name,model_format))
        return model


def get_landmark_model(name,path,**kwargs):
    model=None
    if type(path)==list:
        model_format = "openvino"
    else:
        model_format = path.split(".")[-1]

    if model_format=='trt':
        print("model format error")
        return None

    if name=='3ddfa':
        model = tddfa.TDDFA3D_V2(model_format,path, **kwargs)
    elif name=='2d106det':
        model = det2d106.DET2D106(model_format,path,**kwargs)
    elif name in ['PIPNet','pipnet','pip','PIP']:
        model = pipnet.PIPNet(model_format,path,**kwargs)

    if model is None:
        print("{} is None".format(name))
        return None
    else:
        print("{} {} loaded".format(name,model_format))
        return model



def get_ageGender_model(name,path,out_size,**kwargs):
    model=None
    if type(path)==list:
        model_format = "openvino"
    else:
        model_format = path.split(".")[-1]

    if model_format=='trt':
        print("model format error")
        return None

    if name=='arcface_cmt':
        model = arcface_GenderAge.Arcface_GenderAge_cmt(model_format,path,out_size,**kwargs)

    if model is None:
        print("{} is None".format(name))
        return None
    else:
        print("{} {} loaded".format(name,model_format))
        return model

def get_Race_model(name,path,out_size,**kwargs):
    model=None
    if type(path)==list:
        model_format = "openvino"
    else:
        model_format = path.split(".")[-1]
        
    if model_format=='trt':
        print("model format error")
        return None

    if name=='arcface_race':
        model = arcface_Race.Arcface_Race(model_format,path,out_size,**kwargs)

    if model is None:
        print("{} is None".format(name))
        return None
    else:
        print("{} {} loaded".format(name,model_format))
        return model

def get_recognition_model(name,path,**kwargs):
    model=None
    if type(path)==list:
        model_format = "openvino"
    else:
        model_format = path.split(".")[-1]

    if model_format=='trt':
        print("model format error")
        return None
        
    if name=='arcface':

        model = arcface.Arcface(model_format,path,**kwargs)
    if model is None:
        print("{} is None".format(name))
        return None
    else:
        print("{} {} loaded".format(name,model_format))
        return model
