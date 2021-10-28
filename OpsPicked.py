# PROGRAM NAME: Operator + Player Data Collection
# BASIC BREAKDOWN OF THE PROGRAM:
#   Take user input from what teams are playing; Store to team_1 and team_2
#   Scan the screenshot for 5 players, scan the operator, scan the player name, and increase a set value from 0 and increment everytime that operator is played
#   Upload data to a .csv file and export.
# DEVELOPED BY: Shrey Mandol

# Modules imported by our program
import csv
import numpy as np
from PIL import Image
import pytesseract as pt
import pafy
import vlc
import cv2
import os

# Change path for pytesseract to where you have Tesseract-OCR folder. Included in package files to run and analyse. 
path = os.getcwd() + "\\Tesseract-OCR\\tesseract.exe"
pt.pytesseract.tesseract_cmd = r"%s"%path
strip_string = '\n\x0c/ |\n\n\'‘ ¢-|/_ '


def team_loader(filename: str) -> np.ndarray:
    '''
    Loads a dataset
    Parameters: filename: string type data
    Returns: A dictionary with the data from the loaded file
    '''
    dataset = np.genfromtxt(filename, delimiter=',', dtype = str)
    dataset_dict = {}
    for rows in dataset:
        dataset_dict.update({rows[0] : [rows[1], rows[2], rows[3], rows[4], rows[5]]})
    return dataset_dict

def get_team_names():
    '''
    Gets user input for team names
    Parametes: None
    Returns: 2 team names, as team1 and team2 strings
    '''
    team1 = input("Enter blue team name tag   : ")
    team2 = input("Enter orange team name tag : ")
    return team1, team2

def get_game_url():
    '''
    Asks for a URL and opens it using pafy
    Parameters: none
    Returns: Video file opened using pafy
    '''
    url = input("Enter the game URL: ")
    video = pafy.new(url).getbest()

    return video

def write_to_file(team, ops_played, players, round_ct):
    '''
    Writes data to a .csv file
    Parameters: team: to get team name; ops_played: array containing ops played that round; players: array containing player names in the same order; round_ct: current round count
    Returns: none
    '''
    filename = "Output\\%sFile.csv" %team
    with open(filename, mode = 'a') as team_file:
        team_writer = csv.writer(team_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        rounds = "Round Number %s"%round_ct
        round_array = [rounds, "","","",""]
        print (ops_played)
        print (players)
        team_writer.writerow(round_array)
        team_writer.writerow(ops_played)
        team_writer.writerow(players)
    team_file.close()

def append_to_array(array, image):
    '''
    Converts an image data to sting and appends it to the given array
    Parameters: array: of the array data type; image: image passed to convert to string
    return: none
    '''
    array.append(pt.image_to_string(image).strip(strip_string))

def clean_up_data(array, dataset_from_dict):
    pass

def process_ima(image):
    denoised_image = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21)
    grey_image = cv2.cvtColor(denoised_image, cv2.COLOR_BGR2GRAY)
    ret, bin_image = cv2.threshold(grey_image,127,255,cv2.THRESH_BINARY)
    ret3,otsu_image = cv2.threshold(bin_image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return otsu_image

def process_image(image):
    denoised_image = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21)
    grey_image = cv2.cvtColor(denoised_image, cv2.COLOR_BGR2GRAY)
    return grey_image

# Main body of the program
if __name__ == '__main__':
    
    # Get the video loaded into cv2 to scan through it
    video = get_game_url()
    vod   = cv2.VideoCapture(video.url)
    
    # Video attributes
    width  = int(vod.get(3))
    height = int(vod.get(4))
    fps    = int(vod.get(5))
    print ("Vod details: %s x %s, %s FPS"%(width,height,fps))

    # Get input for team names
    team1, team2 = get_team_names()
    windowTitle = "VOD Analysis for %s vs %s" %(team1,team2)

    # Initialising variables 
    y  = 68 
    x  = 135
    yh = 318
    xw = 185
    frame_count      = 1
    skip_seconds     = 7
    round_ct         = 1
    blue_op_played   = []
    orange_op_played = []
    blue_players     = []
    orange_players   = []
    ban_phase_over   = False

    # Main loop to scrub through the video
    while True:
        
        # Displaying the frame of the VOD
        check, frame = vod.read()
        #frame = cv2.fastNlMeansDenoisingColored(og_frame,None,10,10,7,21)
        #frame = process_image(og_frame)
        if not check:
            break
        cv2.imshow(windowTitle, frame)

        
        # If statemnet which checks if we proceed with the moves below to 
        if frame_count % (fps*skip_seconds) == 0 :
            # Add code to collect data on bans
            if not ban_phase_over:
                ban_phase_marker = frame[235:335, 440:840]
                ban_phase_text   = pt.image_to_string(ban_phase_marker).strip(strip_string)
                if ban_phase_text == "BAN PHASE":
                    map_crop = frame[38:68, 60:310]
                    map_name = pt.image_to_string(map_crop).strip(strip_string)
                    print ("Map name: %s"%map_name)
                    vert = 585
                    oa_ban_crop = frame[vert-10:vert+45, 310:480]
                    od_ban_crop = frame[vert-10:vert+45, 790:960]
                    ba_ban_crop = frame[vert-10:vert+45, 470:640]
                    bd_ban_crop = frame[vert-10:vert+45, 630:800]
                    oa_ban = pt.image_to_string(oa_ban_crop).strip(strip_string)
                    od_ban = pt.image_to_string(od_ban_crop).strip(strip_string)
                    ba_ban = pt.image_to_string(ba_ban_crop).strip(strip_string)
                    bd_ban = pt.image_to_string(bd_ban_crop).strip(strip_string)
                    print ("Bans are: %s, %s, %s, %s"%(oa_ban,od_ban,ba_ban,bd_ban))
                    ban_phase_over = True

            # Cropping image; Round Starting
            round_start_crop = frame[x:xw, y:yh]
            round_start_text = pt.image_to_string(round_start_crop).strip(strip_string)
            round_timer_crop = frame[35:60, 615:660 ]
            round_timer_text = pt.image_to_string(round_timer_crop)

            # If statement that slows down vod when we are in the pick phase
            if round_start_text.lower() == "6th pick phase" or round_start_text.lower() == "reveal phase":
                skip_seconds = 2
                printed_out  = False
            else :
                skip_seconds = 7
            
            # Check the frame for if the round if starting and then check for the operator names   
            if round_start_text.lower() == "round starting":
                printed_out      = False
                blue_op_played   = []
                orange_op_played = []
                skip_seconds     = 45
                round_ct         = round_ct + 1
                print ("Round #%s:"%(round_ct-1))
                
                # Code for OBJ
                obj_check = frame[645:670, 80:245]
                check_text = pt.image_to_string(obj_check)
                cv2.imwrite('Test.jpg', obj_check)
                if "OBJECTIVE LOCATION" in check_text:
                    site_crop = frame[630:680, 570:735]
                else:
                    site_crop = frame[375:435, 570:735]
                site = pt.image_to_string(site_crop)
                print ("Site :%s"%site)

                # Code for names
                for i in range(5):
                    ho                = 125+i*230
                    blue_op_cropped   = frame[310:360, ho:ho+125]
                    blue_op_processed = process_image(blue_op_cropped)
                    orange_op_cropped = frame[560:610, ho:ho+125]
                    orange_op_processed = process_image(orange_op_cropped)
                    append_to_array(blue_op_played, blue_op_processed)
                    append_to_array(orange_op_played, orange_op_processed)
                
                
            if "2:" in round_timer_text:
                skip_seconds   = 110                
                blue_players   = []
                orange_players = []
                
                for i in range(5):
                    bp                    = 130 + i*99
                    blue_player_cropped   = frame[bp:bp+30, 115:225]
                    blue_player_proccesed = process_image(blue_player_cropped)
                    orange_player_cropped = frame[bp:bp+30, 1065:1160]
                    orange_player_proccesed = process_image(orange_player_cropped)
                    append_to_array(blue_players,  blue_player_proccesed)
                    append_to_array(orange_players, orange_player_proccesed)
                
                if not printed_out:
                    # writing into .csv files for team
                    write_to_file(team1, blue_op_played, blue_players, round_ct-1)
                    write_to_file(team2, orange_op_played,orange_players, round_ct-1)
                    printed_out = True

        
        frame_count = frame_count+1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print ("Program is ending...")
    vod.release()
    vod.destroyAllWindows()
