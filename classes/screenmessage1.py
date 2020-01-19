import pygame, colorsys

class OnScreenMessage(object):

    def __init__(self,size,message,font="comicsans",rgb=(255,0,0),grad=20):
        #self.x = x
        #self.y = y
        #self.width = width
        self.size = size
        self.rgb = list(rgb)
        self.message = message
        self.font = pygame.font.SysFont(font, self.size, True)
        self.textwidth, self.textheight = self.font.size(message)
        self.grad = grad
        self.cycleback = True

    def rgbgradient(r,g,b,count):
        l = 0.299*r + 0.587*g + 0.114*b


    def draw(self,view,xoffset,yoffset,screen):
        grad = self.grad #Set gradient

        x= (xoffset*-1)+((screen["w"] - self.textwidth)//2)
        y = (yoffset*-1)+(screen["h"]//2)-(self.textheight//2)
        newrgb = self.rgb
        while grad != 0:
            hls = colorsys.rgb_to_hls(newrgb[0],newrgb[1],newrgb[2])
            if self.cycleback:
                newrgb = colorsys.hls_to_rgb(hls[0],hls[1]-10,hls[2])
            else:
                newrgb = colorsys.hls_to_rgb(hls[0],hls[1]+10,hls[2])
            print(newrgb)
            text = self.font.render(self.message, 1, (newrgb[0],newrgb[1],newrgb[2]))
            #Calculate the area to draw the gradient
            textrect = text.get_rect()
            step = (textrect.height / self.grad) * grad
            print(step)
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
        #print(text.get_rect())
