import discord
from discord.ext import commands
import random
from math import ceil
import os
diff_dic = {'veryeasy':2.,'easy':1.5,'normal':1.,'standard':1.,'hard':2/3,'formidable':1/2,'herculean':1/10}
succ_dic = {1:'Critical Success',2:'Success',3:'Failure',4:'Critical Failure'}
token = os.getenv("MYTHRASBOT_TOKEN")
client = discord.Client()
bot = commands.Bot('$')
@bot.command()
async def roll(ctx):
    roll = random.randint(1,100)
    await ctx.send('rolled ' + str(roll))
@bot.command()
async def skillroll(ctx,skill1,difficulty1):
    skill1 = int(skill1)
    effective_skill1 = ceil(skill1*diff_dic[difficulty1])
    roll = random.randint(1,100)
    if roll <= effective_skill1/10:
        success1 = 'Critical Success!!!'
    elif roll <= effective_skill1:
        success1 = 'Success'
    elif roll > effective_skill1:
        success1 = 'Failed'
    if ((roll >= 99 and skill1 <=100) or (roll == 100 and skill1 > 100)):
        success1 = 'Critical Failure!!! Good luck!'
    await ctx.send('rolled ' + str(roll) + ' against the required ' + str(effective_skill1))
    await ctx.send(success1)
@bot.command()
async def contestedroll(ctx,skill1,difficulty1,skill2,difficulty2):    
    skill1 = int(skill1)
    skill2= int(skill2)    
    roll1 = random.randint(1,100)
    roll2 = random.randint(1,100)     
    difficulty1 = difficulty1.lower()
    difficulty2 = difficulty2.lower()
    effective_skill1 = ceil(skill1*diff_dic[difficulty1])
    effective_skill2 = ceil(skill2*diff_dic[difficulty2])
    maximum_skill = max(effective_skill1,effective_skill2)
    if maximum_skill > 100:
        effective_skill1 = effective_skill1 - maximum_skill + 100
        effective_skill2 = effective_skill2 - maximum_skill + 100
        if effective_skill1 < 5:
            effective_skill1 = 5
        if effective_skill2 < 5:
            effective_skill2 = 5    
    if roll1 <= effective_skill1/10:
        success1 = 1
    elif roll1 <= effective_skill1:
        success1 = 2
    elif roll1 > effective_skill1:
        success1 = 3
    if ((roll1 >= 99 and skill1 <=100) or (roll1 == 100 and skill1 > 100)):
        success1 = 4        
    if roll2 <= effective_skill2/10:
        success2 = 1
    elif roll2 <= effective_skill2:
        success2 = 2
    elif roll2 > effective_skill2:
        success2 = 3
    if ((roll2 >= 99 and skill2 <=100) or (roll2 == 100 and skill2 > 100)):
        success2 = 4        
    if success1 != success2:
        if success1 < success2:
            winner = 'Attacker'
            degrees = success2-success1
        if success1 > success2:
            winner = 'Defender'
            degrees = success1-success2
    else:
        if roll1>roll2:
            winner='Attacker'
            degrees = 0
        else:
            winner='Defender'
            degrees = 0     
    attacker_string = ('Attacker rolls ' + str(roll1) + ' with requirement of ' + str(effective_skill1) + ' - ' + succ_dic[success1])
    defender_string = ('Defender rolls ' + str(roll2) + ' with requirement of ' + str(effective_skill2) + ' - ' + succ_dic[success2])
    result_string   = (winner + ' wins with ' + str(degrees) + ' degree/s of success')
    await ctx.send(attacker_string)
    await ctx.send(defender_string)
    await ctx.send(result_string)
@contestedroll.error
async def contestedroll_error(ctx,error):
	await ctx.send('command is formatted: $contestedroll <skill1> <difficulty1> <skill2> <difficulty2>')
	await ctx.send('difficulties are: veryeasy, easy, normal, standard, hard, formidable, herculean')
@skillroll.error
async def skillroll_error(ctx,error):
	await ctx.send('command are formatted: $skillroll <rating> <difficulty>')
	await ctx.send('difficulties are: veryeasy, easy, normal, standard, hard, formidable, herculean')
@bot.command()
async def mythrasbot(ctx):
	await ctx.send('Hi, I am the MythrasBot. I can roll dice for you.')
	await ctx.send('command are formatted: $skillroll <rating> <difficulty>')
	await ctx.send('command is formatted: $contestedroll <skill1> <difficulty1> <skill2> <difficulty2>')
	await ctx.send('command is formatted: $roll')
	await ctx.send('difficulties are: veryeasy, easy, normal, standard, hard, formidable, herculean')
bot.run(token)
