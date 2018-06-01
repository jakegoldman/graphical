import mdl
from display import *
from matrix import *
from draw import *

"""======== first_pass( commands, symbols ) ==========

  Checks the commands array for any animation commands
  (frames, basename, vary)

  Should set num_frames and basename if the frames
  or basename commands are present

  If vary is found, but frames is not, the entire
  program should exit.

  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.
  ==================== """
def first_pass( commands ):
    isFrame = False
    isBasename = False
    isVary = False

    num_frames = 1

    for c in commands:
        if c['op'] == 'frames':
            num_frames = int( c['args'][0] )
            isFrame = True
        if c['op'] == 'vary':
            isVary = True
        if c['op'] == 'basename':
            isBasename = True
            basename = c['args'][0]

    # if there is vary without frame, exit
    if isVary and not isFrame:
        print 'Error: vary found without frame'
        exit(1)
    # if there isn't a basename, use the default
    if isFrame and not isBasename:
        basename = 'Fry'
        print 'No basename set, defaulting to \'Fry\''
    return [num_frames, basename]


"""======== second_pass( commands ) ==========

  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).

  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.

  Go through the command array, and when you find vary, go
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value.
  ===================="""
def second_pass( commands, num_frames ):
    knobs = [ {} for i in range(num_frames) ]

    for c in commands:
        if c['op'] == 'vary':
            knob = c['knob']
            startF = c['args'][0]
            startV = c['args'][2]
            endF = c['args'][1]
            endV = c['args'][3]

            if( startF < 0 or endF >= num_frames or endF <= startF ):
                print("Incorrect format for vary")
                exit(1)

            increment = (endV - startV) / (endF - startF)

            i = int( startF )
            while i < endF:
                knobs[i][knob] = startV + increment * (i - startF)
                i += 1
    return knobs



def run(filename):
    """
    This function runs an mdl script
    """

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return


    first_res = first_pass(commands)
    num_frames = first_res[0]
    basename = first_res[1]
    knobs = second_pass( commands, num_frames )


    for frame in range(num_frames):

        # set values each time
        view = [0,
                0,
                1];
        ambient = [50,
                   50,
                   50]
        light = [[0.5,
                  0.75,
                  1],
                 [0,
                  255,
                  255]]
        areflect = [0.1,
                    0.1,
                    0.1]
        dreflect = [0.5,
                    0.5,
                    0.5]
        sreflect = [0.5,
                    0.5,
                    0.5]

        color = [0, 0, 0]
        tmp = new_matrix()
        ident( tmp )

        stack = [ [x[:] for x in tmp] ]
        screen = new_screen()
        zbuffer = new_zbuffer()
        tmp = []
        step_3d = 20
        consts = ''
        coords = []
        coords1 = []


        # deal with knobs
        for knob in knobs[frame]:
            symbols[knob][1] = knobs[frame][knob]

        # actually run commands
        for command in commands:
            # print command
            c = command['op']
            args = command['args']

            if c == 'box':
                if isinstance(args[0], str):
                    consts = args[0]
                    args = args[1:]
                if isinstance(args[-1], str):
                    coords = args[-1]
                add_box(tmp,
                        args[0], args[1], args[2],
                        args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                tmp = []
            elif c == 'sphere':
                add_sphere(tmp,
                           args[0], args[1], args[2], args[3], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                tmp = []
            elif c == 'torus':
                add_torus(tmp,
                          args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                tmp = []
            elif c == 'line':
                if isinstance(args[0], str):
                    consts = args[0]
                    args = args[1:]
                if isinstance(args[3], str):
                    coords = args[3]
                    args = args[:3] + args[4:]
                if isinstance(args[-1], str):
                    coords1 = args[-1]
                add_edge(tmp,
                         args[0], args[1], args[2], args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_lines(tmp, screen, zbuffer, color)
                tmp = []
            elif c == 'move':
                k = 1
                if command['knob']:
                    k = symbols[command['knob']][1]
                tmp = make_translate(args[0] * k, args[1] * k, args[2] * k)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'scale':
                k = 1
                if command['knob']:
                    k = symbols[command['knob']][1]
                tmp = make_scale(args[0] * k, args[1] * k, args[2] * k)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'rotate':
                k = 1
                if command['knob']:
                    k = symbols[command['knob']][1]
                theta = args[1] * (math.pi/180) * k
                if args[0] == 'x':
                    tmp = make_rotX(theta)
                elif args[0] == 'y':
                    tmp = make_rotY(theta)
                else:
                    tmp = make_rotZ(theta)
                matrix_mult( stack[-1], tmp )
                stack[-1] = [ x[:] for x in tmp]
                tmp = []
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]] )
            elif c == 'pop':
                stack.pop()
            elif c == 'display':
                display(screen)
            elif c == 'save':
                save_extension(screen, args[0])

        print num_frames
        if num_frames > 1:
            print("saving file: " + filename)
            filename = "./anim/" + basename + ( "%03d.png" % int(frame) )
            save_extension( screen, filename)

        tmp = new_matrix()
        ident( tmp )
        stack = [ [x[:] for x in tmp] ]
        screen = new_screen()
        zbuffer = new_zbuffer()
        tmp = []
        step_3d = 20

    if num_frames > 1:
        make_animation( basename )
