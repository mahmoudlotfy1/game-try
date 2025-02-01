import pygame
# math for the fire
import math
import sys

pygame.init()

w, h= 1200, 600

screen= pygame.display.set_mode((w, h))

# define fonts
font= pygame.font.Font(None,74)










Fps= 60

#the image of the map
bg= pygame.image.load('world/ground.png')

#player aimation
player_an=['playerstand/pixil-frame-0.png','playerstand/pixil-frame-1.png','playerstand/pixil-frame-2.png','playerstand/pixil-frame-3.png','playerstand/pixil-frame-4.png'
,'playerstand/pixil-frame-5.png','playerstand/pixil-frame-6.png','playerstand/pixil-frame-7.png','playerstand/pixil-frame-8.png','playerstand/pixil-frame-9.png','playerstand/pixil-frame-10.png']

player_an_left_right=['left,right/pixil-frame-0.png','left,right/pixil-frame-1.png','left,right/pixil-frame-2.png','left,right/pixil-frame-3.png'
                      ,'left,right/pixil-frame-4.png','left,right/pixil-frame-5.png','left,right/pixil-frame-6.png','left,right/pixil-frame-7.png']

monster_img=['monster/pixil-frame-0.png','monster/pixil-frame-1.png','monster/pixil-frame-2.png','monster/pixil-frame-3.png',
'monster/pixil-frame-4.png','monster/pixil-frame-5.png','monster/pixil-frame-6.png','monster/pixil-frame-7.png','monster/pixil-frame-8.png']

# player class

class player:
    # the situp
    def __init__(self, x, y, speed,width,height):
        self.x= x
        self.y= y
        self.speed= speed
        self.width= width
        self.height=height
        # frams
        self.animation_frame= 0
        self.moving_right= False
        self.moving_left= False
        self.stand= True
        self.green=300
        self.alive= True
        

        #stand( the postion of the player)
        self.x_stand= 0
        self.y_stand= 0

        self.sub= 0
    #character itself
    def shap(self):
        # to restart the frams.
        if self.animation_frame + 1 >= 49:
            self.animation_frame =0
        # adding frams 
        self.animation_frame += 1
        if self.stand:
             image= pygame.transform.scale(pygame.image.load(player_an[self.animation_frame//8]),(self.width,self.height))
        elif self.moving_left:
             image= pygame.transform.scale(pygame.image.load(player_an_left_right[self.animation_frame//8]),(self.width,self.height))
        elif self.moving_right:
             image= pygame.transform.scale(pygame.transform.flip(pygame.image.load(player_an_left_right[self.animation_frame//8]), True, False),(self.width,self.height))
        # adding the player 
      
             
        screen.blit(image, (self.x, self.y))
      
# there was a problem with the movement because the pygame.keyup,
#some how it disturb the game movement so i used else insted but also it caused more problems
# so i added elif to orgnaize it and it did work.
    def move_diraction(self):
          
            if not self.alive:
               self.stand= True
               self.x_stand=0
               self.y_stand=0

               return
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.y_stand= -1
                self.stand= True
            elif keys[pygame.K_s]:
                self.y_stand= 1
                self.stand= True
            elif keys[pygame.K_a]:
                self.x_stand= -1
                self.moving_left,self.stand=True, False
            elif keys[pygame.K_d]:
                self.x_stand= 1
                self.moving_right,self.moving_left,self.stand= True,False,False
            else:
                self.x_stand=0
                self.y_stand=0
                self.stand= True

    def health_bar(self):
          pygame.draw.rect(screen,(255,0,0),[10,5,300,20]) 
          pygame.draw.rect(screen,(0,255,0),[10,5,max(0,self.green-self.sub),20]) 
        
          
               
               
               
          
    def x_y(self):
         return self.x,self.y
    def Rect(self):
         return pygame.Rect(self.x,self.y,self.width,self.height)

    def moving(self,wi,hi):
        self.x+=self.x_stand*self.speed
        self.y+=self.y_stand*self.speed
        # the wall
        self.x = max(0, min(self.x, wi- self.width))
        self.y = max(0, min(self.y, hi - self.height))
    
#bullet class
class Player_bullet:
     def __init__(self,x,y,mouse_x,mouse_y):
          self.x=x
          self.y=y
          self.mouse_x=mouse_x
          self.mouse_y=mouse_y
          self.speed=10
          self.angle= math.atan2(y-mouse_y,x-mouse_x )
          self.x_vel=math.cos(self.angle)*self.speed
          self.y_vel= math.sin(self.angle)*self.speed
          self.alive= True
     def main(self,display):
          self.x-=int(self.x_vel)
          self.y-=int(self.y_vel)

          pygame.draw.circle(display,(255,0,0),(int(self.x),int(self.y)),5)

    

        


class small_monster:
     def __init__(self, x, y,width,height):
        self.x= x
        self.y= y
        self.speed= 6
        self.width= width
        self.height=height
        self.bullet=[]
        self.bullet_wating= 30
        self.sub=0
        self.alive= True
        self.animation_frame=0
          
       



     def shap(self):
          if self.animation_frame + 1 >= 40:
            self.animation_frame =0
        # adding frams 
          self.animation_frame += 1
          image= pygame.transform.scale(pygame.image.load(monster_img[self.animation_frame//5]),(self.width,self.height))
          screen.blit(image,(self.x,self.y))
    
     def moving(self,player1,):
          if not self.alive:
               return
          # the player calculation
          player_x,player_y= player1.x_y()
          player_info= player1.Rect()
          monster= pygame.Rect(self.x,self.y,self.width,self.height)
          direction_x= player_x-self.x
          direction_y= player_y-self.y
       
          # get how it work
          distanse= math.sqrt(direction_x**2+direction_y**2)
          # did not git it trully 
          if distanse !=0:
               direction_x/= distanse
               direction_y/= distanse

          self.x+= direction_x * self.speed
          self.y+= direction_y * self.speed
          if monster.colliderect(player_info):
               self.speed=0
          else:
               self.speed=6
     def shooting(self, player_x, player_y):
          if not self.alive:
               return
          monster= pygame.Rect(self.x,self.y,self.width,self.height)
          if self.bullet_wating<=0:
               self.bullet.append(monster_bullet(self.x+monster.width/2,self.y+ monster.height/2,player_x,player_y))
               self.bullet_wating= 20
    
          
     def showing_the_bullet(self):
          self.bullet_wating -=1
          for bullet in self.bullet[:]:
               bullet.main()
               bullet.shape()
               if bullet.x < 0 or bullet.x> w or bullet.y < 0 or bullet.y > h:
                    self.bullet.remove(bullet)
     def health_bar(self):
          pygame.draw.rect(screen,(0,0,0),[250,550,700,20])
          pygame.draw.rect(screen,(0,255,0),[250,550,max(0,700-self.sub),20])

          
          
        
# monster bullet
class monster_bullet:
     def __init__(self,x,y,player_x,player_y):
          self.x=x
          self.y=y
          self.player_x=player_x
          self.player_y=player_y
          self.speed=15
          self.angle= math.atan2(y-player_y,x-player_x )
          self.x_vel=math.cos(self.angle)*self.speed
          self.y_vel= math.sin(self.angle)*self.speed
          self.wait= 0
     def main(self):
          self.x-=int(self.x_vel)
          self.y-=int(self.y_vel)

     def shape(self):
          pygame.draw.circle(screen,(0,255,0),(int(self.x),int(self.y)),5)  
      

class main_menu:
     def __init__(self):
          pass
     
     def pressing(self,event):
          if event.type== pygame.MOUSEBUTTONDOWN:
               event.pos
               return 1
          else:
               return None
# the main menu
main_img= pygame.image.load('main.jpg')
def mainmenu():
     menu= main_menu()
     main= True
     while main:
          screen.blit( main_img,(0,0))
          
          pygame.display.update()
          for event in pygame.event.get():
               if event.type== pygame.QUIT:
                    main= False
               action= menu.pressing(event)
               if action==1:
                    return
     pygame.quit()



                 
class game():
     def __init__(self):
          self.over= False
     def end (self):
          if self.over == True:
               screen.blit(pygame.image.load('end.jpg'),(0,0))

        
    
             


    

    








def Game():
    
    game_over=game()

    # the player last two number is the w,h so we make sure he does not get out of the screen
    #  if you look at the play image size is the same.
    player1= player(20,20,10,100,100)
  
    P_B=[]
    small_monster1= small_monster(400,400,100,100)

    


    

   

    fps= pygame.time.Clock()

    run=True

    while run:
        #blit is use to show the image on the screan
        screen.blit(bg,(0,0))
        mouse_x, mouse_y= pygame.mouse.get_pos()
        game_over.end()
        # test
       

        fps.tick(Fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            player1.move_diraction()
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
               if player1.alive:
                    P_B.append(Player_bullet(player1.x+player1.width//2,player1.y+player1.height//2,mouse_x,mouse_y))
            if game_over.over==True:
                 if event.type== pygame.KEYDOWN:
                      if event.key== pygame.K_SPACE:
                           player1.sub=0
                           player1.x,player1.y= 20,20
                           small_monster1.sub=0
                           small_monster1.x,small_monster1.y=400,400
                           player1.alive=True
                           small_monster1.alive= True
                           game_over.over= False
                           small_monster1.bullet_wating= 30
                           
                           
                      
          
          
        small_monster1.shooting(player1.x,player1.y)
        small_monster1.showing_the_bullet()
        player1.moving(w,h)
        small_monster1.moving(player1)


        player_got_shoot= pygame.Rect(player1.x,player1.y,player1.width,player1.height)

        for mon_bul_let in small_monster1.bullet[:]:
          the_bullet_hit_the_player= pygame.Rect(mon_bul_let.x,mon_bul_let.y,10,10)
          if player_got_shoot.colliderect(the_bullet_hit_the_player):
               player1.sub+= 10
               small_monster1.bullet.remove(mon_bul_let)
               if player1.sub >= 300:
                   player1.alive= False
                   game_over.over= True
                   

                   
                   small_monster1.alive= False


        monster_got_damge= pygame.Rect(small_monster1.x,small_monster1.y,small_monster1.width,small_monster1.height)
        
        for ply_bul_let in P_B[:]:
          the_bullet_hit_the_monster= pygame.Rect(ply_bul_let.x,ply_bul_let.y,10,10)
          if monster_got_damge.colliderect(the_bullet_hit_the_monster):
               small_monster1.sub+=3
               P_B.remove(ply_bul_let)
               if small_monster1.sub>= 700:
                    player1.alive= False
                    game_over.over= True
                    small_monster1.alive= False
                    
                    

             
          
          # the monster    
                   

        player1.health_bar()
        small_monster1.health_bar()

        for B in P_B[:]:
          B.main(screen)
          if B.x < 0 or B.x> w or B.y < 0 or B.y > h:
               P_B.remove(B)


        
        #monster_bull.shooting()
          

        player1.shap()
        small_monster1.shap()

        game_over.end()
        
        
       
        # the placement of the bullet
        
    
        pygame.display.update()
    pygame.quit()
mainmenu()
Game()

    
# (make the monster shoot), and if the monster touch the player he dies
# health bar


        