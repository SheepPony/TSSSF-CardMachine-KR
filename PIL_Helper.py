from PIL import Image, ImageFont, ImageDraw, ImageOps
import os, glob
from math import ceil
import config

def BuildFont(fontname, fontsize,index=0):
    f= ImageFont.truetype(fontname, fontsize,index=index)
    print("Loaded:",f.getname())
    def gs(text):
        l,t,r,b=f.getbbox(text)
        line_width=r-l
        line_height=b-t
        assert line_width>=0
        assert line_height>=0
        return round(line_width),round(line_height)
    f.getsize=gs
    return f

def WrapText(text, font, max_width):
    '''
    Wraps text properly, so that each line does not exceed
    a maximum width in pixels. It does this by adding words
    in the string to the line, one by one, until the next
    word would make the line longer than the maximum width.
    It then start a new line with that word instead.
    New lines get special treatment. It's kind of funky.
    "Words" are split around spaces.
    '''
    temp = ""
    wrapped_text = ""

    for w in text.split(' '):
        # Add words to empty string until the next word would make the line too long
        # If next word contains a newline, check only first word before newline for width match
        if "\n" in w:
            wrapped_text += temp.strip(' ')
            width, height = font.getsize(u"{0} {1}".format(temp, w.partition('\n')[0]))
            # If adding one last word before the line break will exceed max width
            # Add in a line break before last word.
            if width > max_width:
                wrapped_text += "\n"
            else:
                wrapped_text += " "
            par = w.rpartition('\n')
            wrapped_text += par[0] + "\n"
            temp = par[2] + " "
        else:
            width, height = font.getsize(u"{0} {1}".format(temp, w))
            if width > max_width:
                wrapped_text += temp.strip(' ') + "\n"
                temp = ""
            temp += w + " "
    return wrapped_text + temp.strip(' ')

def GetTextBlockSize(text, font, max_width=-1, leading_offset=0):
    if max_width > -1:
        wrapped_text = WrapText(text, font, max_width)
    else:
        wrapped_text = text
    lines = wrapped_text.split('\n')
    
    # Set leading
    leading = font.font.ascent + font.font.descent + leading_offset

    # Get max line width
    max_line_width = 0
    for line in lines:
        line_width, line_height = font.getsize(line)
        # Keep track of the longest line width
        max_line_width = max(max_line_width, line_width)

    return (max_line_width, len(lines)*leading)

def AddText(image, text, font, fill=(0,0,0), anchor=(0,0),
            max_width=-1, halign="center", valign="top", leading_offset=0,
            rotate=0):
    '''
    First, attempt to wrap the text if max_width is set,
    and creates a list of each line.
    Then paste each individual line onto a transparent
    layer one line at a time, taking into account halign.
    Then rotate the layer, and paste on the image according
    to the anchor point, halign, and valign.

    @return (int, int): Total width and height of the text block
        added, in pixels.
    '''
    if max_width > -1:
        wrapped_text = WrapText(text, font, max_width)
    else:
        wrapped_text = text
    lines = wrapped_text.split('\n')

    # Initiliaze layer and draw object
    layer = Image.new('L', (5000,5000))
    draw = ImageDraw.Draw(layer)
    start_y = 500
    if halign == "left":
        start_x = 500
    elif halign == "center":
        start_x = 2500
    elif halign == "right":
        start_x = 4500
    
    # Set leading
    leading = font.font.ascent + font.font.descent + leading_offset

    # Begin laying down the lines, top to bottom
    y = start_y
    max_line_width = 0
    for line in lines:
        # If current line is blank, just change y and skip to next
        if not line == "":
            line_width, line_height = font.getsize(line)
            
            if halign == "left":
                x_pos = start_x
            elif halign == "center":
                x_pos = start_x-(line_width/2)
            elif halign == "right":
                x_pos = start_x-line_width
            # Keep track of the longest line width
            max_line_width = max(max_line_width, line_width)
            draw.text((x_pos, y), line, font=font, fill=255)
        y += leading

    total_text_size = (max_line_width, len(lines)*leading)

    # Now that the text is added to the image, find the crop points
    top = start_y
    bottom = y - leading_offset
    if halign == "left":
        left = start_x
        right = start_x + max_line_width
    elif halign == "center":
        left = start_x - max_line_width/2
        right = start_x + max_line_width/2
    elif halign == "right":
        left = start_x - max_line_width
        right = start_x
    layer = layer.crop((left, top, right, bottom))
    # Now that the image is cropped down to just the text, rotate
    if rotate != 0:
        layer = layer.rotate(rotate, expand=True)

    # Find the absolute anchor point on the original image
    # Negative anchor values refer from the right/bottom of the image
    x, y = image.size
    anchor_x = anchor[0]+x if anchor[0] < 0 else anchor[0]
    anchor_y = anchor[1]+y if anchor[1] < 0 else anchor[1]
    
    anchor_x=round(anchor_x)
    anchor_y=round(anchor_y)
        
    # Determine the anchor point for the new layer
    width, height = layer.size
    #print(F"W{width} H{height} AX{anchor_x} AY{anchor_y}")
    if halign == "left":
        coords_x = anchor_x
    elif halign == "center":
        coords_x = anchor_x - width/2
    elif halign == "right":
        coords_x = anchor_x - width
    if valign == "top":
        coords_y = anchor_y
    elif valign == "center":
        coords_y = anchor_y - height/2
    elif valign == "bottom":
        coords_y = anchor_y - height
    
    coords_x=round(coords_x)
    coords_y=round(coords_y)
    #print(F"CX{coords_x} CY{coords_y}")
    image.paste(ImageOps.colorize(layer, (255,255,255), fill),
                (coords_x, coords_y), layer)

    return total_text_size

# A4 Page
PAGE_WIDTH_MILLIIMETERS=config.page_width
PAGE_HEIGHT_MILLIMETERS=config.page_height

PAGE_WIDTH_INCHES=PAGE_WIDTH_MILLIIMETERS/25.4
PAGE_HEIGHT_INCHES=PAGE_HEIGHT_MILLIMETERS/25.4

PAGE_RATIO=PAGE_WIDTH_INCHES/PAGE_HEIGHT_INCHES
DPI=300 # Dots per Inch
DPM= DPI/25.4 # Dots per Millimeters

def BuildPage(card_list, grid_width, grid_height, filename,
              cut_line_width=3, page_ratio=PAGE_RATIO, h_margin=100):
    '''
    Adds cards, in order, to a grid defined by grid_width, grid_height.
    It then adds a border to the grid, making sure to preserve the
    page ratio for later printing, and saves to filename
    Assumes that all the cards are the same size
    '''
    # Create card grid based on size of the first card
    w,h = card_list[0].size
    cardgrid = Image.new("RGB", (
        (w+cut_line_width)*grid_width-cut_line_width, 
        (h+cut_line_width)*grid_height-cut_line_width))
    
    # Add cards to the grid, top down, left to right
    for y in range(grid_height):
        for x in range(grid_width):
            card = card_list.pop(0)
            coords = (x*(w+cut_line_width),
                      y*(h+cut_line_width))
            cardgrid.paste(card, coords)

    paper_size_px_full=(
        round(PAGE_WIDTH_MILLIIMETERS*DPM),
        round(PAGE_HEIGHT_MILLIMETERS*DPM))
    paper_image = Image.new("RGB", paper_size_px_full, (255, 255, 255))
    
    paper_size_px_inborder=(
        round((PAGE_WIDTH_MILLIIMETERS-config.page_margins*2)*DPM),
        round((PAGE_HEIGHT_MILLIMETERS-config.page_margins*2)*DPM))
    
    
    if paper_size_px_inborder[0] < cardgrid.width or paper_size_px_inborder[1] < cardgrid.height:
        # Resize needed!
        if config.shrink_cards_to_fit_page:
            orig_img=cardgrid
            cardgrid=ResizeImageToFitInside(cardgrid,paper_size_px_inborder)
            rsz_factor=cardgrid.width/orig_img.width
            print(F"Resizing card image!! Factor {rsz_factor*100:.1f}%")
            
        else:
            print("Card grid too big!")
            print("Paper@300dpi: {paper_image.width}x{paper_image.height}")
            print("In-Margin: {paper_size_px_inborder[0]}x{paper_size_px_inborder[1]}")
            print("Card Grid: {cardgrid.width}x{cardgrid.height}")
            0/0
    paper_image.paste(cardgrid, 
        (round((paper_image.width - cardgrid.width)/2), 
         round((paper_image.height - cardgrid.height)/2)))
    
    
    paper_image.save(filename, dpi=(DPI, DPI))

def BlankImage(w, h, color=(255,255,255), image_type="RGBA"):
    return Image.new(image_type, (w, h), color=color)

def LoadImage(filepath, fallback="blank.png"):
    try:
        return Image.open(filepath)
    except Exception:
        if fallback:
            return Image.open(os.path.join(os.path.split(filepath)[0], fallback))
        else:
            raise

def ResizeImage(image, size, method=Image.Resampling.BICUBIC):
    return image.resize(size, method)

def ResizeImageToFitInside(image,size,method=Image.Resampling.BICUBIC):
    resize_ratio_w=size[0]/image.width
    resize_ratio_h=size[1]/image.height
    resize_ratio=min(resize_ratio_h,resize_ratio_w)
    target_size=(
        round(image.width*resize_ratio),
        round(image.height*resize_ratio))
    return image.resize(target_size,method)

def DrawRect(image, x, y, width, height, color):
    draw = ImageDraw.Draw(image)
    draw.rectangle((x, y, width, height), fill=color)
    
def AddCutLine(
        image,
        margin_px=60,outer_margin=15,
        line_length=35,line_width_px=3,
        line_color=(255,60,60)):
    draw = ImageDraw.Draw(image)
    
    for v in ("T","B"): # Vertical Alignment: Top/Bottom
        for h in ("L","R"): # Horizontal Alignment: Left/Right
            for d in ("V","H"): # Direction: Vertical/Horizontal
                
                if d=="V":
                    if v=="T":
                        ytop=outer_margin
                        ybtm=line_length
                    elif v=="B":
                        ybtm=image.height-outer_margin
                        ytop=image.height-line_length
                    
                    if h=="L":
                        xright=margin_px
                        xleft=margin_px-line_width_px
                    elif h=="R":
                        xleft=image.width-margin_px
                        xright=image.width-margin_px+line_width_px
                elif d=="H":
                    if v=="T":
                        ybtm=margin_px
                        ytop=margin_px-line_width_px
                    elif v=="B":
                        ytop=image.height-margin_px
                        ybtm=image.height-margin_px+line_width_px
                        
                    if h=="L":
                        xleft=outer_margin
                        xright=line_length
                    elif h=="R":
                        xleft=image.width-line_length
                        xright=image.width-outer_margin
                
                # Top-Left H
                draw.rectangle(
                    (xleft,ytop,
                     xright,ybtm),
                    fill=line_color)
    return image

if __name__ == "__main__":
    image = Image.open("y.png")
    font = ImageFont.truetype("Ubahn_newpony.ttf", 40)
    text = "Boulder\nBoulder Boulder\nBoulder"
    w,h = image.size
    center = w/2
    anchor = (-50, -50)
    AddText(image, text, font, anchor=anchor, halign="right",
            valign="bottom", fill=(200,0,0), rotate=0)
    image.show()
