#cracking algorithm
import rhinoscriptsyntax as rs
import Rhino

def crackpolygon(polylines, count, maxGen,attrPts):
    newPolylines = []
    if count > maxGen :
        return 
        
    for polyline in polylines:
        if rs.CloseCurve(polyline) == False:
            print "Not a closed curve"
        else:
            centroid = rs.CurveAreaCentroid(polyline)
            centptVert = rs.PointAdd(centroid[0], [0,((maxGen-count)/maxGen)*25,((maxGen-count)/maxGen)+1*7])
            centpt = rs.AddPoint(centptVert)
            curves = rs.ExplodeCurves(polyline)
            for crv in curves:
                #print crv
                pt1 = rs.CurveStartPoint(crv)
                pt2 = rs.CurveEndPoint(crv)
                pts = [] 
                pts.append(pt1)
                pts.append(pt2)
                pts.append(centpt)
                pts.append(pt1)
                newpl = rs.AddPolyline(pts)
                addCurve = True
                for pt in attrPts:
                    if isPointInCurve(pt,newpl) :
                        addCurve = True
                if addCurve :
                    newPolylines.append(newpl)
                rs.DeleteObject(crv)
                
            rs.DeleteObjects(centpt)
    return crackpolygon(newPolylines, count+1, maxGen, attrPts)

def isPointInCurve(pt, curve):
    curve = rs.coercecurve(curve)
    rc = curve.Contains(pt)
    if rc==Rhino.Geometry.PointContainment.Outside: return False
    if rc==Rhino.Geometry.PointContainment.Inside: return True

    

def main():
    ptsIn = rs.GetObjects("select Pts",1)
    
    attrPts = []
    for pt in ptsIn:
        attrPts.append(rs.coerce3dpoint(pt))
    maxGen = rs.GetInteger("How many iterations would you like to do?", 3)
    polyline = rs.GetCurveObject("pick a closed curve to crack")
    
    rs.EnableRedraw(False)
    polylineGuid = polyline[0]
    polygons = []
    polygons.append(polylineGuid)
    crackpolygon(polygons, 0, maxGen,attrPts)
    
    rs.EnableRedraw(True)
    
    
if __name__ == "__main__" :
    main()
