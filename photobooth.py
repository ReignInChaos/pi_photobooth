import piggyphoto, pygame
import os
import time
import RPi.GPIO as GPIO
from googleapiclient.discovery import build
from googleapiclient.http import *
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/drive.file'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('/home/pi/Downloads/credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))
#folder_metadata = {
#    'name': 'Halloween2018',
#    'mimeType': 'application/vnd.google-apps.folder'
#}
#folder = service.files().create(body=folder_metadata,
#                                    fields='id').execute()
#print 'Folder ID: %s' % folder.get('id')

state = 'preview'
bg = pygame.image.load("/home/pi/Downloads/halloween.jpg")
pygame.mixer.init()
pygame.display.set_mode((1824,984), pygame.FULLSCREEN)
#pygame.display.set_mode((600,400))
screen = pygame.display.get_surface()
    
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.add_event_detect(18,GPIO.FALLING,callback=button_callback)

def uploadFile(file):
    print('upload start')
    body = {
        'name': file,
        'title': file,
        'mimeType':'image/jpeg'
    }
    body['parents'] = ['1YfQHz58VlnRnh7VVKxThGZbMEYugc4bx']
    media = MediaFileUpload(file, mimetype='image/jpeg', resumable=True)
    file = service.files().create(body=body, 
                                    media_body=media).execute()
    print('upload complete')

def quit_pressed():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('quit pressed')
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
    return False

def preview(state):
    if state == 'preview':
        C.capture_preview('preview.jpg')
        picture = pygame.image.load('preview.jpg')
        width = float(picture.get_width()) * 1.4
        height = float(picture.get_height()) * 1.4
        screen.blit(bg, (0,0))
        picture = pygame.transform.scale(picture, (int(width), int(height)))
        screen.blit(picture, (930, 0))
        #textsurface = myfont.render(state, False, (0, 0, 0))
        #screen.blit(textsurface,(0,0))
        pygame.display.flip()
    else:
        pygame.mixer.music.load("/home/pi/Downloads/laugh.mp3")
        pygame.mixer.music.play()
        countdown = 6
        finished = False
        now = time.time()
        scary = pygame.image.load("/home/pi/Downloads/scary1.gif")
        while not finished:
            C.capture_preview('preview.jpg')
            picture = pygame.image.load('preview.jpg')
            width = float(picture.get_width()) * 1.4
            height = float(picture.get_height()) * 1.4
            screen.blit(bg, (0,0))
            picture = pygame.transform.scale(picture, (int(width), int(height)))
            screen.blit(picture, (930, 0))
            textsurface = myfont.render(str(countdown), False, (255, 255, 255))
            screen.blit(textsurface,(890,0))
            pygame.display.flip()
            
            later = time.time()
            difference = int(later - now)
            if difference > 0:
                countdown -= 1
                now = time.time()
            if countdown == 0:
                finished = True
        #screen.blit(scary, (0, 0))
        #pygame.display.flip()
        pygame.mixer.music.load("/home/pi/Downloads/scream.mp3")
        #pygame.mixer.music.play()
        time.sleep(0.5)
        file = 'halloween_2018_' + time.strftime("%H:%M:%S") + '.jpg'       
        C.capture_image(file)
        picture = pygame.image.load(file)
        picture = pygame.transform.scale(picture, (int(width), int(height)))
        screen.blit(bg, (0,0))
        screen.blit(picture, (930, 0))
        pygame.display.flip()
        uploadFile(file)
        time.sleep(6)

C = piggyphoto.camera()
C.leave_locked()
C.capture_preview('preview.jpg')

#bg = pygame.transform.scale(bg, (infoObject.current_w, infoObject.current_h))

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 150)

while not quit_pressed():
    if GPIO.input(18) == GPIO.LOW:
        state = 'countDown'
        print('button pressed')
        preview(state)
    else:
        state='preview'
        preview(state)
        
print('trying to quit')
pygame.quit()
sys.exit()
