import discord
from discord.ext import commands

#試験モードのオンオフ(有効:0、無効:1)
testmode = 0

#バージョン
versioninfo = 'ver.1.1'

#試験モードの条件分岐
if testmode == 0 :
    TOKEN = 'テストモード時に動かすBotのアクセストークン'
    information = '開発版'
    client = commands.Bot(command_prefix = '!t!')

if testmode == 1 :
    TOKEN = '本番環境のBotのアクセスコード'
    information = 'リリース版'
    client = commands.Bot(command_prefix = '!!')

#Bot情報
developerinfo = 'Developer: Nagito Hisanagi \nBlog: https://snmochizuki.net/pcdr/\nGitHub: https://github.com/BATOER-0605'
BOTID='Bot番号:HN01'

#起動時のイベント
@client.event
async def on_ready():
    CHANNEL_ID = チャンネルID
    channel = client.get_channel(CHANNEL_ID)
    if testmode == 1 :
        await channel.send('起動完了', delete_after=10.0 )
        print('起動完了：')
        print(versioninfo)
    if testmode == 0 :
        await channel.send('テストモード有効：起動完了', delete_after = 10.0 )
        print('テストモード有効：起動完了')
        print(versioninfo)
        
#testコマンド
@client.command()
async def test(ctx):
    await ctx.send('Test OK')

#概要
@client.command()
async def intro(ctx):
    await ctx.send('こんにちは！\n私が何をできるか紹介するよ！')
    await ctx.send('1, みんなの現時点での各教科の評定診断ができるよ！（!!hyoutei　で詳細を確認）')
    await ctx.send('2, このBotの開発者の情報が見れるよ！（!!info　で確認可能）')
    await ctx.send('\n「!!intro」でこのメッセージを再表示可能（!!helpでコマンドリスト）')
    await ctx.send('機能は増えていく予定なのでリクエストがあれば「!!request」のリンクから！')

#リクエストURL
@client.command()
async def request(ctx):
    await ctx.send('リクエストURL\nこのBotのBot番号:HN01\n https://forms.gle/2E5oApuRxcjDeDh47')

#評定診断詳細
@client.command()
async def hyoutei(ctx):
    await ctx.send('機能名：評定診断プログラム\n説明：あなたの現在の評定を算出し、赤点かどうかを判定します。\n備考：評定割合は百分率です。％は書かなくていいです。\nver.1.1')


#botの情報を表示するコマンド
@client.command()
async def info(ctx):
    await ctx.send(information)
    await ctx.send(versioninfo)
    await ctx.send(developerinfo)
    await ctx.send(BOTID)

#評定診断起動
@client.command()
@commands.dm_only()
async def hs(message):
    def check(waited_message):
        is_dm = type(waited_message.channel) == discord.DMChannel
        is_same_user = waited_message.author == message.author
        return is_dm and is_same_user

    #各評定割合を入力
    await message.author.send('課題評価割合を入力(半角)')
    kadai_persent = await client.wait_for('message',check=check)
    await message.author.send('試験評価割合を入力(半角)')
    test_persent = await client.wait_for('message',check=check)

    #各点数を入力
    await message.author.send('課題の点数を入力(半角、課題を全部出していれば100を入力)')
    kadai_score = await client.wait_for('message',check=check)
    await message.author.send('試験の点数を入力(半角\n※平均点)')
    test_score = await client.wait_for('message',check=check)

    #評定を計算
    kadai = float(kadai_score.content) * float(kadai_persent.content) / 100
    test = float(test_score.content) * float(test_persent.content) / 100
    score = kadai + test

    #結果が赤点なら警告を出して結果を表示
    if score<60 :
        await message.author.send('【警告】あなたは『赤点』です！！')

    else:
        await message.author.send('まだ舞えます。この調子で頑張りましょう！（評定は黒点です）')

    await message.author.send(score)
    
#トークン
client.run(TOKEN)