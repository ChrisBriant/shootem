import os

#Get the filepath
def get_file_path(type,filename):
    if type == "i":
        return os.path.join("images", filename)

#Test collision of sprite on top of another
def collideontop(topsprite,bottomspritegrp):
    collision = False
    for sprite in bottomspritegrp.sprites():
        if (sprite.rect.x - topsprite.width) <= topsprite.rect.x <= (sprite.rect.x + sprite.width) \
            and (sprite.rect.y) <= topsprite.rect.y + topsprite.height <= (sprite.rect.y + sprite.height):
            collision = True
    return collision
