import discord
from discord.ext import commands, tasks
import random
import datetime
import json
import pytz

intents = discord.Intents.all()

with open('config.json', 'r') as config_file:
    config = json.load(config_file)


cargos = [ 1199719733352742954, 1199720545420320859, 1199724268301336786, 1199724424803393657, 1199724673563369625, 1199724718102679592, 1199724774897750087, 1199724806128550009, 1199724895186206803, 1199724920280719360, 1199760512183959683]

bot = commands.Bot(command_prefix='/', intents=intents)

channel_id = 1205149500164018186

@bot.event
async def on_ready():
    print(f'{bot.user.name} está conectado! hora:{datetime.datetime.now()}')

    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s): {datetime.datetime.now()}')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

    enviar_mensagem.start()
    channel = bot.get_channel(channel_id)

    if channel:
        # Envia a mensagem
        await channel.send(f'{bot.user.name} está online!')

@tasks.loop(minutes=1)
async def enviar_mensagem():
    global envios_realizados

    fuso_horario_sao_paulo = pytz.timezone('America/Sao_Paulo')
    agora = datetime.datetime.now(fuso_horario_sao_paulo)
    horario_envio_manha = agora.replace(hour=10, minute=0, second=0, microsecond=0)
    horario_envio_tarde = agora.replace(hour=16, minute=0, second=0, microsecond=0)

    # Verificar se é dia útil (segunda a sexta)
    if agora >= horario_envio_manha and agora <= horario_envio_manha + datetime.timedelta(minutes=1):
        channel = bot.get_channel(channel_id)

        if channel:
            embed = discord.Embed(
                title='Bom dia galera!!!',
                description=f'{mencionar_cargos()}\n'
                            f'Passando para lembrar você de fazer seu commit do dia!\n'
                            f'{agora.strftime("%A, %d de %B")}\n'
                            f'Fuso horário: America/Sao_Paulo',
                color=discord.Color.gold()
            )
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1074755878273699870/1205135560864178227/developer.png?ex=65d744f4&is=65c4cff4&hm=84bd372293c92b220147e1760a07a305f258211492c5e069ddc92e77f49c9c89&")
            await channel.send(embed=embed)

    if agora >= horario_envio_tarde and agora <= horario_envio_tarde + datetime.timedelta(minutes=1):
        channel = bot.get_channel(channel_id)

        if channel:
            embed = discord.Embed(
                title='Boa Tarde galera!!!',
                description=f'{mencionar_cargos()}\n'
                            f'Já são 16:00 horas não se esqueça de realizar o seu commit do dia!\n'
                            f'{agora.strftime("%A, %d de %B")}\n'
                            f'Fuso horário: America/Sao_Paulo',
                color=discord.Color.gold()
            )
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1074755878273699870/1205135560864178227/developer.png?ex=65d744f4&is=65c4cff4&hm=84bd372293c92b220147e1760a07a305f258211492c5e069ddc92e77f49c9c89&")
            await channel.send(embed=embed)

def mencionar_cargos():
    mencao_cargos = ""
    for cargo_id in cargos:
        mencao_cargos += f'<@&{cargo_id}> '
    return mencao_cargos


@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello world!")

@bot.tree.command(name="mostrar_hora")
async def mostrar_hora(interaction: discord.Interaction):
    agora = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
    await interaction.response.send_message(f'Agora são {agora.strftime("%H:%M:%S")}')

@bot.tree.command(name="adicionar_membro")
async def adicionar_membro(interaction: discord.Interaction):
    global membros
    membros.append(int(interaction.data['options'][0]['value']))
    await interaction.response.send_message(f'Membro adicionado com sucesso!')

@bot.tree.command(name="remover_membro")
async def remover_membro(interaction: discord.Interaction):
    global membros
    membros.remove(int(interaction.data['options'][0]['value']))
    await interaction.response.send_message(f'Membro removido com sucesso!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

bot.run(config['token'])