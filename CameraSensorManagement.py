import face_recognition as fr
import os
import cv2
import copy
from time import sleep

# define constant queries used thoughout the Camera class
SLCT_A_FP = "SELECT pattern FROM `facepattern`;"

class Camera:
    
    def __init__(self, source):
        self.source = source
        
    def test_fr():
        chris_one = fr.load_image_file("Resources/1.jpg")
        chris_two = fr.load_image_file("Resources/2.jpg")
        chris_three = fr.load_image_file("Resources/3.jpg")
        don_one = fr.load_image_file("Resources/4.jpg")

        chris_one_encoding = fr.face_encodings(chris_one)[0]
        chris_two_encoding = fr.face_encodings(chris_two)[0]
        chris_three_encoding = fr.face_encodings(chris_three)[0]
        don_one_encoding = fr.face_encodings(don_one)[0]
        
        results = fr.compare_faces([chris_one_encoding], chris_two_encoding)
        
        if (results[0] == True):
            print("Same")
        else:
            print("Not same")
            
        results = fr.compare_faces([chris_one_encoding], chris_three_encoding)

        if (results[0] == True):
            print("Same")
        else:
            print("Not same")

        results = fr.compare_faces([chris_two_encoding], chris_three_encoding)

        if (results[0] == True):
            print("Same")
        else:
            print("Not same")
            
        results = fr.compare_faces([chris_three_encoding], don_one_encoding)

        if (results[0] == True):
            print("Same")
        else:
            print("Not same")

    def take_source_snapshot(self, img_path):
        try:
            photo = self.source.cur_frame
            cv2.imwrite(img_path, photo) 
            return True
        except Exception as e:
            print("Unable to take source snapshot: {}".format(e))
            return False
            
    def scan_for_faces(self):
        # take image from source
        self.take_source_snapshot("./temp.jpg")
        
        # load and check foraces within image
        temp_i = fr.load_image_file("./temp.jpg")
        temp_fe = fr.face_encodings(temp_i)
        
        # remove the temporary image
        os.remove("./temp.jpg")
        
        # return the result and result set
        if (len(temp_fe) == 0):
            return (False, [])
        else:
            return (True, temp_fe)

    def enrol_face(self, name, db):
        # create the full filename
        fn = './{}.jpg'.format(name)
        
        # retrieve the new face from the source
        result = self.take_source_snapshot(fn)
        
        if not result:
            return False
        
        # open the above snapshot and prepare for facial recognition
        temp_i = fr.load_image_file(fn)
        
        # get the faces from the image file
        # the first image is assumed as being the person
        # of interest, others are ignored.
        temp_fe = fr.face_encodings(temp_i)
        if (len(temp_fe) == 0):
            print("Unable to detect faces within image")
            os.remove(fn)
            return False
        else:
            temp_fe = temp_fe[0]
        
        # remove image
        os.remove(fn)
        
        # convert the above encoding to string form
        str_fe = ' '.join(str(i) for i in temp_fe)
        
        # create an owner with the provided name
        db.query("INSERT INTO `owner` (`name`, `password`) VALUES ('{}', 'password');".format(name))
        # query for the owner that was just created
        result = db.query("SELECT `id` from `owner` WHERE `name` = '{}'".format(name))
        # get the id from the result set
        r_id = result[0][0]
        # store the text in the database
        db.query("INSERT INTO `facepattern` (`pattern`, `owner_id`) VALUES ('{}', {});".format(str_fe, r_id))
        
        print("Face enrolled, {}!".format(name))
    
    def compare_with_source(self, img_path):
        # retrieve the new face from the source
        take_source_snapshot(self.source, "./temp.jpg")
        
        # load both the new and old images into memory,
        # and prepare them for facial recognition
        a_i = fr.load_image_file(img_path);
        b_i = fr.load_image_file("./temp.jpg")
        
        # get the faces from the image files
        # the first face detected is the face used 
        a_fe = fr.face_encodings(a_i)
        b_fe = fr.face_encodings(b_i)
        if (len(a_fe) == 0 or len(b_fe) == 0):
            print("Unable to detect faces within one or both images")
            os.remove("./temp.jpg")
            return False
        else:
            a_fe = a_fe[0]
            b_fe = b_fe[0]
        
        # compare the faces
        result = fr.compare_faces([a_fe], b_fe)[0]
        
        # remove the temporary image
        os.remove("./temp.jpg")
        
        return result
    
    def compare_with_database(self, db, owner = None, c_rs = None):
        # result set
        rs = None
        
        # check if an owner was specified
        if (owner is not None):
            rs = db.query(format("SELECT pattern FROM `facepattern` WHERE `owner` = '{}'", owner))
        else:
            # retrieve face patterns from database
            rs = db.query(SLCT_A_FP)
           
        t_r = True
        t_rs = None
        if c_rs is not None:
            t_rs = c_rs;
        else:
            t_r, t_rs = self.scan_for_faces()
            
        # create the face encoding lists (retrieved from the db)
        rs = [list(map(float, a.split())) for i in rs for a in i]
            
        # compare the faces (comparing with the first face found from the source)
        result = fr.compare_faces(rs, t_rs[0])
        
        # return whether the temporary image matched any owner in the database
        return True in result