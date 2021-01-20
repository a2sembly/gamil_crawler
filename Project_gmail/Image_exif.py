#-*- coding: utf-8 -*-
import exifread as ef
import MapMaker as map

def Image_Info(filepath):
    with open(filepath, 'rb') as f:
        tags = ef.process_file(f)
        try:
            latitude = tags.get('GPS GPSLatitude')
            latitude_ref = tags.get('GPS GPSLatitudeRef')
            longitude = tags.get('GPS GPSLongitude')
            longitude_ref = tags.get('GPS GPSLongitudeRef')
            if latitude:
                lat_value = _convert_to_degress(latitude)
                if latitude_ref.values != 'N':
                    lat_value = -lat_value
            else:
                return {}
            if longitude:
                lon_value = _convert_to_degress(longitude)
                if longitude_ref.values != 'E':
                    lon_value = -lon_value
            else:
                return {}            
            return {'latitude' : lat_value, 'longitude': lon_value}
        except:
            return {}
    return {}

def Image_Info_See_Level(filepath):
    with open(filepath, 'rb') as f:
        tags = ef.process_file(f)
        try:
            Altitude =  tags.get('GPS GPSAltitude')
            if((not Altitude == None) and Altitude.values[0] and str(Altitude.values[0]) in "/"):
                Altitude_a = Altitude.values[0].split('/')
                Altitude_f = float(Altitude_a[0]) / float(Altitude_a[1])
            else:
                Altitude_f = 0
            AltitudeRef =  tags.get('GPS GPSAltitudeRef')
            if Altitude_f is not None:
                R_Altitude = map.Check_See_Level() # 해수면값 조작여부 검증. 고도
                print(R_Altitude)
                if not ((float(R_Altitude) - 5) <= float(Altitude_f) <= (float(R_Altitude + 5))):
                    Altitude_r = str(R_Altitude) + '/ GPS Manipulation'
                    print(R_Altitude)
                    print(Altitude_f)
                    return {'See-Level':Altitude_f}
                else:
                    return {'See-Level':Altitude_f}
            else:
                return {'See-Level':'N/A'}
        except:
            print('exif err')
            return {}
    return {}

def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)