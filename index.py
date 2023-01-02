# --------------- {Imports} --------------- #
import discord, os
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
os.system("clear||cls")

# --------------- {Settings} --------------- #
Token = os.getenv('TOKEN')
ServerID = int(os.getenv('SERVERID'))
RoleId = int(os.getenv('ROLEID'))
TagID = int(os.getenv('TAGID'))

Vanity = "dsc.gg/themoonlight"
Tags = {
  "ᵀᴹᴸ",
  "ᵀᵐˡ"
}

# --------------- {Start-Up} --------------- #
activity = discord.Activity(name="The Moon Light", type=discord.ActivityType.competing)
intents = discord.Intents( guilds=True,members=True,presences=True)
bot = commands.Bot(command_prefix="$", intents=intents, activity=activity, status=discord.Status.do_not_disturb)
bot.remove_command('help')

print('''\033[1;31;40m
 _   _                   _   _  
| | | |                 (_) | |
| | | |   __ _   _ __    _  | |_   _   _ 
| | | |  / _` | | '_ \  | | | __| | | | |
\ \_/ / | (_| | | | | | | | | |_  | |_| |
 \___/   \__,_| |_| |_| |_|  \__|  \__, |
                                    __/ |
                                  |___/ 
''')

# --------------- {Bot Ready} --------------- #
@bot.event
async def on_ready():
  print(f"\033[1m{bot.user} is Ready")
   
# --------------- {Status Update} --------------- #
@bot.event
async def on_presence_update(before, after):
  if str(after.raw_status) == "offline":
    return
  
  ActualStatus = ""
  PreviousStatus = ""

  try:
    for CurrentStatuses in after.activities:
      if 'custom' in CurrentStatuses.type:
        ActualStatus = CurrentStatuses.name
  except Exception:
    pass

  try:
    for OldStatuses in before.activities:
      if 'custom' in OldStatuses.type:
        PreviousStatus = OldStatuses.name
  except Exception:
    pass

  if Vanity in ActualStatus:
    if not Vanity in PreviousStatus:
      role = after.guild.get_role(RoleId)
      print(role, type(role))
      await after.add_roles(role, reason=f"{Vanity} $supporter")
        
  if not Vanity in ActualStatus:
    role = after.guild.get_role(RoleId)
    if role in after.roles:
      await after.remove_roles(role, reason=f"Not {Vanity} $supporter")
      
# --------------- {User Update} --------------- #
@bot.event
async def on_user_update(before, after):
  ActualName = after.name
  FoundTag = False

  for tag in Tags:
    if tag in ActualName:
      FoundTag = True

  if FoundTag:
    guild = bot.get_guild(ServerID) 
    try:
      TagUser = guild.get_member(after.id)
      role = guild.get_role(TagID)
      if not role in TagUser.roles:
        await TagUser.add_roles(role, reason=f"Tag $supporter")
    except Exception as e:
      print(e)

  if not FoundTag:
    guild = bot.get_guild(ServerID) 
    try:
      TagUser = guild.get_member(after.id)
      role = guild.get_role(TagID)
      if role in TagUser.roles:
        await TagUser.remove_roles(role, reason=f"Not Tag $supporter")
    except Exception as e:
      print(e)

bot.run(Token)
