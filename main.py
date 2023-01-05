import random, time
# Map
map = []

def generateMap():
    global map 

    map = []
    for i in range(5):
        build = []
        for j in range(5):
            rng = random.randrange(10)
            if rng == 1: build.append(1) 
            elif rng == 2: build.append(2)
            else: build.append(0)
        
        map.append(build)

playerSpawned = False
targetSpawned = False

def fixMap():
    global playerSpawned, targetSpawned, map 

    for i in map:
        for j in i:
            # Player
            if j == 1:
                if playerSpawned: map[map.index(i)][i.index(j)] = 0
                else: playerSpawned = True
            
            # Target
            if j == 2:
                if targetSpawned: map[map.index(i)][i.index(j)] = 0
                else: targetSpawned = True
    else:
        print(playerSpawned, targetSpawned)
        # check if player/target has spawned
        while not (playerSpawned and targetSpawned):
            generateMap()
            fixMap()

generateMap()
fixMap()

for i in map:
    print(i)

def getPlayerPos():
    for y, i in enumerate(map):
        for x, j in enumerate(i):
            if j == 1: return (x, y)

def getTargetPos():
    for y, i in enumerate(map):
        for x, j in enumerate(i):
            if j == 2: return (x, y)

# print(getPlayerPos())
# print(getTargetPos())

def check():
    playerX, playerY = getPlayerPos()
    targetX, targetY = getTargetPos()

    finished = False

    if playerX == targetX and playerY == targetY:
        finished = True

    return finished

def movePlayer(x, y):
    playerX, playerY = getPlayerPos()
    targetX, targetY = getTargetPos()

    try:
        if map[playerY+y][playerX+x] == 2:
            exit()

        map[playerY][playerX], map[playerY+y][playerX+x] = map[playerY+y][playerX+x], map[playerY][playerX]

        print('Moved player!')
        for i in map:
            print(i)
    except:
        pass

def moveRandomly():
    availablePositions = ['up', 'down', 'left', 'right']

    playerX, playerY = getPlayerPos()
    targetX, targetY = getTargetPos()

    distanceX = targetX-playerX
    distanceY = targetY-playerY

    def removeImpossiblePositions(): # removes impossible positions
        if playerY-1 < 0: availablePositions.remove('up')
        if playerY+1 > 4: availablePositions.remove('down')
        if playerX-1 < 0: availablePositions.remove('left')
        if playerX+1 > 4: availablePositions.remove('right')
    
    removeImpossiblePositions()

    print(f'Distance X from player to target: {distanceX}')
    print(f'Distance Y from player to target: {distanceY}')

    print(f'Possible moves: {", ".join(availablePositions)}.')
    predictCharacters = {}
    for i in availablePositions:
        if i == 'up': predictCharacters[i] = map[playerY-1][playerX]
        if i == 'down': predictCharacters[i] = map[playerY+1][playerX]
        if i == 'left': predictCharacters[i] = map[playerY][playerX-1]
        if i == 'right': predictCharacters[i] = map[playerY][playerX+1]

    def think(): # think in a new position
        randomThinking = random.choice(availablePositions)
        print(f'> Thought in {randomThinking}, which has {predictCharacters[randomThinking]} in it\'s position')
        if predictCharacters[randomThinking] == 2:
            print('found')
            for i in map:
                print(i)
            exit()

        # initial placeholders
        predictDistanceX = distanceX
        predictDistanceY = distanceY

        if randomThinking == 'up': predictDistanceY = targetY-(playerY-1)
        if randomThinking == 'down': predictDistanceY = targetY-(playerY+1)
        if randomThinking == 'left': predictDistanceX = targetX-(playerX-1)
        if randomThinking == 'right': predictDistanceX = targetX-(playerX+1)

        print(f'Predicted Distance X from player to target: {predictDistanceX}')
        print(f'Predicted Distance Y from player to target: {predictDistanceY}')

        worthX = abs(predictDistanceX)<abs(distanceX)
        worthY = abs(predictDistanceY)<abs(distanceY)

        if worthX:
            print('moving to X because its worth it moving')
            if randomThinking == 'left':
                movePlayer(-1, 0)
            if randomThinking == 'right':
                movePlayer(+1, 0)
        if worthY:
            print('moving to Y because its worth it moving')
            if randomThinking == 'up':
                movePlayer(0, -1)
            if randomThinking == 'down':
                movePlayer(0, +1)
        #
        # TODO: Predict into all directions (for i in availablePositions loop) and calculate which move got the closest result
        #       Then actually move the player to the closest result's direction
        #

        print(availablePositions)
        if check():
            exit()

        time.sleep(1)
        think()
        
    think()
    print('-'*30)

moveRandomly()
