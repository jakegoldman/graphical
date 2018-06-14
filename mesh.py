
'''
    filename: the the name of the mesh file
    polygons: the polygon matrix

    This function will parse the file, adding all verteces to a list and then
    adding all faces to the polygon matrix.
'''
def read_mesh( filename, polygons ):
    verteces = []
    faces = []
    with open( filename ) as f:
        for l in f:
            # split the line and check the first value
            line = l.split()

            # handle empty lines
            if line:

                # if this line defines a vertex, add it to the list
                if line[0] == 'v':
                    verteces.append( [ float( line[1] ), float( line[2] ), float( line[3] ) ] )

                # if this line defines a face, add it to the list (TEMPORARY)
                elif line[0] == 'f':
                    face = []
                    line = line[1:]
                    for vert in line:
                        face.append( int( vert ) )
                    faces.append( face )

                else:
                    print("UNKNOWN LINE DETECTED:")
                    print(l)


    # SUPER INNEFICIENT TESTING PRINTS
    print 'VERTECES:'
    for vertex in verteces:
        print '%f, %f, %f' % ( vertex[0], vertex[1], vertex[2] )
    print '\n\n\n\n\n'

    print 'FACES:'
    for face in faces:
        to_print = ''
        for vertex in face:
            to_print += str(vertex) + ', '
        print to_print[:len(to_print) - 2]
# end v_pass





# _____________________________ TESTING _____________________________
if __name__ == '__main__':
    polygons = []
    read_mesh( 'meshes/test.obj', polygons)
