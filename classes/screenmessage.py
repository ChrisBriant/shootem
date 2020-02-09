import pygame, colorsys

class OnScreenMessage(object):

    def __init__(self,size,message,font="comicsans",rgb=(255,0,0),grad=20,cycle=True):
        self.size = size
        self.rgb = list(rgb)
        self.message = message
        self.font = pygame.font.SysFont(font, self.size, True)
        self.textwidth, self.textheight = self.font.size(message)
        self.grad = grad
        self.cycle = cycle

    def rgbgradient(r,g,b,count):
        l = 0.299*r + 0.587*g + 0.114*b


    def draw(self,view,xoffset,yoffset,screen):
        grad = self.grad #Set gradient

        x= (xoffset*-1)+((screen["w"] - self.textwidth)//2)
        y = (yoffset*-1)+(screen["h"]//2)-(self.textheight//2)
        newrgb = self.rgb
        lstepval = -10
        while grad != 0:
            hls = colorsys.rgb_to_hls(newrgb[0],newrgb[1],newrgb[2])
            if any(c < 0 for c in colorsys.hls_to_rgb(hls[0],hls[1]+lstepval,hls[2])):
                lstepval = 10
                newrgb = colorsys.hls_to_rgb(hls[0],hls[1]+lstepval,hls[2])
            elif any(c > 255 for c in colorsys.hls_to_rgb(hls[0],hls[1]+lstepval,hls[2])):
                lstepval = -10
                newrgb = colorsys.hls_to_rgb(hls[0],hls[1]+lstepval,hls[2])
            else:
                newrgb = colorsys.hls_to_rgb(hls[0],hls[1]+lstepval,hls[2])

            """
            if self.cycleback:
                newrgb = colorsys.hls_to_rgb(hls[0],hls[1]-10,hls[2])
            else:
                newrgb = colorsys.hls_to_rgb(hls[0],hls[1]+10,hls[2])
            """
            text = self.font.render(self.message, 1, (newrgb[0],newrgb[1],newrgb[2]))
            #Calculate the area to draw the gradient
            textrect = text.get_rect()
            step = (textrect.height / self.grad) * grad
            view.blit(text, (x,y),(textrect.x,textrect.y,textrect.width,step))
            grad -= 1
        """
        if self.cycleback:
            self.cycleback = False
            self.rgb = newrgb
        else:
            self.cycleback = True
            """
        """
                view.blit(text, ((xoffset*-1)+((screen["w"] - self.textwidth)//2),
                                (yoffset*-1)+(screen["h"]//2)-(self.textheight//2)))
                    """
        #Make gradient cycle
        if self.cycle:
            self.rgb = newrgb
        #print(text.get_rect())


class FlashingText():

    def __init__(self,size,message,font="hack",rgb=(250,250,250)):
        self.size = size
        self.rgb = list(rgb)
        self.alpha =  255
        self.message = message
        self.font = pygame.font.SysFont(font, self.size, True)
        self.textwidth, self.textheight = self.font.size(message)


    def draw(self,view,posx,posy,xoffset,yoffset,screen):
        #Get place to draw text
        #posx and posy are relative to the centre of the screen
        x= (xoffset*-1)+((screen["w"] - self.textwidth)//2) + posx
        y = (yoffset*-1)+(screen["h"]//2)-(self.textheight//2) + posy

        self.image = pygame.Surface((self.textwidth, self.textheight))
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.image.set_alpha(self.alpha)
        self.alpha = max(0,self.alpha-5)
        if self.alpha == 5:
            self.alpha = 255

        self.text = self.font.render(self.message, True, self.rgb)
        self.image.blit(self.text,(0,0))
        view.blit(self.image,(x,y))
