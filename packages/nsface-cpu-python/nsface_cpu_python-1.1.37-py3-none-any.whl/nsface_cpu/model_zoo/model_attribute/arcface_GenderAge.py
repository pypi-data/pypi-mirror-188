from sklearn.metrics import mean_absolute_error

import cv2

import numpy as np

from ...utils.util_warp import face_align
from ...utils.util_attribute import get_pred
from ...data.constant import LMARK_REF_ARC

from ..model_common import load_onnx, load_openvino


gender_dict={0:'F',1:'M'}


class Arcface_GenderAge_cmt:
    def __init__(self,model_type,model_path,out_size=112,**kwargs):
        self.model_path = model_path
        self.out_size=out_size
        self.model_type=model_type

        if self.model_type=='onnx':
            self.net = load_onnx.Onnx_session(self.model_path,input_mean=0.0, input_std=1.0,onnx_device='cpu')
        elif self.model_type=='openvino':
            self.net = load_openvino.Openvino(self.model_path,device='CPU')

    def get(self,img,face,to_bgr):
        if not 'aimg' in face.keys():
            aimg = face_align(img,LMARK_REF_ARC,face.land5,self.out_size)
            face.aimg = aimg
        else:
            aimg = face.aimg

        if self.model_type=='onnx':
            aimg = (aimg/255. - 0.5)/0.5

        #gender_outs, age_outs = self.net(aimg)
        output = self.net(aimg)
        if output[0].shape==(1,2):
            gender_outs=output[0]
            age_outs=output[1]
        else:
            gender_outs=output[1]
            age_outs=output[0]

        pred_g,pred_a,sf_gender = get_pred(gender_outs,age_outs)
        face.gender = gender_dict[pred_g]
        face.age = pred_a
        face.gender_sf = sf_gender

        return face.gender, face.age, face.gender_sf







        

    









