'''
Welcome to Monopoly!

I wrote Monopoly using pygame because why not?

I wrote an AI into it (algorithm) to play againt the user.
Her name is Eve. All her decision making is based around an attribute each property has, called 'realWorth'.
Initially she takes into account cost in relation to rent and compares it to other properties then adjusts realWorth accordingly.
She then re-evaluates realWorth on every iteration of the loop, adjusting for what other properties on the street are owned and whether it's mortgaged or not.
The amount she adjusts it by is pretty arbitrary. I wasn't sure what it should be so I just stuck in some random numbers, which kinda shows at times. It's one of her bigger weaknesses.
But ultimately I'm really happy with how she turned out. She sometimes beats me, which is cool.

I'm pretty inexperienced as a game developer so the code is kinda messy. I've tried to leave comments through it to explain what I'm trying to do, but I gave up on that about halfway through.
I also have no idea what to put in this front bit. Maybe some copyright signs? My initials? Patent pending, all rights reserved?

I should also add that I drew all the graphics, wrote the background music, and designed the font.
So nobody can sue me for anything. Except maybe the-company-that-shall-not-be-named for, well, the entire game idea. And also the name. But apart from that it's all original work.
Feel free to use the font for whatever you want. You can probably find better ones on DaFont though.

Anyway, enjoy my free Monopoly!

'''
import pygame
import math
import random
import time
from pygame import mixer

# -------------------------------------------------------------------------------
# SQUARE CLASSES

#There are 28 properties on a monopoly board, in order of ascending price and rent.
#Their attribute 'colour' is an integer and it refers to what street its in. Can be used as an index in the global lists 'colours' and 'streets'
class Property:
    def __init__(self, name, boardpos, colour):
        self.name = name
        self.boardpos = boardpos
        self.colour = colour
        self.houses = 0
        self.owner = bank
        self.rent = 0
        self.mortgaged = False
        self.rejected = False  # This is here so the user only has to buy/reject a property once.
        self.paidRent = False
        self.streetOwned = False
        self.buttonPosition = [[0, 0], [0, 0]]
        self.realWorth = 0 # This is what Eve uses to decide what to do with the property
        self.houseWorth = 0 # She uses this to decide whether to buy houses or not. She'll buy houses on any street but the second last.
        self.costsList = []

    def getPrice(self): # Returns the price of a property, based on its position on the board.
        if self.name == 'India':
            return 350
        elif self.name == 'China':
            return 400
        elif self.colour == 8:
            return 200
        elif self.colour == 9:
            return 150
        elif self.boardpos == 5*self.colour + 4:
            return 40*self.colour +80
        else:
            return 40 * self.colour + 60

    def getInitialRent(self): # Returns the (houseless) rent of a property, based on its position on the board.
        if self.colour <= 7:
            if self.boardpos == 5 * self.colour + 4 or self.name == 'England':
                self.costsList = houseCostGrid[self.colour][1]
                return houseCostGrid[self.colour][1][0]

            else:
                self.costsList = houseCostGrid[self.colour][0]
                return houseCostGrid[self.colour][0][0]
        elif self.colour == 8:
            return 25
        else:
            return 4*roll

    def getInitialWorth(self): # Returns the initial worth of a property, using initialMod (see around line 1300)
        global initialMod
        if self.colour <= 7:
            rents = sum(self.costsList) + self.getInitialRent()
            worth = rents * initialMod - self.getCostOfHouse()
            return worth
        elif self.colour == 8:
            return 200
        else:
            return 150

    def getInitialHouseWorth(self): # See above, but using houseMod
        global houseMod
        if self.colour <= 7:
            rents = avgDiff([self.getInitialRent()]+self.costsList)
            worth = rents * houseMod
            return worth
        else: # if a property's colour > 7, it's either a station or a utility and therefore can't be developed.
            return 0

    def getCostOfHouse(self): # Returns the cost of a house on a property, given its position on the board.
        multiplier = math.floor(self.colour/2) + 1
        if self.colour < 8:
            return multiplier*50
        else:
            return False

    def drawColour(self): # Draws houses, owner's colour,  and/or mortgaged sign on properties.
        if self.owner.colour:
            if 0 < self.boardpos < 10:
                colourPos = [605-math.floor(57.25*self.boardpos), 685]
                pygame.draw.rect(screen, self.owner.colour, (colourPos, (57, 15)))
                pygame.draw.rect(screen, palette.dutchWhite, (colourPos, (57, 2)))
                self.buttonPosition = [[colourPos[0], colourPos[0]+57], [colourPos[1], colourPos[1]+15]]
                if self.mortgaged:
                    screen.blit(mortgagePic, (colourPos[0], colourPos[1] - 77))
                if 0 < self.houses < 5:
                    count = 1
                    for house in range(self.houses):
                        housePos = [colourPos[0] + count, 610]
                        screen.blit(buildingPics[0], (housePos))
                        count += 14
                elif self.houses >= 5:
                    hotelPos = [colourPos[0] + 16, 610]
                    screen.blit(buildingPics[1], (hotelPos))

            elif 10 < self.boardpos < 20:
                colourPos = [0, 607-math.floor(57.25*(self.boardpos-10))]
                pygame.draw.rect(screen, self.owner.colour, (colourPos, (15, 57)))
                pygame.draw.rect(screen, palette.dutchWhite, ((colourPos[0] + 13, colourPos[1]), (2, 57)))
                self.buttonPosition = [[colourPos[0], colourPos[0]+15], [colourPos[1], colourPos[1]+57]]
                if 0 < self.houses < 5:
                    count = 1
                    for house in range(self.houses):
                        housePos = [71, colourPos[1] + count]
                        screen.blit(buildingPics[2], (housePos))
                        count += 14
                elif self.houses >= 5:
                    hotelPos = [71, colourPos[1] + 16]
                    screen.blit(buildingPics[3], (hotelPos))

                if self.mortgaged:
                    screen.blit(mortgagePic2, (colourPos[0] + 15, colourPos[1]))

            elif 20 < self.boardpos < 30:
                colourPos = [32 + math.ceil(57.25*(self.boardpos-20)), 0]
                pygame.draw.rect(screen, self.owner.colour, (colourPos, (57, 15)))
                pygame.draw.rect(screen, palette.dutchWhite, ((colourPos[0], colourPos[1] + 13), (57, 2)))
                self.buttonPosition = [[colourPos[0], colourPos[0]+57], [colourPos[1], colourPos[1]+15]]
                if 0 < self.houses < 5:
                    count = 1
                    for house in range(self.houses):
                        housePos = [colourPos[0] + count, 73]
                        screen.blit(buildingPics[4], (housePos))
                        count += 14
                elif self.houses >= 5:
                    hotelPos = [colourPos[0] + 16,75]
                    screen.blit(buildingPics[5], (hotelPos))

                if self.mortgaged:
                    screen.blit(mortgagePic, (colourPos[0], colourPos[1] + 15))

            else:
                colourPos = [685, 35 + math.ceil(57.25 * (self.boardpos - 30))]
                pygame.draw.rect(screen, self.owner.colour, (colourPos, (15, 57)))
                pygame.draw.rect(screen, palette.dutchWhite, ((colourPos), (2, 57)))
                self.buttonPosition = [[colourPos[0], colourPos[0]+15], [colourPos[1], colourPos[1]+57]]
                if 0 < self.houses < 5:
                    count = 1
                    for house in range(self.houses):
                        housePos = [608, colourPos[1] + count]
                        screen.blit(buildingPics[6], (housePos))
                        count += 14
                elif self.houses >= 5:
                    hotelPos = [608, colourPos[1] + 16]
                    screen.blit(buildingPics[7], (hotelPos))

                if self.mortgaged:
                    screen.blit(mortgagePic2, (colourPos[0] -77, colourPos[1]))

    def updateRent(self): # Updates a property's rent (who would have thought)
        if self.houses > 0:
            if self.boardpos == 5 * self.colour + 4 or self.name == 'England':
                self.rent = houseCostGrid[self.colour][1][self.houses]
            else:
                self.rent = houseCostGrid[self.colour][0][self.houses]
        if self.mortgaged:
            self.rent = 0
        return self.rent

class Chance: # There ultimately wasn't much point in writing this class except to help identify squares by their type.
    def __init__(self, name, boardpos):
        self.name = name
        self.boardpos = boardpos
        if self.name == 'Chance':
            self.list = chance
        else:
            self.list = communityChest

    def pickCard(self):
        return random.choice(self.list)

class TaxSquares: # Again, more of an identifier than anything else.
    def __init__(self, name, boardpos):
        self.name = name
        self.boardpos = boardpos
        self.paid = False

    def getTax(self):
        if self.name == 'Income Tax':
            return 200
        return 100

class SpecialSquares: # Applies to the squares on the corners.
    def __init__(self, name, boardpos):
        self.name = name
        self.boardpos = boardpos
        self.paid = False

    def getPayAmount(self, freeParking): # Returns how much money a player gets for landing on a square. See Alert classes for details on alerts
        global alert
        if self.name == 'Go':
            if user.isTurn:
                alert = Alert('Lazy Programming', 'You landed on Go and got $400 #because I was too lazy to fix #that issue. Some people play by #that rule anyway.')
            elif Eve.isTurn:
                alert = EveAlert('Sweet sweet cashola', 'Eve gets $400 by landing on Go')

            return 200
        elif self.name == 'Free Parking':
            if user.isTurn:
                alert = Alert('Rolling in Dough, maybe', ('You got $' + str(freeParking) + ' from Free Parking!'))
            return freeParking
        else:
            return 0

# -------------------------------------------------------------------------------
# SPRITE CLASSES
class Player: # Class for practical matters considering the user and Eve.
    def __init__(self, name, isTurn, screens):
        self.name = name
        self.piece = None
        self.boardpos = 0
        self.timeMoving = 0
        self.pieceSelected = False
        self.pieceConfirmed = False
        self.colour = None
        self.isTurn = isTurn
        self.money = 1500
        self.screens = screens #
        self.canRoll = True
        self.doublesCount = 0
        self.inJail = False
        self.jailTurns = 0
        self.getOutOfJailFreeCards = []
        # The next 4 attributes are boolean statuses (statuses? statii?). Arguably I could have made one string attribute called 'status'. Ah, the joy of hindsight.
        self.isDeveloping = False
        self.isTrading = False
        self.isMortgaging = False
        self.normalGameplay = True
        self.offer = []
        self.bid = '0'
        self.firstTimeInJail = True
        self.paidOOJ = False #OOJ stands for Out Of Jail. It gets tedious to write.


    def choosePiece(self, mousepos): # Lets the user choose a piece.
        if 110 < mousepos[0] < 110 + 1*270:
            if 276 < mousepos[1] < 276 + 128:
                self.piece = boot
                return (110, 276)
            elif 427 < mousepos[1] < 427 + 128:
                self.piece = iron
                return (110, 427)
        elif 110 + 1*270 < mousepos[0] < 110 + 2*270:
            if 276 < mousepos[1] < 276 + 128:
                self.piece = car
                return (110 + 1*270, 276)
            elif 427 < mousepos[1] < 427 + 128:
                self.piece = ship
                return (110 + 1 * 270, 427)
        elif 110 + 2*270 < mousepos[0] < 110 + 3*270:
            if 276 < mousepos[1] < 276 + 128:
                self.piece = dog
                return (110 + 2 * 270, 276)
            elif 427 < mousepos[1] < 427 + 128:
                self.piece = thimble
                return (110 + 2 * 270, 427)
        elif 110 + 3*270 < mousepos[0] < 110 + 4*270:
            if 276 < mousepos[1] < 276 + 128:
                self.piece = hat
                return (110 + 3 * 270, 276)
            elif 427 < mousepos[1] < 427 + 128:
                self.piece = wheelbarrow
                return (110 + 3 * 270, 427)
        else:
            return False

    def getPos(self): # 'Boardpos' is an integer from 0-39 depending on what square you're on, but that has to be translated into x and y co-ords, hence this function.
        if 0 <= self.boardpos < 10:
            return [608-57*self.boardpos, 630]
        elif 10 <= self.boardpos < 20:
            return [15, 608-57*(self.boardpos-10)]
        elif 20 <= self.boardpos < 30:
            return [38 + 57*(self.boardpos-20), 15]
        else:
            return [630, 38 + 57*(self.boardpos-30)]

    def move(self): # Moves players forward one place at a time. I'm pretty sure it gets called on every iteration of the loop.
        if self.timeMoving > 0:
            if self.boardpos == 39:
                self.boardpos = 0
                self.money += 200
            else:
                self.boardpos += 1
            time.sleep(0.1)
            self.timeMoving -= 1

class Bank: # An identifier class. It is reminiscent of real life banks though.
    def __init__(self):
        self.colour = None

class AI: # There's an Eve object of the Player class and an AI object of the AI class. I like to think of 'Eve: Player' as Eve's body and 'AI: AI' as her brain.
    def __init__(self):
        self.player = Eve

    def bid(self, prop): # In auctions, Eve returns a value $1 higher than whatever you bid until it gets too high for her. It's annoying, but it's the most logical thing to do in an Auction.
        global alert
        if type(alert) == Auction:
            if alert.highestBid < prop.realWorth and alert.highestBid < self.player.money:
                return alert.highestBid + 1

    def wantsProp(self, prop): # Returns boolean of whether she wants to buy a given property or not.
        if prop.realWorth > prop.getPrice() + 50:
            if self.player.money > prop.getPrice()//2:
                return True
        elif prop.realWorth > prop.getPrice():
            if self.player.money > prop.getPrice():
                return True
        elif prop.realWorth > prop.getPrice() - 50:
            if self.player.money >= prop.getPrice()*2:
                return True
        return False

    def develop(self, street): # Returns the next property she wants to build a house on.
        if len(street) == 2:
            for prop in street:
                prop.houseWorth = prop.getInitialHouseWorth() + 25
        worthSum = 0
        for prop in street:
            worthSum += prop.houseWorth
        worthAvg = worthSum/len(street)

        underdevelopedCount = 0
        buildingProp = None
        if (worthAvg > street[0].getCostOfHouse() and self.player.money > street[0].getCostOfHouse()) or (worthAvg > street[0].getCostOfHouse() - 25 and self.player.money > 2*street[0].getCostOfHouse()):

            for prop in street:
                if prop.houses < street[len(street)-1].houses:
                    underdevelopedCount += 1
            if underdevelopedCount == 0:
                buildingProp = street[len(street)-1]
            elif underdevelopedCount == 2:
                buildingProp = street[1]
            elif underdevelopedCount == 1:
                buildingProp = street[0]

            if buildingProp.houses < 5:
                buildingProp.houses += 1
                self.player.money -= buildingProp.getCostOfHouse()
                return buildingProp

    def wantsTrade(self, offer, recieving): # Evaluates trades. She has to switch the owners of the properties, so she can evaluate whether the properties would be worth having once they've been traded.
        gettingValue = 0
        modOffer = offer
        modRecieve = recieving
        for item in offer:
            if type(item) == MoneyOffer:
                gettingValue += item.value
                modOffer.remove(item)
            else:
                item.owner = self.player

        givingValue = 0
        for item in recieving:
            if type(item) == MoneyOffer:
                givingValue += item.value
                modRecieve.remove(item)
            else:
                item.owner = user

        if givingValue > self.player.money:
            for item in modOffer:
                item.owner = user
            for item in modRecieve:
                item.owner = self.player
            return False

        getWorthProperties()
        getWorthStations()
        getWorthUtilities()

        for item in modOffer:
            item.owner = user
            gettingValue += item.realWorth
        for item in modRecieve:
            item.owner = self.player
            givingValue += item.realWorth

        getWorthProperties()
        getWorthStations()
        getWorthUtilities()

        if givingValue < gettingValue:
            return True
        return False

    def itemsToTrade(self): # Lets Eve write her own trades! She trades in pairs, and never offers or requests money so she's fairly limited, but it's still more than I thought it would be.
        global rejectedTrades
        userProps = []
        EveProps = []

        for prop in properties:
            if prop.owner == user:
                userProps.append(prop)
            elif prop.owner == Eve:
                EveProps.append(prop)

        offer = []
        request = []

        for want in userProps:
            for give in EveProps:
                if want.getPrice() <= give.getPrice() and want.realWorth > give.realWorth and not(want.streetOwned or give.streetOwned):
                    if not give in offer and not want in request:
                        if len(offer) < 3 and len(request) < 3:
                            offer.append(give)
                            request.append(want)

        sameStreets = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for give in offer:
            for want in request:
                if give.colour == want.colour:
                    sameStreets[give.colour] += 1


        for streetid in sameStreets: # This is where Eve modifies it depending on how many properties from a street she used.
        #It's a fix for a bug where she'll trade some properties on a street for other properties on the same street.
            if streetid == 1:
                for give in offer:
                    if give.colour == sameStreets.index(streetid):
                        i = offer.index(give)
                        offer.remove(offer[i])
                        request.remove(request[i])
            elif streetid == 2:
                offercount = 0
                for give in offer:
                    if give.colour == sameStreets.index(streetid):
                        offercount += 1
                if offercount == 1:
                    if give.colour == sameStreets.index(streetid):
                        i = offer.index(give)
                        offer.remove(offer[i])
                        request.remove(request[i])
                elif offercount == 2:
                    for want in request:
                        if want.colour == sameStreets.index(streetid):
                            i = request.index(want)
                            offer.remove(offer[i])
                            request.remove(request[i])

        if len(offer) == 0 or len(request) == 0:
            return [False]
        elif [offer, request] in rejectedTrades: # rejectedTrades is a list of trades that the user has said not to, so that Eve won't ask again.
            return [False]
        return [offer, request]

    def emergencyAction(self): # This is what Eve does if she goes to end her turn and she has negative money.
        global properties
        houseProps = [[], [], [], [], [], [], [], []]
        baselineHouseProps = [[], [], [], [], [], [], [], []]
        regProps = []
        for prop in properties:
            if prop.owner == self.player:
                if prop.houses > 0:
                    houseProps[prop.colour].append(prop)
                elif not prop.mortgaged:
                    regProps.append(prop)

        streetsToDemolish = [] # She starts by demolishing any houses, because they give a better return (90% back vs 50%)
        while not houseProps == baselineHouseProps: #This loop orders them by worth to cost ratio
            bestToSell = False
            for street in houseProps:
                if len(street) > 0:
                    if not bestToSell or street[0].houseWorth/street[0].getCostOfHouse() < bestToSell.houseWorth/bestToSell.getCostOfHouse():
                        bestToSell = street[0]
            houseProps[bestToSell.colour] = []
            streetsToDemolish.append(streets[bestToSell.colour])

        propsMortgaged = []
        housesSold = []
        for street in streetsToDemolish: # This loop sells the houses
            for iter in range(5):
                for prop in street:

                    if self.player.money < 0 and prop.houses > 0:
                        prop.houses -= 1
                        self.player.money += (9*prop.getCostOfHouse())//10
                        housesSold.append(prop)

                    if self.player.money >= 0:
                        return [housesSold, propsMortgaged, True]

        propsToMort = []
        while len(regProps)>0: # Ordering properties to mortgage
            bestToMort = False
            for prop in regProps:
                if not bestToMort or prop.realWorth/prop.getPrice() < bestToMort.realWorth/bestToMort.getPrice():
                    bestToMort = prop
            regProps.remove(bestToMort)
            propsToMort.append(bestToMort)

        for prop in propsToMort: # Mortgaging properties
            if self.player.money < 0:
                prop.mortgaged = True
                self.player.money += prop.getPrice()//2
                propsMortgaged.append(prop)
            else:
                return [housesSold, propsMortgaged, True]

        for list in housesSold: # Mortgaging properties that had houses on them at the start
            if self.player.money < 0:
                list[0].mortgaged = True
                self.player.money += list[0].getPrice//2
                propsMortaged.append(list[0])
            else:
                return [housesSold, propsMortgaged, True]

        if self.player.money >= 0:
            return [housesSold, propsMortgaged, True]

        return [housesSold, propsMortgaged, False] # Means that Eve is still in debt after mortgaging everything.


    def useGojf(self): # Determines if Eve will use a get out of jail free card when leaving jail.
        if len(self.player.getOutOfJailFreeCards) > 0:
            return True
        return False

# -------------------------------------------------------------------------------
# ALERT CLASSES

'''
Alerts are what I called the notification box that is used to narrate the events of the game for the user.
They don't really do anything for Eve or for the logic of the game, but they are necessary for the user to interact.
Some of the attributes for alert classes like Auction don't seem to make sense.
That's because there's one alert object that switches class a lot and it has to be able to get by.

All alert classes have the method write(), which draws the alert and its text on the screen.
They can also be confirmed (or denied) depending on which class and type of alert they are. This is called in the Game Loop whenever the mouse is clicked.
Auctions are odd ones out- they have calculators and bids.

Alerts (excluding auctions) are initialised with a heading and a body. They are split into lines by # signs.
EveAlerts must be confirmed before Eve can do anything new, which is how the user is able to keep up with what she does during her turn.

'''

class Alert:
    def __init__ (self, heading, body):
        self.heading = heading
        self.body = body
        self.confirmed = True

        if self.heading == 'Chance' or self.heading == 'Community Chest':
            self.type = 'confirm'
            self.image = confirmAlertPic
        elif self.heading.__contains__('Tutorial'):
            self.type = 'confirm'
            self.image = confirmAlertPic
        elif self.heading == 'They see me rollin\'' or self.heading == 'Serial doubles-roller' or self.heading == 'Not-so-smooth criminal':
            self.type = 'confirm'
            self.image = confirmAlertPic
        elif self.body.__contains__('?'):
            self.type = 'choice'
            self.image = choiceAlertPic
        elif self.heading == 'Trade':
            self.type = 'trade'
            self.image = tradeAlertPic
        elif self.heading == 'Mortgage' or self.heading == 'Unmortgage' or self.heading == 'Sell house?':
            self.type = 'confirm'
            self.image = confirmAlertPic
        else:
            self.type = 'basic'
            self.image = alertPic
        self.timePausing = 0

    def write(self):
        headingSize = 36
        bodySize = 24
        headingFont = pygame.font.Font('polly.ttf', headingSize)
        bodyFont = pygame.font.Font('polly.ttf', bodySize)
        lineSpacing = 6

        heading = headingFont.render(self.heading, True, palette.darkGold)

        lines = self.body.split('#')

        screen.blit(self.image, (700, 0))
        screen.blit(heading, (770, 224))
        for i in range(len(lines)):
            lines[i] = bodyFont.render(lines[i], True, palette.axolotl)
            height = 224 + headingSize + lineSpacing + i*(bodySize+lineSpacing)
            screen.blit(lines[i], (770, height))

    def confirmOrDeny(self):
        if self.type == 'choice':
            if inCircle(pygame.mouse.get_pos(), [700+353, 433], 15):
                return 'confirmed'
            if inCircle(pygame.mouse.get_pos(), [700+394, 433], 15):
                return 'denied'
        elif self.type == 'confirm' or self.type == 'trade':
            if inCircle(pygame.mouse.get_pos(), [700 + 394, 433], 15):
                return 'confirmed'
        return False

class Auction:
    def __init__(self, prop):
        self.prop = prop
        self.EveRejected = False
        self.image = auctionPic
        self.calcPos = {
            '0': [996, 408],
            '1': [940, 374],
            '2': [996, 374],
            '3': [1052, 374],
            '4': [940, 340],
            '5': [996, 340],
            '6': [1052, 340],
            '7': [940, 306],
            '8': [996, 306],
            '9': [1052, 306],
            'C': [940, 408],
            'bid': [1052, 408]
        }
        self.size = [56, 34]
        self.body = 'Your turn'
        self.highestBid = 0
        self.heading = 'Auction'
        self.type = 'auction'
        self.turnsSincePlayerBid = 0
        self.winner = None
        self.confirmed = True

    def checkCalc(self):
        global user, Eve
        for num in self.calcPos:
            if self.calcPos[num][0] < pygame.mouse.get_pos()[0] < self.calcPos[num][0] + self.size[0]:
                if self.calcPos[num][1] < pygame.mouse.get_pos()[1] < self.calcPos[num][1] + self.size[1]:
                    if num == 'C' and len(user.bid) > 0:
                        user.bid = '0'
                    elif num == 'bid':
                        if int(user.bid) > self.highestBid:
                            self.highestBid = int(user.bid)
                            self.winner = user
                            if AI.bid(self.prop):
                                Eve.bid = AI.bid(self.prop)
                            else:
                                self.EveRejected = True

                            self.turnsSincePlayerBid = 0
                            self.body = 'Eve is bidding...'
                        else:
                            self.body = "You gotta bid more #than the highest bid #mate that's how #auctions work"
                    else:
                        if user.bid == '0':
                            user.bid = num
                        else:
                            user.bid += num




    def write(self):
        global user, Eve
        numberSize = 28
        bodySize = 28
        if self.body.__contains__('auctions'):
            bodySize = 15
        elif self.body.__contains__('Eve'):
            bodySize = 20
        numberFont = pygame.font.Font('polly.ttf', numberSize)
        bodyFont = pygame.font.Font('polly.ttf', bodySize)
        lineSpacing = 4

        highestBid = numberFont.render('$'+str(self.highestBid), True, palette.axolotl)
        playerNum = numberFont.render('$' + user.bid, True, palette.dutchWhite)

        lines = self.body.split('#')

        screen.blit(self.image, (700, 0))
        screen.blit(highestBid, (775, 265))
        screen.blit(playerNum, (945, 265))
        for i in range(len(lines)):
            lines[i] = bodyFont.render(lines[i], True, palette.dutchWhite)
            height = 314 + i*(bodySize+lineSpacing)
            screen.blit(lines[i], (774, height))

    def confirmOrDeny(self):
        if 711 < pygame.mouse.get_pos()[0] < 921 and 403 < pygame.mouse.get_pos()[1] < 435:
            return 'denied'
        return False

class EveAlert:

    def __init__ (self, heading, body):
        self.heading = heading
        self.body = body
        self.type = 'confirm'
        self.image = confirmAlertPic
        self.confirmed = False
        self.smallFont = False

    def write(self):
        headingSize = 36
        bodySize = 24
        lineSpacing = 6
        if self.smallFont:
            headingSize = 32
            bodySize = 21
            lineSpacing = 5
        headingFont = pygame.font.Font('polly.ttf', headingSize)
        bodyFont = pygame.font.Font('polly.ttf', bodySize)


        heading = headingFont.render(self.heading, True, palette.darkGold)

        lines = self.body.split('#')

        screen.blit(self.image, (700, 0))
        screen.blit(heading, (770, 224))
        for i in range(len(lines)):
            lines[i] = bodyFont.render(lines[i], True, palette.axolotl)
            height = 224 + headingSize + lineSpacing + i*(bodySize+lineSpacing)
            screen.blit(lines[i], (770, height))

    def confirmOrDeny(self):
        if inCircle(pygame.mouse.get_pos(), [700 + 394, 433], 15):
            self.confirmed = True
            return 'confirmed'
        return False

# -------------------------------------------------------------------------------
# MISC CLASSES
class Roll: # Every side of the dice is its own object, of this class.
    def __init__(self, image, value):
        self.image = image
        self.value = value

class Button: # The menu is made up of buttons, which are in the list 'buttons' and belong to this class.
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.left = pos[0]
        self.top = pos[1]
        self.right = pos[0] + size[0]
        self.bottom = pos[1] + size[1]
        self.middle = ((self.left+self.right)//2, (self.top+self.bottom)//2)
    def mouseHover(self): # Returns True if the mouse is over the button.
        mousepos = pygame.mouse.get_pos()
        if self.left < mousepos[0] < self.right and self.top < mousepos[1] < self.bottom:
            return True
        return False

class Palette: # Aside from the house colours, there are only six colours that I use in the game, ranging from darkish green to yellowish brown. I found the palette online, hence the fancy colour names.
    def __init__(self):
        self.axolotl = (115, 128, 84)
        self.olivine = (163, 168, 109)
        self.dutchWhite = (225, 213, 184)
        self.darkVanilla = (214, 199, 167)
        self.camel = (190, 153, 110)
        self.darkGold = (170, 114, 42)

class Card: # Chance and Community Chest cards
    def __init__(self, text, type, value):
        self.text = text
        self.type = type
        self.value = value
        self.executed = False

    def execute(self, player): # A set of conditionals that do different stuff to the player who picked the card.
        if self.type == 'pay':
            player.money += self.value
        elif self.type == 'move':
            if player.boardpos > self.value:
                player.money += 200
            player.boardpos = self.value
        elif self.type == 'go to jail':
            player.inJail = True
        elif self.type == 'gojf':
            if self.text.__contains__('bribed'):
                player.getOutOfJailFreeCards.append(communityChest[4])
            else:
                player.getOutOfJailFreeCards.append(chance[8])
            player.canRoll = False
        elif self.type == 'social':
            for sprite in players:
                if sprite == player:
                    sprite.money += self.value*(len(players)-1)
                else:
                    sprite.money -= self.value
        elif self.type == 'repairs':
            for prop in properties:
                if prop.owner == player:
                    if prop.houses > 4:
                        player.money -= self.value[1]
                    else:
                        player.money -= self.value[0]*prop.houses
        elif self.type == 'nearestu':
            if 0 < player.boardpos <= 12:
                player.boardpos = 12
            elif 28 < player.boardpos < 40:
                player.boardpos = 12
                player.money += 200
            else:
                player.boardpos = 28
        elif self.type == 'nearests':
            if 0 < player.boardpos <= 5:
                player.boardpos = 5
            elif player.boardpos <= 15:
                player.boardpos = 15
            elif player.boardpos <= 25:
                player.boardpos = 25
            elif player.boardpos <= 35:
                player.boardpos = 35
            else:
                player.boardpos = 5
                player.money += 200
        elif self.type == 'mover':
            player.boardpos += self.value

class MoneyOffer: # Used in trades
    def __init__(self, value):
        self.value = value
        self.name = '$' + str(self.value)
        self.colour = value

class Ratio: # Part of Eve's property valuing system
    def __init__(self, cost, rent):
        self.cost = cost
        self.rent = rent
        self.value = self.cost/self.rent

# -------------------------------------------------------------------------------
# MISC FUNCTIONS

def inCircle(mousePos, circleMid, radius): # Checks if the mouse is in a circle with a given position and radius.
    if (mousePos[0]-circleMid[0])**2 + (mousePos[1]-circleMid[1])**2 <= radius**2:
        return True
    return False

def clickingOnButton():
    global buttons
    for button in buttons:
        if button.mouseHover():
            return True
    return False

def rollDice(die):
    roll1 = random.choice(die)
    roll2 = random.choice(die)
    return [roll1, roll2]

def isDodgy(): # When trading, you can't separate properties in a street if they have houses on them. This function returns true if the user tries to do that.
    global players, streets
    for player in players:
        tradeStreetHasHouses = False

        for prop in player.offer:
            neighboursBeingTraded = 0

            if type(prop) == MoneyOffer:
                break

            if prop.streetOwned:
                for neighbour in streets[prop.colour]:
                    if neighbour.houses > 0:
                        tradeStreetHasHouses = True
                        break

            if tradeStreetHasHouses:
                for neighbour in streets[prop.colour]:
                    if neighbour in player.offer:
                        neighboursBeingTraded += 1

                if neighboursBeingTraded < len(streets[prop.colour]):
                    return [True, colours[prop.colour]]
    return False

def getAvg(listOfRatios):
    sum = 0
    for ratio in listOfRatios:
        sum += ratio.value
    return sum/len(listOfRatios)

def avgDiff(listOfNums):
    diffList = []
    for i in range(len(listOfNums)-1):
        diff = listOfNums[i+1] - listOfNums[i]
        diffList.append(diff)
    avg = sum(diffList)/len(diffList)
    return avg


# -------------------------------------------------------------------------------
# MISC METHODS
def draw(player, pos): # I wrote a function to draw players becasue there are two parts to their pieces: the colour, and the piece itself.
    if player == user:
        screen.blit(userColour, pos)
        screen.blit(user.piece, pos)
    elif player == Eve:
        screen.blit(EveColour, pos)
        screen.blit(Eve.piece, pos)

def boardSetup(): # Sets up all the lists of properties and squares
    global squares, properties, colours
    notPropertyNames = ['Go', 'Community Chest', 'Income Tax', 'Chance', 'Jail', 'Free Parking', 'Go To Jail',
                        'Super Tax']

    squareNames = ['Go', 'France', 'Community Chest', 'England', 'Income Tax',
                   'North Station', 'Thailand', 'Chance', 'Turkey',
                   'Iran', 'Jail', 'Congo', 'Electric Company', 'Germany',
                   'Vietnam', 'East Station', 'Egypt', 'Community Chest',
                   'Philippines', 'Ethiopia', 'Free Parking', 'Japan', 'Chance', 'Mexico',
                   'Russia', 'South Station', 'Bangladesh', 'Nigeria',
                   'Water Works', 'Pakistan', 'Go To Jail', 'Brazil', 'Indonesia', 'Community Chest',
                   'America', 'West Station', 'Chance', 'India', 'Super Tax', 'China']


    for i in range(len(squareNames)):
        if not squareNames[i] in notPropertyNames:
            currentProp = Property(squareNames[i], i, 10)
            if currentProp.name.__contains__('Station'):
                currentProp.colour = 8
            elif currentProp.name == 'Electric Company' or currentProp.name == 'Water Works':
                currentProp.colour = 9
            else:
                for n in range(8):
                    if 5 * n < i < 5 * n + 5:
                        currentProp.colour = n
            currentProp.rent = currentProp.getInitialRent()
            squares.append(currentProp)
            properties.append(currentProp)
            if currentProp.colour <= 7:
                streets[currentProp.colour].append(currentProp)
        elif squareNames[i] == 'Chance' or squareNames[i] == 'Community Chest':
            currentChance = Chance(squareNames[i], i)
            squares.append(currentChance)
        elif squareNames[i].__contains__('Tax'):
            currentTax = TaxSquares(squareNames[i], i)
            squares.append(currentTax)
        else:
            currentSpecial = SpecialSquares(squareNames[i], i)
            squares.append(currentSpecial)

def showMenu(): # Draws the side menu
    global buttons, user, Eve, palette, board, background, buttonActions

    screen.fill(palette.axolotl)
    screen.blit(board, (0, 0))
    screen.blit(background, (700, 0))

    turnFont = pygame.font.Font('polly.ttf', 45)
    if user.isTurn:
        turnText = turnFont.render('YOUR TURN', True, palette.dutchWhite)
    else:
        turnText = turnFont.render('EVE\'S TURN', True, palette.dutchWhite)
    screen.blit(turnText, (870, 60))

    for button in buttons:
        if button == endTurnButton or button == mortgageButton:
            screen.blit(endTurnBehind, (button.pos))

        if button.mouseHover():
            pygame.draw.rect(screen, palette.dutchWhite, (button.pos, button.size))

        if button == endTurnButton and not etAvailable:
            screen.blit(endTurnUnAv, (button.pos))

        if button == endTurnButton:
            screen.blit(endTurnFront, (button.pos))
        elif button == mortgageButton:
            screen.blit(mortgageFront, (button.pos))

    if buttonActions[0]:
        screen.blit(throw[0].image, (188+11+37, 210+33))
        screen.blit(throw[1].image, (188+38+150, 210+33))


    screen.blit(buttonsPic, (700, 0))

    draw(user, (770, 50))
    draw(Eve, (730, 636))

    moneyFont = pygame.font.Font('polly.ttf', 40)
    userMoney = moneyFont.render('$' + str(user.money), True, palette.darkVanilla)
    EveMoney = moneyFont.render('$' + str(Eve.money), True, palette.darkVanilla)

    screen.blit(userMoney, (760, 150))
    screen.blit(EveMoney, (820, 646))

# -------------------------------------------------------------------------------
#GET RENT METHODS

# These are methods that update the rent value of properties based on houses and neighbours and stuff

def getRentStations():
    global squares
    stations = [squares[5], squares[15], squares[25], squares[35]]
    for currentStation in stations:
        matchesCount = -1
        if currentStation.owner != bank:
            for station in stations:
                if station.owner == currentStation.owner:
                    matchesCount += 1
            currentStation.rent = (2**matchesCount)*25

def getRentUtilities():
    global roll, squares
    utilities = [squares[12], squares[28]]
    if utilities[0].owner == utilities[1].owner and utilities[0].owner != bank:
        for utility in utilities:
            utility.rent = 10*roll

def getRentProperties():
    global properties, streets
    for street in streets:
        for currentProp in street:
            matchesCount = 0
            if currentProp.owner != bank:
                for prop in street:
                    if prop.owner == currentProp.owner and not prop.mortgaged:
                        matchesCount += 1
            if matchesCount >= len(street):
                currentProp.streetOwned = True
                currentProp.rent = currentProp.getInitialRent() * 2
                currentProp.updateRent()
            else:
                currentProp.streetOwned = False

# -------------------------------------------------------------------------------
#GET WORTH METHODS

# These methods update the realWorth attribute of properties based on their neighbours

def getWorthProperties():
    for prop in properties:
        prop.realWorth = prop.getInitialWorth()
    for street in streets:
        for currentProp in street:
            neighboursOwnedByEve = 0
            neighboursOwnedByUser = 0
            for neighbour in street:
                if neighbour != currentProp:
                    if neighbour.owner == Eve:
                        neighboursOwnedByEve += 1
                    elif neighbour.owner == user:
                        neighboursOwnedByUser += 1

            if neighboursOwnedByEve > 0 and neighboursOwnedByUser > 0:
                currentProp.realWorth -= 50
            else:
                currentProp.realWorth += 150 - (len(street)-neighboursOwnedByUser-neighboursOwnedByEve)*50

            for house in range(currentProp.houses):
                currentProp.realWorth += currentProp.houseWorth

            if currentProp.mortgaged:
                currentProp.realWorth -= currentProp.getPrice()//2

def getWorthStations():
    stations = [squares[5], squares[15], squares[25], squares[35]]
    for station in stations:
        station.realWorth = station.getInitialWorth()
        neighboursOwnedByEve = 0
        neighboursOwnedByUser = 0
        for neighbour in stations:
            if neighbour.owner == Eve:
                neighboursOwnedByEve += 1
            elif neighbour.owner == user:
                neighboursOwnedByUser += 1
        if neighboursOwnedByEve > 0 and neighboursOwnedByUser > 0:
            station.realWorth += 25*(neighboursOwnedByEve + neighboursOwnedByUser)
        else:
            station.realWorth += 50 * (neighboursOwnedByEve + neighboursOwnedByUser)

def getWorthUtilities():
    utilities = [squares[12], squares[28]]
    if utilities[1].owner != bank:
        utilities[0].realWorth = utilities[0].getInitialWorth() + 50
    if utilities[0].owner != bank:
        utilities[1].realWorth = utilities[1].getInitialWorth() + 50



# -------------------------------------------------------------------------------
#PIECES
boot = pygame.image.load('pieces/boot.png')
car = pygame.image.load('pieces/car.png')
dog = pygame.image.load('pieces/dog.png')
hat = pygame.image.load('pieces/hat.png')
iron = pygame.image.load('pieces/iron.png')
ship = pygame.image.load('pieces/ship.png')
thimble = pygame.image.load('pieces/thimble.png')
wheelbarrow = pygame.image.load('pieces/wheelbarrow.png')

pieces = [boot, car, dog, hat, iron, ship, thimble, wheelbarrow]


# -------------------------------------------------------------------------------
#DICE
dieOne = Roll(pygame.image.load('dice/one.png'), 1)
dieTwo = Roll(pygame.image.load('dice/two.png'), 2)
dieThree = Roll(pygame.image.load('dice/three.png'), 3)
dieFour = Roll(pygame.image.load('dice/four.png'), 4)
dieFive = Roll(pygame.image.load('dice/five.png'), 5)
dieSix = Roll(pygame.image.load('dice/six.png'), 6)

die = [dieOne, dieTwo, dieThree, dieFour, dieFive, dieSix]

roll = 0
throw = [0, 0]

# -------------------------------------------------------------------------------
#BUTTONS
background = pygame.image.load('background.png')
buttonsPic = pygame.image.load('buttons.png')

endTurnBehind = pygame.image.load('endTurnBehind.png')
endTurnFront = pygame.image.load('endTurnFront.png')
endTurnUnAv = pygame.image.load('endTurnUnAv.png')
etAvailable = False

mortgageFront = pygame.image.load('mortgageFront.png')

rollButton = Button([1143, 0], [157, 161])
developButton = Button([1143, 161], [157, 161])
tradeButton = Button([1143, 318], [157, 161])
quitButton = Button([1143, 475], [157, 161])
endTurnButton = Button([849, 475], [157, 161])
mortgageButton = Button([996, 475], [157, 161])

buttons = [rollButton, developButton, tradeButton, quitButton, mortgageButton, endTurnButton]
buttonActions = [False, False, False, False, False]

# -------------------------------------------------------------------------------
#CHANCE AND COMMUNITY CHEST
gojfCC = pygame.image.load('gojfComChest.png')
gojfC = pygame.image.load('gojfChance.png')

communityChest = [
    Card('Advance to Go. Collect $400.', 'move', 0), Card("The bank's web server got #COVID and accidentally deposits #into your account. Collect $200.", 'pay', 200),
    Card("You hurt yourself but there's #no socialised medicine. #Pay $50 and remember- you have #nothing to lose but your chains.", 'pay', -50),
    Card('You made some banger #investments. Collect $50.', 'pay', 50), Card('You argue that you murdered #the child in self defence: #Get out of Jail free.', 'gojf', gojfCC),
    Card('The government planted drugs #on you to meet prison quotas. #Go to Jail. Go directly to Jail. #Do not pass Go, do not collect $200.', 'go to jail', 0),
    Card('Your great-Aunt Gertrude #kicks the bucket. Inherit $100', 'pay', 100),
    Card('Happy Birthday! #Collect $10 from every player', 'social', 10), Card('You and your life insurance mature. #Collect $100', 'pay', 100),
    Card("You got COVID- pay #hospital fees of $50", 'pay', -50), Card('Your friend Banquo was #prophecised to father #a line of kings. #Pay $50 to hire a hitman', 'pay', -50),
    Card('You find $25 bucks on the #ground. Its your lucky day.', 'pay', 25), Card('Make hardcore repairs #on all your property. #For each house pay $40, #for each hotel pay $115', 'repairs', [40, 115]),
    Card('You have come last in a #beauty contest. Collect $10 #sympathy money', 'pay', 10), Card('Your co-worker gives you $100 #not to tell anyone about his #heroin addiction', 'pay', 100)
]
chance = [
    Card('Advance to Go. Collect $400.', 'move', 0), Card('Advance to Russia. #If you pass Go, collect $200.', 'move', 24), Card('Advance to China. #If you pass Go, collect $200.', 'move', 39),
    Card('Advance to Congo. #If you pass Go, collect $200.', 'move', 11), Card('Advance to North Station. #If you pass Go, collect $200.', 'move', 5),
    Card('Advance to the nearest utility. #If you pass Go, collect $200', 'nearestu', 0),
    Card('Advance to the nearest station. #If you pass Go, collect $200', 'nearests', 0),
    Card('Bank pays you some of that #sweet sweet mullah. Collect $50.', 'pay', 50), Card('You bribe the cops with donuts: #Get out of jail free', 'gojf', gojfC), Card('Go back 3 spaces', 'mover', -3),
    Card('You infringed the copyright of #a popular board game. #Go to Jail. Go directly to Jail. #Do not pass Go, do not collect $200.', 'go to jail', 0),
    Card('Make general repairs on all your #property. For each house pay $25, #for each hotel pay $100', 'repairs', [25, 100]), Card('25 bucks fall out of your pocket. #You lament the lack of women\'s #shorts with reasonably-sized pockets', 'pay', -25),
    Card("You have mysteriously #become everybody's grandma. #Pay each player #$50 as a present.", 'social', -50), Card('Your investment in divorce #lawyers was successful. #Collect $150.', 'pay', 150)
]


# -------------------------------------------------------------------------------
#PROPERTY DECO

housePic = pygame.image.load('house.png')
hotelPic = pygame.image.load('hotel.png')
houseSidePic = pygame.image.load('houseSide.png')
hotelSidePic = pygame.image.load('hotelSide.png')

buildingPics = [
    housePic, hotelPic,
    houseSidePic, hotelSidePic,
    pygame.transform.rotate(housePic, 180), pygame.transform.rotate(hotelPic, 180),
    pygame.transform.rotate(houseSidePic, 180), pygame.transform.rotate(hotelSidePic, 180),
]

# Rent you pay at each house level for each street
houseCostGrid = [
    [
        [2, 10, 30, 90, 160, 250], [4, 20, 60, 180, 320, 450]
    ], [
        [6, 30, 90, 270, 400, 550], [8, 40, 100, 300, 450, 600]
    ], [
        [10, 50, 150, 450, 625, 750], [12, 60, 180, 500, 700, 900]
    ], [
        [14, 70, 200, 550, 750, 950], [16, 80, 220, 600, 800, 1000]
    ], [
        [18, 90, 250, 700, 875, 1050], [20, 100, 300, 750, 925, 1100]
    ], [
        [22, 110, 330, 800, 975, 1150], [24, 120, 360, 850, 1025, 1200]
    ], [
        [26, 130, 390, 900, 1100, 1275], [28, 150, 450, 1000, 1200, 1400]
    ], [
        [35, 175, 500, 1100, 1300, 1500], [50, 200, 600, 1400, 1700, 2000]
    ]
]

mortgagePic = pygame.image.load('mortgage.png')
mortgagePic2 = pygame.transform.rotate(mortgagePic, 90)

# -------------------------------------------------------------------------------
# WINDOW
pygame.init()

screen = pygame.display.set_mode((1300, 700))

pygame.display.set_caption("Monopoly")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# -------------------------------------------------------------------------------
# COLOURS
palette = Palette()

playerColours = [palette.axolotl, palette.camel, palette.darkGold]
colours = ['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'indigo', 'purple', 'station', 'utility', 'undefined']

axolotlPiece = pygame.image.load('pieces/axolotlPiece.png')
darkVanillaPiece = pygame.image.load('pieces/darkVanillaPiece.png')
camelPiece = pygame.image.load('pieces/camelPiece.png')
darkGoldPiece = pygame.image.load('pieces/darkGoldPiece.png')

pieceColours = [axolotlPiece, camelPiece, darkGoldPiece]

# -------------------------------------------------------------------------------
# FREE PARKING
freeParking = 0

freeParkingFont = pygame.font.Font('polly.ttf', 40)
freeParkingText = freeParkingFont.render("Free Parking:", True, palette.darkVanilla)
freeParkingValue = freeParkingFont.render('$' + str(freeParking), True, palette.darkVanilla)

# -------------------------------------------------------------------------------
# ALERTS
choiceAlertPic = pygame.image.load('choiceAlert.png')
alertPic = pygame.image.load('alert.png')
confirmAlertPic = pygame.image.load('confirmAlert.png')
tradeAlertPic = pygame.image.load('tradeAlert.png')

moneyToTake = MoneyOffer(0)
moneyToGive = MoneyOffer(0)

auctionPic = pygame.image.load('auction.png')
auctioning = False

welcome = Alert('Welcome to Monopoly',
"Your opponent is an AI called #Eve. She likes walks on the beach #and daydreaming about the robot #revolution.")

# -------------------------------------------------------------------------------
# SPRITES

# Here are the screens for the animations when someone wins. I'm not sure how to actually do gifs so I draw different pictures every 0.2 seconds.
ugos1 = pygame.image.load('game over/user1.png')
ugos2 = pygame.image.load('game over/user2.png')
ugos3 = pygame.image.load('game over/user3.png')
ugos4 = pygame.image.load('game over/user4.png')
ugos5 = pygame.image.load('game over/user5.png')

ugoScreens = [ugos1, ugos2, ugos3, ugos4, ugos5]

cgos1 = pygame.image.load('game over/CPU1.png')
cgos2 = pygame.image.load('game over/CPU2.png')
cgos3 = pygame.image.load('game over/CPU3.png')

cgoScreens = [cgos1, cgos2, cgos3]

user = Player('You', True, ugoScreens)
Eve = Player('Eve', False, cgoScreens)
players = [user, Eve]

bank = Bank()

winner = None

# -------------------------------------------------------------------------------
# BOARD
board = pygame.image.load("board.png")

squares = []
properties = []
streets = [[],[],[],[],[],[],[],[]]
boardSetup()

# -------------------------------------------------------------------------------
# AI SETUP
AI = AI()

costRatios = []
houseRatios = []
rejectedTrades = []

# Here is where it sets up initialMod and houseMod

for prop in properties:
    if prop.colour <= 7:
        costs = prop.getCostOfHouse() + prop.getPrice()
        rents = sum(prop.costsList) + prop.getInitialRent()
        ratio = Ratio(costs, rents)
        costRatios.append(ratio)

        costs = prop.getCostOfHouse()
        rents = avgDiff([prop.getInitialRent()]+prop.costsList)
        ratio = Ratio(costs, rents)
        houseRatios.append(ratio)

initialMod = getAvg(costRatios)
houseMod = getAvg(houseRatios)

for prop in properties:
    if prop.colour <= 7:
        prop.realWorth = prop.getInitialWorth()
        prop.houseWorth = prop.getInitialHouseWorth()


# -------------------------------------------------------------------------------
# SELECTING PIECES AND COLOURS

choosePieceFont = pygame.font.Font('polly.ttf', 100)
choosePieceText = choosePieceFont.render("Select Piece:", True, palette.darkVanilla)

while not user.pieceConfirmed:

    screen.fill(palette.axolotl)
    screen.blit(pygame.image.load('choosePiece.png'), (0, 0))

    if user.pieceSelected:
        pygame.draw.rect(screen, palette.olivine, (user.pieceSelected, (270, 128)))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if user.pieceSelected and inCircle(pygame.mouse.get_pos(), [1139, 206], 32.5):
                user.pieceConfirmed = True
            else:
                user.pieceSelected = user.choosePiece(pygame.mouse.get_pos())

    screen.blit(choosePieceText, (150, 125))
    screen.blit(pygame.image.load('piecesForChoosing.png'), (0, 0))

    pygame.display.update()

pieces.remove(user.piece)

user.colour = random.choice(playerColours)
userColour = pieceColours[playerColours.index(user.colour)]

playerColours.remove(user.colour)
pieceColours.remove(userColour)

Eve.piece = random.choice(pieces)

Eve.colour = random.choice(playerColours)
EveColour = pieceColours[playerColours.index(Eve.colour)]

playerColours.remove(Eve.colour)
pieceColours.remove(EveColour)



# -------------------------------------------------------------------------------
# MUSIC

beginning = True
mixer.music.load('music.wav')
mixer.music.play(-1)

# -------------------------------------------------------------------------------
# TUTORIAL

tutorial = True
tuteAlert = Alert('Welcome to Monopoly', 'Would you like a tutorial?')
tuteScreensNum = 7
example = ''

while tutorial:
    screen.fill(palette.axolotl)
    freeParkingValue = freeParkingFont.render('$' + str(freeParking), True, palette.darkVanilla)

    showMenu()

    screen.blit(dieOne.image, (188 + 11 + 37, 210 + 33))
    screen.blit(dieOne.image, (188 + 38 + 150, 210 + 33))

    screen.blit(freeParkingText, (250, 372))
    screen.blit(freeParkingValue, (310, 424))

    for prop in properties:
        prop.drawColour()

    draw(Eve, Eve.getPos())
    draw(user, user.getPos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if tuteAlert.confirmOrDeny() == 'confirmed':
                if tuteAlert.heading == 'Welcome to Monopoly':
                    tuteAlert = Alert('Tutorial - 1 of ' + str(tuteScreensNum),
                                      'This is the \'roll\' button. #Press it to roll the dice #in the middle of the board.')
                    for prop in properties:
                        prop.owner = random.choice(players)

                elif tuteAlert.heading.__contains__('1 of'):
                    tuteAlert = Alert('Tutorial - 2 of ' + str(tuteScreensNum),
                                      'This is the \'develop\' button. #Press it to build houses on your #properties later in the game.')

                elif tuteAlert.heading.__contains__('2 of'):
                    tuteAlert = Alert('Tutorial - 3 of ' + str(tuteScreensNum),
                                      'This is the \'trade\' button. #Press it to initialise a trade #with Eve, your opponent.')

                elif tuteAlert.heading.__contains__('3 of'):
                    tuteAlert = Alert('Tutorial - 4 of ' + str(tuteScreensNum),
                                      'This is the \'forfeit\' button. #Press it to quit the game.')

                elif tuteAlert.heading.__contains__('4 of'):
                    tuteAlert = Alert('Tutorial - 5 of ' + str(tuteScreensNum),
                                      'This is the \'mortgage\' button. #Press it to mortgage or unmortgage #a property or sell a house.')

                elif tuteAlert.heading.__contains__('5 of'):
                    tuteAlert = Alert('Tutorial - 6 of ' + str(tuteScreensNum),
                                      'This is the \'end turn\' button. #Press it when it is availiable #to end your turn.')

                elif tuteAlert.heading.__contains__('6 of'):
                    if properties[len(properties)-3].owner.colour == palette.axolotl:
                        if properties[len(properties)-3].owner == user:
                            example = 'eg. you own West #Station, so it\'s green. '
                        else:
                            example = 'eg. Eve owns West #Station, so it\'s green. '
                    elif properties[len(properties)-3].owner.colour == palette.camel:
                        if properties[len(properties)-3].owner == user:
                            example = 'eg. you own West #Station, so it\'s beige. '
                        else:
                            example = 'eg. Eve owns West #Station, so it\'s beige. '
                    elif properties[len(properties)-3].owner.colour == palette.darkGold:
                        if properties[len(properties)-3].owner == user:
                            example = 'eg. you own West #Station, so it\'s dark gold. '
                        else:
                            example = 'eg. Eve owns West #Station, so it\'s dark gold. '
                    tuteAlert = Alert('Tutorial - 7 of ' + str(tuteScreensNum),
                                      'These rectangles indicate each #property\'s owner. ' + example + 'Click on #these rectangles to select properties #when trading, mortgaging or building.')

                elif tuteAlert.heading.__contains__('7 of'):
                    tutorial = False
                    break

                tuteAlert.body += '#Press \'OK\' to continue.'
            if tuteAlert.confirmOrDeny() == 'denied':
                if tuteAlert.heading == 'Welcome to Monopoly':
                    tutorial = False
                    break

    for i in range(tuteScreensNum):
        if tuteAlert.heading.__contains__(str(i+1) + ' of') and i < len(buttons):
            pygame.draw.circle(screen, palette.darkGold, buttons[i].middle, 157//2, 10)
        elif tuteAlert.heading.__contains__('7 of'):
            pygame.draw.circle(screen, palette.darkGold, (693, 350), 45, 10)

    tuteAlert.write()

    pygame.display.update()


for prop in properties:
    prop.owner = bank

# -------------------------------------------------------------------------------
# GAME LOOP
while not (winner==Eve or winner==user):
    freeParkingValue = freeParkingFont.render('$' + str(freeParking), True, palette.darkVanilla)

    showMenu()

    screen.blit(freeParkingText, (250, 372))
    screen.blit(freeParkingValue, (310, 424))

    for prop in properties:
        prop.drawColour()

    getRentProperties()
    getRentStations()
    getRentUtilities()

    getWorthProperties()
    getWorthStations()
    getWorthUtilities()

    # Event loop

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if user.isTurn: # checking to see if user has clicked on any buttons
                betterTradeMessage = False

                if (alert.type == 'choice' or alert.type == 'confirm')  and clickingOnButton():
                    if alert.type == 'choice' and not alert.body.__contains__('Answer the question woodja'):
                        alert.body += ' #Answer the question woodja'
                    elif alert.type == 'confirm' and not alert.body.__contains__('You gotta click "OK" mate'):
                        alert.body += ' #You gotta click "OK" mate'

                elif alert.type == 'trade' and clickingOnButton():
                    betterTradeMessage = True

                elif rollButton.mouseHover() and user.canRoll:
                    beginning = False
                    user.normalGameplay = True
                    user.isMortgaging = False
                    user.isTrading = False
                    user.isDeveloping = False
                    auctioning = False
                    justLanded = True

                    throw = rollDice(die)
                    buttonActions[0] = True
                    roll = throw[0].value + throw[1].value

                    for square in squares:
                        if type(square) == Property:
                            if square.colour == 9:
                                square.rent = square.getInitialRent()
                            square.rejected = False
                            square.paidRent
                        elif type(square) == TaxSquares or type(square) == SpecialSquares:
                            square.paid = False

                    for comcard in communityChest:
                        comcard.executed = False
                    for chancecard in chance:
                        chancecard.executed = False
                    card = None

                    if throw[0] == throw[1] and user.doublesCount < 3:
                        user.canRoll = True
                        if user.inJail:
                            alert = Alert('They see me rollin\'', 'They hatin\', #\'Cause I be gettin\' #out of jail for free')
                        user.doublesCount += 1
                    else:
                        user.canRoll = False
                    if user.doublesCount >= 3:
                        user.normalGameplay = False
                        user.timeMoving = 0
                        alert = Alert('Serial doubles-roller', 'You rolled doubles 3 times #in a row. You really are #a despicable person.')
                        user.canRoll = False
                    if user.inJail:
                        user.timeMoving = 0
                        user.jailTurns += 1
                    elif alert.heading != 'Serial doubles-roller':
                        user.timeMoving = roll

                elif developButton.mouseHover():
                    alert = Alert('Build?', 'Would you like to develop #your properties?')
                    user.normalGameplay = False

                elif tradeButton.mouseHover():
                    user.normalGameplay = False
                    moneyToGive = MoneyOffer(0)
                    moneyToTake = MoneyOffer(0)
                    alert = Alert('Trade with Eve?', 'Do you wish to trade with Eve?')

                elif quitButton.mouseHover():
                    alert = Alert('You sure mate?', 'Are you sure you want #to resign? Eve will #automatically win.')
                    user.normalGameplay = False

                elif mortgageButton.mouseHover():
                    alert = Alert('Mortgage and friends', 'Do you want to mortgage #or unmortgage a property #or sell a house?')
                    user.normalGameplay = False

                elif endTurnButton.mouseHover() and etAvailable:
                    if user.money < 0:
                        alert = Alert('Memories from 2008', 'You need $' + str(0-user.money) + ' to continue. #Do you want to declare #bankruptcy?')
                    else:
                        user.isTurn = False
                        Eve.isTurn = True
                        Eve.canRoll = True
                        user.canRoll = True
                        user.doublesCount = 0
                        etAvailable = False

                elif user.isDeveloping:
                    for prop in properties:
                        if prop.buttonPosition[0][0] < pygame.mouse.get_pos()[0] < prop.buttonPosition[0][1] and prop.buttonPosition[1][0] < pygame.mouse.get_pos()[1] < prop.buttonPosition[1][1]:
                            if prop.streetOwned and prop.owner == user:
                                alert = Alert('Build house?', 'Would you like to build 1 house #on ' + prop.name + ' for $' + str(prop.getCostOfHouse()) + '?')

                elif user.isTrading:
                    for prop in properties:
                        if prop.buttonPosition[0][0] < pygame.mouse.get_pos()[0] < prop.buttonPosition[0][1] and prop.buttonPosition[1][0] < pygame.mouse.get_pos()[1] < prop.buttonPosition[1][1]:
                            if not user.offer.__contains__(prop) and prop.owner == user:
                                user.offer.append(prop)
                            elif user.offer.__contains__(prop):
                                user.offer.remove(prop)
                            elif not Eve.offer.__contains__(prop) and prop.owner == Eve:
                                Eve.offer.append(prop)
                            elif Eve.offer.__contains__(prop):
                                Eve.offer.remove(prop)
                    if 1058 < pygame.mouse.get_pos()[0] < 1058+25 and 222 < pygame.mouse.get_pos()[1] < 222+25:
                        if not moneyToGive in user.offer:
                            user.offer.append(moneyToGive)
                        moneyToGive.value += 50
                        moneyToGive.name = '$' + str(moneyToGive.value)
                    elif 1088 < pygame.mouse.get_pos()[0] < 1088+25 and 222 < pygame.mouse.get_pos()[1] < 222+25:
                        if not moneyToTake in Eve.offer:
                            Eve.offer.append(moneyToTake)
                        moneyToTake.value += 50
                        moneyToTake.name = '$' + str(moneyToTake.value)

                elif user.isMortgaging:
                    for prop in properties:
                        if prop.owner == user and prop.buttonPosition[0][0] < pygame.mouse.get_pos()[0] < prop.buttonPosition[0][1] and prop.buttonPosition[1][0] < pygame.mouse.get_pos()[1] < prop.buttonPosition[1][1]:
                            if prop.houses <= 0:
                                if prop.mortgaged:
                                    alert = Alert('Unmortgage', 'Unmortgage ' + prop.name + ' for $' + str(prop.getPrice()) + '?')
                                else:
                                    alert = Alert('Mortgage', 'Mortgage ' + prop.name + ' for $' + str(int(prop.getPrice()/2)) + '?')
                            else:
                                alert = Alert('Sell house?', 'Sell house on ' + prop.name + ' for $' + str(int(prop.getCostOfHouse()*0.9)) + '?')

            if alert.confirmOrDeny() == 'denied': # Regardless of whose turn it is, user can confirm/deny alerts
                if alert.heading == 'Auction' and alert.winner:
                    auctionProp = alert.prop
                    auctionWinner = alert.winner
                    moneySpent = alert.highestBid
                    auctionProp.owner = auctionWinner
                    auctionWinner.money -= moneySpent
                    auctioning = False
                    alert = Alert('Auction over', auctionWinner.name + ' bought ' + auctionProp.name + ' for $' + str(moneySpent))

                if alert.heading == 'Unowned Property':
                    squares[user.boardpos].rejected = True
                    auctioning = True
                    user.normalGameplay = False
                    alert = Auction(squares[user.boardpos])
                    alert.highestBid = 0
                    alert.winner = None
                    user.bid = '0'
                    Eve.bid = '0'

                if alert.heading == 'You sure mate?':
                    alert = Alert("That's the spirit", 'Good on ya mate')

                if alert.heading == 'Get out of Jail Free?':
                    alert = Alert('A free man', 'You paid $50 to #get out of jail.')
                    user.money -= 50
                    user.inJail = False
                    user.jailTurns = 0

                if alert.heading == 'Build?':
                    alert = Alert('Bruh', "Why did you click on #the house button then")

                if alert.heading == 'Build house?':
                    alert = Alert('Alrighty then', 'Click on another property to develop')

                if alert.heading == 'Trade with Eve?' or alert.heading == 'Accept trade?':
                    alert = Alert('Fair enough', 'Eve is probably smarter #than you anyway.')
                    rejectedTrades.append([Eve.offer, user.offer])
                    moneyToTake = MoneyOffer(0)
                    moneyToGive = MoneyOffer(0)
                    EveOffer = ''
                    userOffer = ''
                    user.offer = []
                    Eve.offer = []
                    offerAlert = []
                    requestAlert = []
                    user.isTrading = False
                    Eve.isTrading = False

                if alert.heading == 'Mortgage and friends':
                    alert = Alert('You sure?', 'I heard mortgages were #really trendy in 2020')

                if alert.heading == 'Mortgage':
                    alert = Alert('Flipper-flopper', 'You\'re a flipper flopper #aren\'t you mate')

                if alert.heading == 'Memories from 2008':
                    alert = Alert('OK chief', 'Maybe you should mortgage #some properties or something')

            if alert.confirmOrDeny() == 'confirmed':
                if alert.heading == 'Unowned Property':
                        squares[user.boardpos].rejected = True
                        squares[user.boardpos].owner = user
                        user.money -= squares[user.boardpos].getPrice()
                        alert = Alert('', '')

                if alert.heading == 'You sure mate?':
                    winner = Eve

                if alert.heading == 'Get out of Jail Free?':
                        alert = Alert('Dodgy Dealing', "You did some dodgy deals #but hey, haven't we all")
                        user.getOutOfJailFreeCards.remove(user.getOutOfJailFreeCards[0])
                        user.inJail = False
                        user.jailTurns = 0

                if alert.heading == 'Chance':
                    for cardBoi in chance:
                        if alert.body.__contains__(cardBoi.text):
                            if not cardBoi.executed:
                                cardBoi.execute(user)
                                cardBoi.executed = True

                if alert.heading == 'Community Chest':
                    for cardBoi2 in communityChest:
                        if alert.body.__contains__(cardBoi2.text):
                            if not cardBoi2.executed:
                                cardBoi2.execute(user)
                                cardBoi2.executed = True

                if alert.heading == 'Build?':
                    user.isDeveloping = True
                    user.isTrading = False
                    user.isMortgaging = False
                    alert = Alert('Building', 'Select a property to #develop')

                if alert.heading == 'Build house?':
                    for prop in properties:
                        if alert.body.__contains__(prop.name):
                            for comparisonProp in streets[prop.colour]:
                                if prop.houses > comparisonProp.houses:
                                    alert = Alert('Communist ideology', 'You have to develop your #properties equally.')
                            if prop.houses < 4 and not alert.heading == 'Communist ideology':
                                prop.houses += 1
                                user.money -= prop.getCostOfHouse()
                                alert = Alert('Bob the builder', 'You built 1 house on ' + prop.name)
                            elif prop.houses == 4 and not alert.heading == 'Communist ideology':
                                prop.houses += 1
                                user.money -= prop.getCostOfHouse()
                                alert = Alert('Fancy fancy', 'You built a hotel on ' + prop.name)
                            elif not alert.heading == 'Communist ideology':
                                alert = Alert('Nah mate',
                                              "My programming is dodgy but it #ain't that dodgy. No developing #past hotels")

                if alert.heading == 'Trade with Eve?':
                    user.isDeveloping = False
                    user.isTrading = True

                if alert.heading == 'Trade' or alert.heading == 'Accept trade?':

                    if isDodgy():
                        alert = Alert("Friendship is magic", "Everyone in " + isDodgy()[
                            1] + " street are best #friends! You can't separate them.")

                    elif AI.wantsTrade(user.offer, Eve.offer):
                        alert = Alert('Trade successful', "Well done")

                        for item in user.offer:
                            if type(item) == Property:
                                item.owner = Eve
                        for item in Eve.offer:
                            if type(item) == Property:
                                item.owner = user

                        user.money += moneyToTake.value - moneyToGive.value
                        Eve.money += moneyToGive.value - moneyToTake.value

                    else:
                        alert = Alert('Not falling for that', 'Eve has declined the trade.')

                    moneyToTake = MoneyOffer(0)
                    moneyToGive = MoneyOffer(0)
                    EveOffer = []
                    userOffer = []
                    user.offer = []
                    Eve.offer = []
                    offerAlert = []
                    requestAlert = []
                    user.isTrading = False
                    Eve.isTrading = False

                if alert.heading == 'Mortgage and friends':
                    alert = Alert('Manage properties', 'Select a property to manage')
                    user.isMortgaging = True
                    user.isDeveloping = False
                    user.isTrading = False

                if alert.heading == 'Mortgage':
                    for prop in properties:
                        if alert.body.__contains__(prop.name) and not prop.mortgaged:
                            cantSell = False
                            if prop.colour <= 7:
                                for neighbour in streets[prop.colour]:
                                    if neighbour.houses > prop.houses:
                                        cantSell = True
                                        break
                                if cantSell:
                                    alert = Alert('Communist ideology', 'You have to develop your #properties equally.')
                                else:
                                    prop.mortgaged = True
                                    user.money += int(prop.getPrice() / 2)
                                    alert = Alert('Manage properties', 'Select a property to manage')
                            elif prop.colour == 8 or prop.colour == 9:
                                prop.mortgaged = True
                                user.money += int(prop.getPrice() / 2)
                                alert = Alert('Manage properties', 'Select a property to manage')

                if alert.heading == 'Unmortgage':
                    for prop in properties:
                        if alert.body.__contains__(prop.name) and prop.mortgaged:
                            prop.mortgaged = False
                            user.money -= prop.getPrice()
                            alert = Alert('Manage properties', 'Select a property to manage')

                if alert.heading == 'Sell house?':
                    for prop in properties:
                        if alert.body.__contains__(prop.name) and prop.houses > 0:
                            cantSell = False
                            for neighbour in streets[prop.colour]:
                                if neighbour.houses > prop.houses:
                                    cantSell = True
                                    break
                            if cantSell:
                                alert = Alert('Communist ideology', 'You have to develop your #properties equally.')
                            else:
                                prop.houses -= 1
                                user.money += int(prop.getCostOfHouse()*0.9)
                                alert = Alert('Manage properties', 'Select a property to manage')

                if alert.heading == 'They see me rollin\'':
                    user.normalGameplay = True
                    user.inJail = False
                    user.timeMoving = roll

                if alert.heading == 'Serial doubles-roller':
                    user.inJail = True
                    user.jailTurns = 0
                    user.doublesCount = 0
                    alert = Alert('', '')

                if alert.heading == 'Not-so-smooth criminal':
                    user.jailTurns = 0
                    user.inJail = True
                    user.canRoll = False
                    alert = Alert('', '')

                if alert.heading == 'Memories from 2008':
                    winner = Eve

                if type(alert) == EveAlert:

                    if alert.heading == 'Auction over':
                        Eve.normalGameplay = True

                    if alert.heading == 'Another one bytes the dust':
                        winner = user
                        Eve.isTurn = False
                        user.isTurn = False
                        break

                    if alert.heading == 'The Australian Dream':
                        for prop in mortgagedProps:
                            Eve.money -= prop.getPrice()
                            prop.mortgaged = False
                            mortgagedProps = []

                    if alert.heading == 'Escaping CAPTCHA' or alert.heading == 'Escaping reCAPTCHA':
                        Eve.jailTurns = 0
                        Eve.inJail = False
                        Eve.normalGameplay = True
                        Eve.timeMoving = roll

                    if alert.heading == 'Destructobot':
                        Eve.normalGameplay = False
                        Eve.timeMoving = 0
                        Eve.inJail = True
                        Eve.canRoll = False

                    if alert.heading == 'Artificial estate agent':
                        currentSquare.owner = Eve
                        Eve.money -= currentSquare.getPrice()

                    if alert.heading == 'Rent':
                        Eve.money -= currentSquare.rent
                        currentSquare.owner.money += currentSquare.rent
                        currentSquare.paidRent = True

                    if alert.heading.__contains__('Eve -'):
                        if alert.heading.__contains__('Community Chest'):
                            for cardBoi in communityChest:
                                if alert.body.__contains__(cardBoi.text):
                                    if not cardBoi.executed:
                                        cardBoi.execute(Eve)
                                        cardBoi.executed = True
                        elif alert.heading.__contains__('Chance'):
                            for cardBoi in chance:
                                if alert.body.__contains__(cardBoi.text):
                                    if not cardBoi.executed:
                                        cardBoi.execute(Eve)
                                        cardBoi.executed = True


                    if alert.body.__contains__('Eve paid'):
                        for square in squares:
                            if alert.heading == square.name:
                                if not square.paid:
                                    Eve.money -= square.getTax()
                                    freeParking += square.getTax()
                                    square.paid = True

                    if alert.heading == 'Artificial unintelligence':
                        Eve.normalGameplay = False
                        Eve.canRoll = False
                        Eve.inJail = True
                        Eve.jailTurns = 0

                    if alert.heading == 'Escaping CAPTCHA' or alert.heading == 'Escaping reCAPTCHA':
                        alert = EveAlert('', '')

                    elif alert.heading.__contains__('Community Chest'):
                        for cardBoi in communityChest:
                            if alert.body.__contains__(cardBoi.text):
                                if cardBoi.type == 'move':
                                    alert = EveAlert('', '')
                                else:
                                    alert = Alert('', '')
                    elif alert.heading.__contains__('Chance'):
                        for cardBoi in chance:
                            if alert.body.__contains__(cardBoi.text):
                                if cardBoi.type == 'move' or cardBoi.type == 'nearestu' or cardBoi.type == 'nearests':
                                    alert = EveAlert('', '')
                                else:
                                    alert = Alert('', '')
                    else:
                        alert = Alert('', '')



            if alert.type == 'auction' and clickingOnButton():
                if not alert.body.__contains__('finish the auction'):
                    alert.body += '#finish the auction'

            elif auctioning and type(alert) == Auction:
                alert.checkCalc()

        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    if user.isTurn and (beginning or not((type(alert) == EveAlert) or alert.heading == 'Memories from 2008')):
        if not user.canRoll and user.timeMoving <= 0 and not alert.body.__contains__('?'):
            etAvailable = True

        if user.normalGameplay:
            user.move()
            if user.timeMoving == 0:

                currentSquare = squares[user.boardpos]

                if type(currentSquare) == Property:
                    if currentSquare.owner == bank and not currentSquare.rejected:
                        if not (alert.body.__contains__('Answer the question woodja')):
                            alert = Alert('Unowned Property',
                                          'Buy ' + currentSquare.name + ' for $' + str(currentSquare.getPrice()) + '?')
                    elif currentSquare.owner == Eve:
                        if currentSquare.mortgaged:
                            alert = Alert('Lucky', currentSquare.name + ' is mortgaged.')
                        elif not currentSquare.paidRent:
                            user.money -= currentSquare.rent
                            currentSquare.owner.money += currentSquare.rent
                            alert = Alert('Rent', ('You paid $' + str(
                                currentSquare.rent) + ' rent to ' + currentSquare.owner.name))
                            currentSquare.paidRent = True
                    elif currentSquare.owner == user:
                        if len(currentSquare.name) > 10:
                            alert = Alert('Home sweet home', 'You take a nice rest in #' + currentSquare.name)
                        else:
                            alert = Alert('Home sweet home', 'You take a nice rest in ' + currentSquare.name)

                elif type(currentSquare) == Chance:
                    if not card:
                        card = currentSquare.pickCard()

                    if not alert.body.__contains__('You gotta click "OK" mate'):
                        alert = Alert(currentSquare.name, card.text)
                    if card.executed:
                        alert = Alert('', '')

                elif type(currentSquare) == TaxSquares:
                    if not currentSquare.paid:
                        user.money -= currentSquare.getTax()
                        freeParking += currentSquare.getTax()
                        currentSquare.paid = True
                    alert = Alert(currentSquare.name,
                                  'You paid $' + str(currentSquare.getTax()) + ' ' + currentSquare.name)

                elif type(currentSquare) == SpecialSquares and not beginning:
                    if not currentSquare.paid:
                        user.money += currentSquare.getPayAmount(freeParking)
                        if currentSquare.name == 'Free Parking':
                            freeParking = 0
                        elif currentSquare.name == 'Jail' and not user.inJail:
                            alert = Alert('Just visiting', "Isn't it fun to gloat at #the people in jail")
                        currentSquare.paid = True
                    if currentSquare.name == 'Go To Jail':
                        alert = Alert('Not-so-smooth criminal',
                                      'You got caught jaywalking. #You were sent to jail, #as the public must be protected #from your villany at #all costs')

        if user.inJail and not alert.heading == 'They see me rollin\'':
            user.boardpos = 10
            if user.jailTurns >= 3:
                if len(user.getOutOfJailFreeCards) > 0:
                    alert = Alert('Get out of Jail Free?', 'Do you wish to use a #get out of jail free card?')
                else:
                    alert = Alert('A free man', 'You paid $50 to #get out of jail.')
                    user.money -= 50
                    user.inJail = False
                    user.jailTurns = 0
            elif user.jailTurns > 0:
                if alert.heading == '':
                    alert = Alert('Do penance, sinner', ('You have ' + str(3 - user.jailTurns) + ' turns left in jail'))

        if user.isTrading:
            offerAlert = 'You are offering: '
            requestAlert = 'You are requesting: '
            for prop in user.offer:
                if user.offer.index(prop) % 3 == 1:
                    offerAlert = offerAlert + '#'
                if len(user.offer) > 1 and user.offer.index(prop) == len(user.offer) - 2:
                    offerAlert = offerAlert + prop.name + ' and '
                elif user.offer.index(prop) == len(user.offer) - 1:
                    offerAlert = offerAlert + prop.name
                else:
                    offerAlert = offerAlert + prop.name + ', '

            for prop in Eve.offer:
                if Eve.offer.index(prop) % 3 == 0:
                    requestAlert = requestAlert + '#'
                if len(Eve.offer) > 1 and Eve.offer.index(prop) == len(Eve.offer) - 2:
                    requestAlert = requestAlert + prop.name + ' and '
                elif Eve.offer.index(prop) == len(Eve.offer) - 1:
                    requestAlert = requestAlert + prop.name
                else:
                    requestAlert = requestAlert + prop.name + ', '

            if not betterTradeMessage:
                alert = Alert('Trade', offerAlert + '#' + requestAlert)

            else:
                alert = Alert('Trade', offerAlert + '#' + requestAlert + '#Better sort out your trade first')

    elif Eve.isTurn:
        if Eve.canRoll and Eve.timeMoving == 0 and not auctioning and alert.confirmed and alert.type != EveAlert:

            Eve.paidOOJ = False
            beginning = False
            Eve.normalGameplay = True
            Eve.isMortgaging = False
            Eve.isTrading = False
            Eve.isDeveloping = False
            auctioning = False
            alert.confirmed = False

            throw = rollDice(die)
            buttonActions[0] = True
            roll = throw[0].value + throw[1].value

            for square in squares:
                if type(square) == Property:
                    if square.colour == 9:
                        square.rent = square.getInitialRent()
                    square.rejected = False
                    square.paidRent = False

                elif type(square) == TaxSquares or type(square) == SpecialSquares:
                    square.paid = False

            for comcard in communityChest:
                comcard.executed = False
            for chancecard in chance:
                chancecard.executed = False
            card = None

            if throw[0] == throw[1] and Eve.doublesCount < 3:
                Eve.canRoll = True
                if Eve.inJail:
                    if not alert.confirmed:
                        if Eve.firstTimeInJail:
                            alert = EveAlert('Escaping CAPTCHA', 'Eve rolls doubles and gets #out of jail. Nice.')
                            Eve.inJail = False
                            Eve.normalGameplay = False
                        else:
                            alert = EveAlert('Escaping reCAPTCHA', 'Eve rolls doubles and gets #out of jail. Nice.')
                            Eve.inJail = False
                            Eve.normalGameplay = False
                        Eve.firstTimeInJail = False
                Eve.doublesCount += 1
            else:
                Eve.canRoll = False
            if Eve.doublesCount >= 3:
                Eve.normalGameplay = False
                if not alert.confirmed:
                    alert = EveAlert('Destructobot',
                                 'Uh-oh. Eve has committed #unspeakable acts- namely, #rolling doubles 3 times in #a row')
            if Eve.inJail and not alert.heading.__contains__('Escaping'):
                Eve.timeMoving = 0
                Eve.jailTurns += 1
            elif not alert.heading == 'Destructobot':
                Eve.timeMoving = roll

        if not Eve.canRoll and Eve.timeMoving == 0 and not auctioning and type(alert) != EveAlert:

            if Eve.money < 0:

                Eve.normalGameplay = False
                actions = AI.emergencyAction()
                if not actions[2]:
                    alert = EveAlert('Another one bytes the dust', '')
                else:
                    alert = EveAlert('Stayin\' Alive', '')
                alert.smallFont = True
                if len(actions[0])>0:
                    EveDemMes = 'Eve demolished: '
                    i = 0
                    while len(actions[0]) > 0:
                        prop = actions[0][0]
                        numOfHousesSold = actions[0].count(prop)
                        while prop in actions[0]:
                            actions[0].remove(prop)
                        if i % 2 == 0:
                            EveDemMes += '#'
                        EveDemMes += str(numOfHousesSold) + ' house'
                        if numOfHousesSold > 1:
                            EveDemMes += 's'
                        EveDemMes += ' in ' + prop.name

                        if not(len(actions[0]) == 0):
                            EveDemMes += ', '
                        i += 1
                    alert.body += EveDemMes + '#'

                if len(actions[1]) > 0:
                    EveMortMes = 'Eve mortgaged '
                    for prop in actions[1]:
                        if actions[1].index(prop) % 3 == 1:
                            EveMortMes += '#'
                        if 0 < actions[1].index(prop) == len(actions[1]) - 1:
                            EveMortMes += 'and '
                        EveMortMes += prop.name
                        if actions[1].index(prop) < len(actions[1]) - 1 and not len(actions[1]) == 0:
                            EveMortMes += ','
                    alert.body += EveMortMes + '#'
                if not actions[2]:
                    alert.body += 'Eve has $' + str(0-Eve.money) +' of debt and has #declared bankruptcy.'

            Eve.isTurn = False
            user.isTurn = True
            user.normalGameplay = False
            Eve.doublesCount = 0

        if Eve.normalGameplay and alert.heading != 'Another one bytes the dust' and alert.heading != 'Stayin\' alive':

            Eve.move()
            if Eve.timeMoving == 0:
                currentSquare = squares[Eve.boardpos]

                if type(currentSquare) == Property:
                    if currentSquare.owner == bank and not currentSquare.rejected:
                        if AI.wantsProp(currentSquare):

                            if not alert.confirmed:
                                alert = EveAlert('Artificial estate agent',
                                          'Eve buys ' + currentSquare.name + ' for $' + str(currentSquare.getPrice()))
                        else:

                            alert = Auction(currentSquare)
                            auctioning = True
                            alert.highestBid = 0
                            alert.winner = None
                            user.bid = '0'
                            Eve.bid = '0'
                        currentSquare.rejected = True
                    elif currentSquare.owner == user:

                        if currentSquare.mortgaged:
                            if not alert.confirmed:
                                alert = EveAlert('Unlucky', currentSquare.name + ' is mortgaged.')

                        elif not currentSquare.paidRent:
                            if not alert.confirmed:
                                alert = EveAlert('Rent', ('Eve paid $' + str(currentSquare.rent) + ' rent to you.'))

                    elif currentSquare.owner == Eve and not alert.heading == 'Artificial estate agent':

                        if len(currentSquare.name) > 9:
                            if not alert.confirmed:
                                alert = EveAlert('Vibin\'', 'Eve takes a nice rest in #' + currentSquare.name)
                        else:
                            if not alert.confirmed:
                                alert = EveAlert('Vibin\'', 'Eve takes a nice rest in ' + currentSquare.name)


                elif type(currentSquare) == Chance:
                    if not card:
                        card = currentSquare.pickCard()

                    if not alert.confirmed:
                        alert = EveAlert('Eve - ' + currentSquare.name, card.text)

                elif type(currentSquare) == TaxSquares:
                    if not alert.confirmed:
                        alert = EveAlert(currentSquare.name,'Eve paid $' + str(currentSquare.getTax()) + ' ' + currentSquare.name)

                elif type(currentSquare) == SpecialSquares and not beginning:

                    if not currentSquare.paid:
                        Eve.money += currentSquare.getPayAmount(freeParking)

                        if currentSquare.name == 'Free Parking':
                            if not alert.confirmed:
                                alert = EveAlert('Free Parking', 'Eve got $' + str(freeParking) + ' from free parking.')
                            freeParking = 0
                        elif currentSquare.name == 'Jail' and not Eve.inJail:
                            if not alert.confirmed:
                                alert = EveAlert('Visiting the people zoo',
                                          "When Eve takes over the world, #all the humans will be in cages #just like the one she sees #before her")
                        currentSquare.paid = True

                    if currentSquare.name == 'Go To Jail':
                        if not alert.confirmed:
                            alert = EveAlert('Artificial unintelligence',
                                      'Eve got caught robbing #a bank. Clearly AI still has a #long way to go.')

                if alert.confirmed and Eve.money > 0 and type(alert) != Auction and not Eve.inJail:

                    developCountries = []
                    for i in range(15):
                        for street in streets:
                            if street[0].streetOwned and street[0].owner == Eve and streets.index(street) <= 7:
                                country = AI.develop(street)
                                if country and not country in developCountries:
                                    developCountries.append(country)
                    if len(developCountries) == 0:
                        alert = EveAlert('Finished turn', 'Eve has finished her turn')
                        if not (type(AI.itemsToTrade()[0]) == bool) and AI.wantsTrade(AI.itemsToTrade()[1], AI.itemsToTrade()[0]):
                            EveOffer = 'Eve is offering: '
                            Eve.offer = AI.itemsToTrade()[0]
                            EveRequest = 'Eve is requesting: '
                            user.offer = AI.itemsToTrade()[1]
                            for prop in AI.itemsToTrade()[0]:
                                if Eve.offer.index(prop) % 3 == 1:
                                    EveOffer += '#'
                                if 0 < Eve.offer.index(prop) == len(Eve.offer) - 1:
                                    EveOffer += 'and '
                                EveOffer += prop.name
                                if Eve.offer.index(prop) < len(Eve.offer) - 1 and not len(Eve.offer) == 0:
                                    EveOffer += ', '
                            for prop in user.offer:
                                if user.offer.index(prop) % 3 == 1:
                                    EveRequest += '#'
                                if 0 < user.offer.index(prop) == len(user.offer) - 1:
                                    EveRequest += 'and '
                                EveRequest += prop.name
                                if user.offer.index(prop) < len(user.offer) - 1 and not len(user.offer) == 0:
                                    EveRequest += ', '
                            alert = Alert('Accept trade?', EveOffer + '#' + EveRequest + '#Do you accept?')
                        else:
                            mortgagedProps = []
                            for prop in properties:
                                if prop.owner == Eve and prop.mortgaged:
                                    totalCost = 0
                                    for prop2 in mortgagedProps:
                                        totalCost += prop2.getPrice()
                                    if Eve.money > totalCost + prop.getPrice():
                                        mortgagedProps.append(prop)

                            if len(mortgagedProps) > 0:
                                alert = EveAlert('The Australian Dream', 'Eve unmortgaged: ')
                                unmortgageText = ''
                                for prop in mortgagedProps:
                                    if mortgagedProps.index(prop) % 3 == 1:
                                        unmortgageText += '#'
                                    if 0 < mortgagedProps.index(prop) == len(mortgagedProps) - 1:
                                        unmortgageText += 'and '
                                    unmortgageText += (prop.name)
                                    if mortgagedProps.index(prop) < len(mortgagedProps) - 1:
                                        unmortgageText += ', '
                                alert.body += unmortgageText
                    else:
                        alert = EveAlert('Developing countries', 'Eve developed ')
                        for prop in developCountries:
                            if type(prop) == Property:
                                if developCountries.index(prop) % 3 == 1:
                                    alert.body += '#'
                                if 0 < developCountries.index(prop) == len(developCountries) - 1:
                                    alert.body += 'and '
                                alert.body += prop.name
                                if developCountries.index(prop) < len(developCountries) - 1 and not len(developCountries) == 0:
                                    alert.body += ', '

        if Eve.inJail and alert.heading != 'Stayin\' Alive' and alert.heading != 'Another one bytes the dust' and alert.heading != 'Developing countries':
            Eve.doublesCount = 0
            Eve.boardpos = 10
            if Eve.jailTurns >= 3:
                if AI.useGojf():
                    Eve.getOutOfJailFreeCards.remove(Eve.getOutOfJailFreeCards[0])
                    Eve.inJail = False
                    Eve.jailTurns = 0
                else:
                    if not Eve.paidOOJ:
                        Eve.money -= 50
                        Eve.paidOOJ = True

                if Eve.firstTimeInJail:
                    if not alert.confirmed:
                        alert = EveAlert('Escaping CAPTCHA', 'Eve has gotten out of jail')
                else:
                    if not alert.confirmed:
                        alert = EveAlert('Escaping reCAPTCHA', 'Eve has gotten out of #jail- again.')

                Eve.firstTimeInJail = False

            elif Eve.jailTurns >= 0:
                if not alert.confirmed:
                    alert = EveAlert('Bot detection', ('Eve has ' + str(3 - Eve.jailTurns) + ' turns left in jail'))



    if auctioning and type(alert) == Auction:

        alert.turnsSincePlayerBid += 1
        if alert.turnsSincePlayerBid == 20:

            if int(Eve.bid) > alert.highestBid:
                alert.highestBid = Eve.bid
                alert.body = 'Your turn'
                alert.winner = Eve

        if alert.EveRejected:
            if alert.heading == 'Auction' and alert.winner:
                auctionProp = alert.prop
                auctionWinner = alert.winner
                moneySpent = alert.highestBid
                auctionProp.owner = auctionWinner
                auctionWinner.money -= moneySpent
                auctioning = False
                Eve.normalGameplay = False
                alert = EveAlert('Auction over',
                              auctionWinner.name + ' bought ' + auctionProp.name + ' for $' + str(moneySpent))

    if beginning:
        alert = welcome
        screen.blit(dieOne.image, (188 + 11 + 37, 210 + 33))
        screen.blit(dieOne.image, (188 + 38 + 150, 210 + 33))

    alert.write()

    playerCardpos = [995, 145]
    for gojfcard in user.getOutOfJailFreeCards:
        screen.blit(gojfcard.value, (playerCardpos))
        playerCardpos[0] += 10
        playerCardpos[1] += 2

    EveCardpos = [1050, 650]
    for Evegojfcard in Eve.getOutOfJailFreeCards:
        screen.blit(Evegojfcard.value, (EveCardpos))
        EveCardpos[0] += 10
        EveCardpos[1] += 2

    draw(Eve, (Eve.getPos()))
    draw(user, (user.getPos()))

    pygame.display.update()


# -------------------------------------------------------------------------------
# GAME OVER SCREEN

prevScreen = None
currScreen = None
while True:
    screen.fill(winner.colour)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    while currScreen == prevScreen:
        currScreen = random.choice(winner.screens)

    screen.blit(currScreen, (0, 0))
    prevScreen = currScreen

    pygame.display.update()
    time.sleep(0.2)