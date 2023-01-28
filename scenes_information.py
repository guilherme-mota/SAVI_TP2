import numpy as np

# Information about the scenes

class  Scenes:

    def __init__(self, scene):

        self.information = self.getSceneInfo(scene)


    def getSceneInfo(self, scene):

        if scene == 1: 
            dic =  {'img':'docs/rgbd-scenes-v2_imgs/scene01_img791.png',
                    'rot':np.array([0.665134, -0.0095047, -0.684383, -0.29851 ]), 
                    'trans':np.array([1.0799, -0.614107, 1.26038])}
        elif scene == 2:
            dic =  {'img':'docs/rgbd-scenes-v2_imgs/scene02_img413.png',
                    'rot':np.array([0.363794, -0.0220627, 0.875862, 0.316292 ]), 
                    'trans':np.array([-0.605352, -0.713728, 1.86245])}
        elif scene == 3:
            dic =  {'img':'docs/rgbd-scenes-v2_imgs/scene03_img0.png',
                    'rot':np.array([0, 0, 0, 1 ]), 
                    'trans':np.array([0, 0, 0])}
        elif scene == 4:
            dic =  { 'img':'docs/rgbd-scenes-v2_imgs/scene04_img0.png' }
        elif scene == 5:
            dic =  { 'img':'docs/rgbd-scenes-v2_imgs/scene05_img404.png' }
        elif scene == 6:
            dic =  { 'img':'docs/rgbd-scenes-v2_imgs/scene06_img293.png' }
        elif scene == 7:
            dic =  { 'img':'docs/rgbd-scenes-v2_imgs/scene07_img189.png' }
        elif scene == 8:
            dic =  { 'img':'docs/rgbd-scenes-v2_imgs/scene08_img345.png' }
        elif scene == 9:
            dic =  { 'img':'docs/rgbd-scenes-v2_imgs/scene09_img0.png' }
        elif scene == 10:
            dic =  { 'img':'docs/rgbd-scenes-v2_imgs/scene10_img0.png' }
        elif scene == 11:
            dic =  { 'img':'docs/rgbd-scenes-v2_imgs/scene11_img0.png' }
        elif scene == 12:
            dic =  { 'img':'docs/rgbd-scenes-v2_imgs/scene12_img175.png' }
        elif scene == 13:
            dic =  { 'img':'docs/rgbd-scenes-v2_imgs/scene13_img205.png' }
        elif scene == 14:
            dic =  { 'img':'docs/rgbd-scenes-v2_imgs/scene14_img0.png' }
        else:
            raise ValueError('Unknown Scene')

        return dic
