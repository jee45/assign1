import flask
import glob
import yaml
import operator
print('jimp')


plays = {}
jPlays = {}
for fileName in glob.glob('/Users/ad/PycharmProjects/assign1/data/*.yaml'):

    with open(fileName, 'r') as yf:
        play = yaml.safe_load(yf)
        plays[play['id']] = play


app = flask.Flask(__name__)

def printLevels(level):
    for x in range(level):
        print ('| ' , end='')
        #print ('| ' , x, end='')

def recursivelyPrintYamlShit(inThing, level, depth=1000):
    jjPlays = {}
    if level <= depth:
        if isinstance(inThing, str):
            printLevels(level)
            print('str ', end='')
            print(" .... value: ", inThing)
            jjPlays['value'] = inThing

        elif not inThing:
            ''' ....    this might be wrong. dont forget to check this!!!!  '''

            jjPlays['value'] = 'Narrator'

        elif isinstance(inThing, dict):
            for key in inThing:
                printLevels(level)
                print('dict ',' .. key: ', key)
                jjPlays[key] = recursivelyPrintYamlShit(inThing[key], level + 1, depth)

        elif isinstance(inThing, list):
                for index, val in enumerate(inThing):
                    printLevels(level)
                    print( 'list ', ' .. index: ', index)
                    jjPlays[str(index)] = recursivelyPrintYamlShit(val, level + 1, depth)
        return jjPlays




def recursivelyDontPrintYamlShit(inThing, level, depth=1000):
    jjPlays = {}

    if level <= depth:
        if isinstance(inThing, str):
            jjPlays['value'] = inThing


        elif not inThing:
            ''' ....    this might be wrong. dont forget to check this!!!!  '''

            jjPlays['value'] = 'Narrator'

        elif isinstance(inThing, dict):
            for key in inThing:
                jjPlays[key] = recursivelyDontPrintYamlShit(inThing[key], level + 1, depth)

        elif isinstance(inThing, list):
                for index, val in enumerate(inThing):

                    jjPlays[str(index)] = recursivelyDontPrintYamlShit(val, level + 1, depth)
        return jjPlays


def recursivelyDeleteCertainkeys(inThing, level, depth=1000, dictKeysToRemove = []):
    jjPlays = {}

    if level <= depth:
        if isinstance(inThing, str):
            jjPlays['value'] = inThing
        elif isinstance(inThing, dict):

            for key in inThing:

                if key in dictKeysToRemove:
                    print('.')
                else:
                    jjPlays[key] = recursivelyDeleteCertainkeys(inThing[key], level + 1, depth, dictKeysToRemove)

        elif isinstance(inThing, list):
                for index, val in enumerate(inThing):

                    jjPlays[str(index)] = recursivelyDeleteCertainkeys(val, level + 1, depth, dictKeysToRemove)
        return jjPlays




print('making')
jPlays = recursivelyDontPrintYamlShit(plays, 0)
print('checking')
recursivelyDontPrintYamlShit(jPlays, 0)
print('printed dont print')


remove =['scene', 'act']
#jPlays = recursivelyDeleteCertainkeys(jPlays, 0, 100 ,remove )
#print(jPlays.keys())

'''
acts = []
for play in jPlays:
    #print(jPlays[play]['acts']['0']['scenes']['1']['blocks']['0']['lines']['0'].keys())
    #print(jPlays[play]['acts']['0']['scenes']['1']['blocks']['0']['lines']['0']['value'])

    #print(jPlays[play]['acts']['0']['scenes']['0']['blocks'].keys())
    #print(jPlays[play]['acts']['0']['scenes']['0']['blocks']['0']['lines']['0'].keys())


'''

@app.route('/')
def hello_world():

    # make sure this is ordered by date.

    return flask.render_template('index.html', plays=plays.values())


@app.route('/plays/<play>/')
def show_play(play):

    #the only thing im displaying here, in terms of the
    #acts, scenes, and blocks are just links to the indentifiers.
    # you only need to know the top value of each of these,
    #then just link to the showScene route.
    '''

    actCount = 0


    for acts in jPlays[play]['acts']:

        if int(acts) > actCount:
            actCount = int(acts)

    acts = []



    for actNumber in range(actCount):
        sceneCount = 0
        scenes= []
        for scene in  jPlays[play]['acts'][str(actNumber)]['scenes']:
            if int(scene) > actCount:
                sceneCount = int(scene)


        for sceneNumber in range(sceneCount):
            blockCount = 0
            blocks = []
            for blockNumber in jPlays[play]['acts'][str(actNumber)]['scenes'][str(sceneNumber)]['blocks']:
                if int(blockNumber) > blockCount:
                    blockCount = int(blockNumber)



            blocks.append(blockCount)

            scenes.append(blocks)
        acts.append(scenes)




    for act in acts:
        print(" - " , act)
        for scene in act:
            print(" - - ",scene )


    '''

    #get title,
    #get date
    #get list of characters,
    #get list of acts,

    #for each act
        #get scenes in the act
        #make a link to the scenes page with: /play/<id>/acts/<act>/scenes/<scene>




    return flask.render_template("play.html",
                                 title = jPlays[play]['full_title']['value'],
                                 date = jPlays[play]['date']['value'],
                                 id=jPlays[play]['id']['value'],
                                 characters = jPlays[play]['characters'],

                                 acts = jPlays[play]['acts']



                                 )



def isTheTopScene(scene, sceneNumbers):
    sceneNumber  =  int(scene)
    top = 0
    for x in sceneNumbers:
        if int(x) >top:
            top = int(x)

    if top > sceneNumber:
        return False
    else:
        return True


@app.route('/plays/<play>/acts/<act>/scenes/<scene>')
def show_scene(play, act, scene):

    #get the play's title
    title = jPlays[play]['full_title']['value']


    if int(scene) > 0:
        thereIsAPrevious = True
    else:
        thereIsAPrevious = False

    if isTheTopScene(scene,jPlays[play]['acts'][act]['scenes'].keys() ):
        thereIsANext = False
    else:
        thereIsANext = True


    #for this scene, get the setting
    setting = jPlays[play]['acts'][act]['scenes'][scene]['title']['value']

    #for this scene, get blocks and speeches
    blocks = jPlays[play]['acts'][act]['scenes'][scene]['blocks']

    print(blocks['1']['speaker']['value'])

    #make hyper link to 'next scene'

    return flask.render_template("scene.html",
                                 id = play,
                                 title = title,
                                 thisActNumber = act,
                                 thisSceneNumber = scene,
                                 thereIsAPrevious = thereIsAPrevious,
                                 thereIsANext = thereIsANext,
                                 setting = setting,
                                 blocks = blocks
                                 )



@app.route('/characters/<character>')
def show_characters(character):

    characterName = ""
    appearances = []



    #a list of all plays in which that character appears

    if character == 'Narrator':
        flask.flash('look, every play has a narrator. be more specific....')
        print(character)




    for play in jPlays:

        if character in jPlays[play]['characters'].keys():
            characterName = jPlays[play]['characters'][character]['value']

            pack = []
            #play id
            pack.append(jPlays[play]['id']['value'])

            #play title
            pack.append(jPlays[play]['full_title']['value'])

            #play year
            pack.append(jPlays[play]['date']['value'])

            appearances.append(pack)


    appearances = sorted(appearances, key=operator.itemgetter(2))


    # (looked up by ID — character IDs are globally unique across all plays).
    # The plays should be listed by date,
    # exactly as they appear in the main plays list (part 1).

    return flask.render_template("characters.html",
                                 characterId = character,
                                 characterName = characterName,
                                 appearances=appearances

                                 )

if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True)
