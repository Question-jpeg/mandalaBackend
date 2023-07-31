from cairosvg import svg2png

from bot.config.sizes import TRIANGLE_HEIGHT, WIDTH, HEIGHT, N, TN, INITIAL_ANGLE, SVG_SIZE
from bot.config.values import COLORS
from math import sin, cos, pi
from bot.logic import createMatrix

def get_image(date):

    data = createMatrix(date)
    matrix = data['matrix']
    center = data['center']

    offsetX = SVG_SIZE / 2
    offsetY = SVG_SIZE / 2 - TRIANGLE_HEIGHT / 2

    def generatePath(offsetX, offsetY, rowIndex, i):
        color = COLORS[matrix[rowIndex][i]]['color']
        return f'<path d="M {offsetX} {offsetY} L {offsetX+WIDTH/2} {offsetY+HEIGHT/2} L {offsetX} {offsetY+HEIGHT} L {offsetX-WIDTH/2} {offsetY+HEIGHT/2} Z" fill="{color}" />'

    def generateSvg(i):
        angle = 360/TN*i
        angleRad = 2*pi/TN*i + INITIAL_ANGLE
        
        R =  TRIANGLE_HEIGHT / 2
        x = cos(angleRad) * R
        y = sin(angleRad) * R 
        
        return f'''
            <svg width="{SVG_SIZE}" height="{SVG_SIZE}" viewBox="0 0 {SVG_SIZE} {SVG_SIZE}" transform="translate({x} {y}); rotate({angle} {SVG_SIZE/2} {SVG_SIZE/2})">
                {''.join(paths)}
            </svg>
        '''

    paths = [generatePath(offsetX - r*WIDTH/2 + WIDTH*i, offsetY + HEIGHT*r/2, r, i) for r in range(N) for i in range(r+1)]
    triangles = [generateSvg(i) for i in range(TN)]

    svg_code = f'''
        <svg width="{SVG_SIZE}" height="{SVG_SIZE}" viewBox="0 0 {SVG_SIZE} {SVG_SIZE}">
        {''.join(triangles)}
        </svg>
    '''

    return svg2png(bytestring=svg_code, background_color='black') # write_to can be removed