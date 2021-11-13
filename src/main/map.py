import sys

sys.path.append("../utils/")
import graphicUtils

class map:
    def __init__(self):
        self.distance_map = {"Cloak_Room_Entry": graphicUtils.Cloak_Room_Entry(),
                             "Kitchen": graphicUtils.Kitchen(),
                             "Trophy_Room": graphicUtils.Trophy_Room(),
                             "Dinning_Room": graphicUtils.Dinning_Room(),
                             "Drawing_Room": graphicUtils.Drawing_Room(), 
                             "Gazebo": graphicUtils.Gazebo(),
                             "Conservatory": graphicUtils.Conservatory(),
                             "Fountain": graphicUtils.Fountain(),
                             "Library": graphicUtils.Library(),
                             "Billiard Room": graphicUtils.Billiard_Room(), 
                             "Studio": graphicUtils.Studio(),
                             "Conservatory": graphicUtils.Conservatory(),
                             "Magnifier_1": graphicUtils.Magnifier_1(),
                             "Magnifier_2": graphicUtils.Magnifier_2(),
                             "Magnifier_3": graphicUtils.Magnifier_3(),
                             "Magnifier_4": graphicUtils.Magnifier_4(),
                             "Magnifier_5": graphicUtils.Magnifier_5(),
                             "Magnifier_6": graphicUtils.Magnifier_6(),
                             "Magnifier_7": graphicUtils.Magnifier_7(),
                             "Magnifier_8": graphicUtils.Magnifier_8(),
                             "Magnifier_9": graphicUtils.Magnifier_9()}

        ## a 42 * 24 grid
        self.grid = [[False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
                     ["Roo","Roo","Roo","Roo","Roo","Roo",False,"Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo",False,"Roo","Roo","Roo","Roo","Roo","Roo","Roo",False,False,"Roo","Roo","Roo","Roo","Roo","Roo","Roo",False,False,"Roo","Roo","Roo","Roo","Roo",False],
                     ["Roo","Roo","Roo","Roo","Roo","Roo",False,"Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo",True ,"Roo","Roo","Roo","Roo","Roo","Roo","Gat",True ,True ,"Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo",False,"Roo","Roo","Roo","Roo","Roo",False],
                     ["Roo","Roo","Roo","Roo","Roo","Roo",False,"Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo",True ,"Roo","Roo","Roo","Roo","Roo","Roo","Roo",True ,True ,"Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo",False,"Roo","Roo","Roo","Roo","Roo",False],
                     ["Roo","Roo","Roo","Roo","Roo","Roo",False,"Roo","Roo","Roo","Roo","Roo","Roo","Roo",True ,True ,"Gat","Roo","Roo","Roo","Roo","Roo","Roo",True ,True ,"Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo",False,"Roo","Roo","Roo","Roo","Roo",False],
                     ["Roo","Roo","Roo","Roo","Roo","Roo",False,"Roo","Roo","Roo","Roo","Roo","Roo",True ,True ,True ,"Roo","Roo","Roo","Roo","Roo","Roo","Roo",True ,True ,"Gat","Roo","Roo","Roo","Roo","Roo","Roo","Roo",False,"Roo","Roo","Roo","Roo","Roo",False],
                     ["Roo","Roo","Roo","Roo","Roo","Roo",False,"Roo","Roo","Roo","Roo","Roo","Roo",True ,True ,True ,"Roo","Roo","Roo","Roo","Roo","Roo",True ,True ,True ,"Roo","Roo","Roo","Roo","Roo","Roo","Roo",False,False,"Roo","Roo","Roo","Roo","Roo",False],
                     ["Roo","Roo","Roo","Roo","Roo","Roo",False,"Roo","Roo","Roo","Roo","Roo","Gat",True ,True ,True ,"Roo","Roo","Roo","Roo","Roo","Roo",True ,True ,True ,True ,True ,True ,True ,True ,False,False,False,False,"Roo","Roo","Gat","Roo","Roo",False],
                     ["Roo","Roo","Roo","Roo","Roo","Roo",False,True ,True ,True ,True ,True ,True ,True ,True ,True ,"Roo","Roo","Roo","Gat","Roo","Roo",True ,True ,True ,"Roo","Roo",True ,False,False,False,False,False,False,"Roo","Roo",True ,"Roo","Roo",False],
                     ["Roo","Roo","Roo","Roo","Roo","Roo",False,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,"Roo","Roo","Roo",True ,False,False,False,False,False,False,False,False,True ,True ,True ,False],
                     ["Roo","Roo","Roo","Roo","Roo",False,False,"Roo","Roo","Gat","Roo","Roo","Roo","Roo",True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,"Gat","Roo","Roo","Gat","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo",True ,False,True ,False],
                     ["Roo","Roo","Roo","Roo","Roo",False,False,"Roo","Roo","Roo","Roo","Roo","Roo","Roo",True ,"Roo","Gat","Roo","Roo","Roo","Roo","Roo",True ,True ,"Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Gat",True ,False,False,False],
                     ["Roo","Roo","Roo","Roo","Gat",True ,True ,"Gat","Roo","Roo","Roo","Roo","Roo","Gat",True ,"Roo","Roo","Roo","Roo","Roo","Roo","Roo",True ,True ,"Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Gat",False,False,False],
                     ["Roo","Roo","Roo","Roo","Gat",True ,True ,"Gat","Roo","Roo","Roo","Roo","Roo","Gat",True ,"Roo","Roo","Roo","Roo","Roo","Roo","Gat",True ,True ,"Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Gat",False,False,False],
                     ["Roo","Roo","Roo","Roo","Roo",False,False,"Roo","Roo","Roo","Roo","Roo","Roo","Roo",True ,"Roo","Roo","Roo","Roo","Roo","Roo","Roo",True ,True ,"Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Gat",True ,False,False,False],
                     ["Roo","Roo","Roo","Roo","Roo",False,False,"Roo","Roo","Roo","Roo","Roo","Roo","Roo",True ,"Roo","Roo","Roo","Roo","Gat","Roo","Roo",True ,True ,"Gat","Roo","Roo","Gat","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo",True ,False,True ,False],
                     [False,False,False,False,False,False,False,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,"Roo","Roo","Roo",True ,False,False,False,False,False,False,False,False,True ,True ,True ,False],
                     [False,False,False,False,False,False,False,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,"Roo","Roo",True ,False,False,False,False,False,False,"Roo","Roo",True ,"Roo","Roo",False],
                     [False,False,"Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Gat",True ,True ,True ,"Roo","Gat","Roo",True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,True ,False,False,False,False,"Roo","Roo","Gat","Roo","Roo",False],
                     [False,"Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo",True ,True ,"Roo","Roo","Roo","Roo","Roo",True ,"Roo","Roo","Roo","Gat","Roo",True ,True ,True ,"Roo","Roo","Roo","Roo","Roo",False,False,"Roo","Roo","Roo","Roo","Roo",False],
                     ["Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo",True ,"Roo","Roo","Roo","Roo","Roo",True ,"Roo","Roo","Roo","Roo","Roo",True ,"Roo","Gat","Roo","Roo","Roo","Roo","Roo","Roo",False,"Roo","Roo","Roo","Roo","Roo",False],
                     ["Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo",True ,"Roo","Roo","Roo","Roo","Gat",True ,"Roo","Roo","Roo","Roo","Roo",True ,"Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo",False,"Roo","Roo","Roo","Roo","Roo",False],
                     ["Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo",True ,"Roo","Roo","Roo","Roo","Roo",True ,"Roo","Roo","Roo","Roo","Roo",True ,"Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo",False,"Roo","Roo","Roo","Roo","Roo",False],
                     [False,"Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo",True ,"Gat","Roo","Roo","Roo","Roo",True ,"Gat","Roo","Roo","Roo","Gat",True ,"Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo",False,"Roo","Roo","Roo","Roo","Roo",False],
                     [False,False,"Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo","Roo",False,"Roo","Roo","Roo","Roo","Roo",False,"Roo","Roo","Roo","Roo","Roo",False,"Roo","Roo","Roo","Roo","Roo","Roo","Roo",False,False,"Roo","Roo","Roo","Roo","Roo",False],
                     [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]]
    
    def getReachableRoom(self, maxSteps, starting_point):
        """
        Given steps and starting point, return the rooms that's reachable
        """
        result = []
        for obj in self.distance_map[starting_point].distance_others.keys():
            if self.distance_map[starting_point].distance_others[obj] <= maxSteps:
                result.append(obj)
        return result

    def getTerminatedLocation(self, coord_x, coord_y):
        pass


                             
