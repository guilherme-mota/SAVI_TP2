import numpy as np

# Information about the diferent scenes
class  Scenes:

    def __init__(self, scene):

        self.information = self.getSceneInfo(scene)


    def getSceneInfo(self, scene):

        if scene == 1: 
            dic =  {'pcd':'docs/rgbd-scenes-v2_pc/rgbd-scenes-v2/pc/01.pcd',
                    'img':'docs/rgbd-scenes-v2_imgs/scene01_img791.png',
                    'rot':np.array([0.665134, -0.0095047, -0.684383, -0.29851 ]), 
                    'trans':np.array([1.0799, -0.614107, 1.26038])}
        elif scene == 2:
            dic =  {'pcd':'docs/rgbd-scenes-v2_pc/rgbd-scenes-v2/pc/02.pcd',
                    'img':'docs/rgbd-scenes-v2_imgs/scene02_img413.png',
                    'rot':np.array([0.363794, -0.0220627, 0.875862, 0.316292 ]), 
                    'trans':np.array([-0.605352, -0.713728, 1.86245])}
        elif scene == 3:
            dic =  {'pcd':'docs/rgbd-scenes-v2_pc/rgbd-scenes-v2/pc/03.pcd',
                    'img':'docs/rgbd-scenes-v2_imgs/scene03_img0.png',
                    'rot':np.array([0, 0, 0, 1 ]), 
                    'trans':np.array([0, 0, 0])}
        elif scene == 4:
            dic =  {'pcd':'docs/rgbd-scenes-v2_pc/rgbd-scenes-v2/pc/04.pcd',
                    'img':'docs/rgbd-scenes-v2_imgs/scene04_img0.png',
                    'rot':np.array([0, 0, 0, 1 ]), 
                    'trans':np.array([0, 0, 0])}
        elif scene == 5:
            dic =  {'pcd':'docs/rgbd-scenes-v2_pc/rgbd-scenes-v2/pc/05.pcd',
                    'img':'docs/rgbd-scenes-v2_imgs/scene05_img404.png',
                    'rot':np.array([0.92118, 0.00982951, -0.355027, -0.15905]), 
                    'trans':np.array([1.96118, -0.200736, 0.341896])}
        elif scene == 6:
            dic =  {'pcd':'docs/rgbd-scenes-v2_pc/rgbd-scenes-v2/pc/06.pcd',
                    'img':'docs/rgbd-scenes-v2_imgs/scene06_img293.png',
                    'rot':np.array([0.979517, 0.0453742, -0.184894, -0.0656378 ]), 
                    'trans':np.array([1.35475, -0.174762, 0.481929])}
        elif scene == 7:
            dic =  {'pcd':'docs/rgbd-scenes-v2_pc/rgbd-scenes-v2/pc/07.pcd',
                    'img':'docs/rgbd-scenes-v2_imgs/scene07_img189.png',
                    'rot':np.array([0.973754, -0.0190409, -0.217644, -0.0637781]), 
                    'trans':np.array([1.34061, -0.397391, 0.174681])}
        elif scene == 8:
            dic =  {'pcd':'docs/rgbd-scenes-v2_pc/rgbd-scenes-v2/pc/08.pcd',
                    'img':'docs/rgbd-scenes-v2_imgs/scene08_img345.png',
                    'rot':np.array([0.742083, 0.0185494, -0.624903 ,-0.241816 ]), 
                    'trans':np.array([2.16656, -0.664954, 0.929348])}
        elif scene == 9:
            dic =  {'pcd':'docs/rgbd-scenes-v2_pc/rgbd-scenes-v2/pc/09.pcd',
                    'img':'docs/rgbd-scenes-v2_imgs/scene09_img0.png',
                    'rot':np.array([0, 0, 0, 1 ]), 
                    'trans':np.array([0, 0, 0])}
        elif scene == 10:
            dic =  {'pcd':'docs/rgbd-scenes-v2_pc/rgbd-scenes-v2/pc/10.pcd',
                    'img':'docs/rgbd-scenes-v2_imgs/scene10_img0.png',
                    'rot':np.array([0, 0, 0, 1 ]), 
                    'trans':np.array([0, 0, 0])}
        elif scene == 11:
            dic =  {'pcd':'docs/rgbd-scenes-v2_pc/rgbd-scenes-v2/pc/11.pcd',
                    'img':'docs/rgbd-scenes-v2_imgs/scene11_img0.png',
                    'rot':np.array([0, 0, 0, 1 ]), 
                    'trans':np.array([0, 0, 0])}
        elif scene == 12:
            dic =  {'pcd':'docs/rgbd-scenes-v2_pc/rgbd-scenes-v2/pc/12.pcd',
                    'img':'docs/rgbd-scenes-v2_imgs/scene12_img175.png',
                    'rot':np.array([0.930567, 0.0542049, 0.321128, 0.167272 ]), 
                    'trans':np.array([-0.582299, -0.332549, 0.404767])}
        elif scene == 13:
            dic =  {'pcd':'docs/rgbd-scenes-v2_pc/rgbd-scenes-v2/pc/13.pcd',
                    'img':'docs/rgbd-scenes-v2_imgs/scene13_img205.png',
                    'rot':np.array([0.981403, 0.0858466, 0.123505, 0.11925]), 
                    'trans':np.array([-0.343344, -0.626815, 0.515212])}
        elif scene == 14:
            dic =  {'pcd':'docs/rgbd-scenes-v2_pc/rgbd-scenes-v2/pc/14.pcd',
                    'img':'docs/rgbd-scenes-v2_imgs/scene14_img0.png',
                    'rot':np.array([0, 0, 0, 1 ]), 
                    'trans':np.array([0, 0, 0])}
        else:
            raise ValueError('Unknown Scene')

        return dic
