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
                             "Courtyard": graphicUtils.Courtyard(),
                             "Fountain": graphicUtils.Fountain(),
                             "Library": graphicUtils.Library(),
                             "Billiard_Room": graphicUtils.Billiard_Room(), 
                             "Studio": graphicUtils.Studio(),
                             "Conservatory": graphicUtils.Conservatory(),
                             "Carriage_House": graphicUtils.Carriage_House(),
                             "Magnifier_1": graphicUtils.Magnifier_1(),
                             "Magnifier_2": graphicUtils.Magnifier_2(),
                             "Magnifier_3": graphicUtils.Magnifier_3(),
                             "Magnifier_4": graphicUtils.Magnifier_4(),
                             "Magnifier_5": graphicUtils.Magnifier_5(),
                             "Magnifier_6": graphicUtils.Magnifier_6(),
                             "Magnifier_7": graphicUtils.Magnifier_7(),
                             "Magnifier_8": graphicUtils.Magnifier_8(),
                             "Magnifier_9": graphicUtils.Magnifier_9()}

        ## a 42 * 24 grid, where 0 represents paths, 1 represents barriers, 2 represents room space, and 3 represents doors
        self.grid = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                     [2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,1,1,2,2,2,2,2,1],
                     [2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,3,0,0,2,2,2,2,2,2,2,2,1,2,2,2,2,2,1],
                     [2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,1,2,2,2,2,2,1],
                     [2,2,2,2,2,2,1,2,2,2,2,2,2,2,0,0,3,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,1,2,2,2,2,2,1],
                     [2,2,2,2,2,2,1,2,2,2,2,2,2,0,0,0,2,2,2,2,2,2,2,0,0,3,2,2,2,2,2,2,2,1,2,2,2,2,2,1],
                     [2,2,2,2,2,2,1,2,2,2,2,2,2,0,0,0,2,2,2,2,2,2,0,0,0,2,2,2,2,2,2,2,1,1,2,2,2,2,2,1],
                     [2,2,2,2,2,2,1,2,2,2,2,2,3,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0,0,0,1,1,1,1,2,2,3,2,2,1],
                     [2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,2,2,2,3,2,2,0,0,0,2,2,0,1,1,1,1,1,1,2,2,0,2,2,1],
                     [2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,1,1,1,1,1,1,1,1,0,0,0,1],
                     [2,2,2,2,2,1,1,2,2,3,2,2,2,2,0,0,0,0,0,0,0,0,0,0,3,2,2,3,2,2,2,2,2,2,2,2,0,1,0,1],
                     [2,2,2,2,2,1,1,2,2,2,2,2,2,2,0,2,3,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,2,2,2,3,0,1,1,1],
                     [2,2,2,2,3,0,0,3,2,2,2,2,2,3,0,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,2,2,2,2,3,1,1,1],
                     [2,2,2,2,3,0,0,3,2,2,2,2,2,3,0,2,2,2,2,2,2,3,0,0,2,2,2,2,2,2,2,2,2,2,2,2,3,1,1,1],
                     [2,2,2,2,2,1,1,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,2,2,2,3,0,1,1,1],
                     [2,2,2,2,2,1,1,2,2,2,2,2,2,2,0,2,2,2,2,3,2,2,0,0,3,2,2,3,2,2,2,2,2,2,2,2,0,1,0,1],
                     [1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,1,1,1,1,1,1,1,1,0,0,0,1],
                     [1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,1,1,1,1,1,1,2,2,0,2,2,1],
                     [1,1,2,2,2,2,2,2,2,2,3,0,0,0,2,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,2,2,3,2,2,1],
                     [1,2,2,2,2,2,2,2,2,2,2,0,0,2,2,2,2,2,0,2,2,2,3,2,0,0,0,2,2,2,2,2,1,1,2,2,2,2,2,1],
                     [2,2,2,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,0,2,2,2,2,2,0,2,3,2,2,2,2,2,2,1,2,2,2,2,2,1],
                     [2,2,2,2,2,2,2,2,2,2,2,2,0,2,2,2,2,3,0,2,2,2,2,2,0,2,2,2,2,2,2,2,2,1,2,2,2,2,2,1],
                     [2,2,2,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,0,2,2,2,2,2,0,2,2,2,2,2,2,2,2,1,2,2,2,2,2,1],
                     [1,2,2,2,2,2,2,2,2,2,2,2,0,3,2,2,2,2,0,3,2,2,2,3,0,2,2,2,2,2,2,2,2,1,2,2,2,2,2,1],
                     [1,1,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,1,2,2,2,2,2,1,2,2,2,2,2,2,2,1,1,2,2,2,2,2,1],
                     [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
    
    def getReachableRoom(self, maxSteps, starting_point):
        """
        Given steps and starting point, return the rooms that's reachable as chains
        """
        paths = []
        
        for nextObj in self.distance_map[starting_point].distance_others.keys():
            if self.distance_map[starting_point].distance_others[nextObj] <= maxSteps:
                path = [nextObj]
                self.getReachableHelper(path, paths, maxSteps - self.distance_map[starting_point].distance_others[nextObj], nextObj)
        return paths

    def getReachableHelper(self, path, paths, maxSteps, starting_point):
        """
        Do a depth first search on the graph, and recursively find all routes.
        """
        for nextObj in self.distance_map[starting_point].distance_others.keys():
            if self.distance_map[starting_point].willStop:
                if path not in paths:
                    paths.append(path)
                    break
            elif self.distance_map[starting_point].distance_others[nextObj] > maxSteps:
                if path not in paths:
                    paths.append(path)
            else:
                pathCopy = [x for x in path]
                pathCopy.append(nextObj)
                self.getReachableHelper(pathCopy, paths, maxSteps - self.distance_map[starting_point].distance_others[nextObj], nextObj)


    def getRoomFromCoord(self, coord_x, coord_y):
        """
        This method returns the room you are in given coordinates, if it's not in a room, return None
        """
        pass 


    def getShortestDistanceToOtherRooms(self, starting_point):
        """
        Using Dijkstra's Algorithm, get the shortest distance to all rooms on the board.
        """
        numberVertices = 13
        edges = {start: self.distance_map[start].distance_others for start in self.distance_map.keys()}  # {'Trophy_Room': {'Carriage_House': 2, 'Kitchen': 2, 'Magnifier_1': 4, 'Cloak_Room_Entry': 6, 'Studio': 7, 'Conservatory': 6, 'Magnifier_9': 4}}

        result = {room_name: float("inf") for room_name in edges.keys()}    # {"Trophy_Room": inf, "Carriage_House": inf, ...}
        result[starting_point] = 0          # {"Trophy_Room": 0, "Carriage_House": inf, ...}

        visited = set()
        while len(visited) < numberVertices:
            nextVertice, minDistance = getMinVerticeDistance(result, visited)
            if minDistance == float("inf"):
                break
            visited.add(nextVertice)

            updateVertices(nextVertice, minDistance, result, visited, edges)

        return result

    
def getMinVerticeDistance(result, visited):
    minDistance = float("inf")
    nextVertice = None
    for verticeName in result.keys():
        if verticeName in visited:
            continue
        if result[verticeName] < minDistance:
            nextVertice = verticeName
            minDistance = result[verticeName]

    return nextVertice, minDistance


def updateVertices(vertice, minDistance, result, visited, edges):
    for verticeToCheck in edges[vertice].keys():
        distanceToVertice = edges[vertice][verticeToCheck]
        if verticeToCheck in visited:
            continue
        newDistance = minDistance + distanceToVertice
        oldDistance = result[verticeToCheck]
        if newDistance < oldDistance:
            result[verticeToCheck] = newDistance
    return 


                             
