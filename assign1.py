import flask
import glob
import yaml
import operator


plays = {}
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



@app.route('/')
def hello_world():
    # make sure this is ordered by date.
    return flask.render_template('index.html', plays=plays.values())


@app.route('/plays/<play>/')
def show_play(play):
    return flask.render_template("play.html",
                                 title = plays[play]['full_title'],
                                 date = plays[play]['date'],
                                 id=plays[play]['id'],
                                 characters = plays[play]['characters'],

                                 acts = plays[play]['acts']

                                 )

@app.route('/plays/<play>/acts/<act>/scenes/<scene>')
def show_scene(play, act, scene):

    #get the play's title
    title = plays[play]['full_title']


    if int(scene) > 0:
        thereIsAPrevious = True
    else:
        thereIsAPrevious = False

    if int(scene) < len(plays[play]['acts'][int(act)]['scenes']) -1:
        thereIsANext = True

    else:
        thereIsANext = False


    #for this scene, get the setting
    setting = plays[play]['acts'][int(act)]['scenes'][int(scene)]['title']

    #for this scene, get blocks and speeches
    blocks = plays[play]['acts'][int(act)]['scenes'][int(scene)]['blocks']

    return flask.render_template("scene.html",
                                 id = play,
                                 title = title,
                                 thisActNumber = act,
                                 thisSceneNumber = scene,
                                 thereIsAPrevious = thereIsAPrevious,
                                 thereIsANext = thereIsANext,
                                 setting = setting,
                                 blocks = blocks,
                                 characters = plays[play]['characters']

                                 )



@app.route('/characters/<character>')
def show_characters(character):

    characterName = ""
    appearances = []

    #a list of all plays in which that character appears

    if character == 'Narrator':
        flask.flash('look, every play has a narrator. be more specific....')
        print(character)

    for play in plays:
        if character in plays[play]['characters'].keys():
            characterName = plays[play]['characters'][character]

            pack = []
            #play id
            pack.append(plays[play]['id'])

            #play title
            pack.append(plays[play]['full_title'])

            #play year
            pack.append(plays[play]['date'])
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

@app.route('/plays/<play>/acts/<act>')
def show_acts(play, act):

    charactersInThisAct = []

    for scene in plays[play]['acts'][int(act)]['scenes']:
        for block in scene['blocks']:
            if block['speaker'] in charactersInThisAct:
                pass
            else:
                block['speaker']
                charactersInThisAct.append(block['speaker'])


    return flask.render_template("acts.html",
                                 title = plays[play]['full_title'],
                                 charactersList = charactersInThisAct,
                                 characters = plays[play]['characters'],
                                 date = plays[play]['date'],
                                 act = plays[play]['acts'][int(act)],
                                 id = play,
                                 actNumber = act
                                 )

if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True)
