import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
from datetime import datetime
from typing import Optional
import asyncio
import random
import re
import json
from datetime import timezone

try:
    with open("discord_users.json", "r") as f:
        users = json.load(f)
except:
    users = {"all": [], "banned": []}

def save_users():
    with open("discord_users.json", "w") as f:
        json.dump(users, f, indent=2)

def add_user(uid, name):
    if not any(u["id"] == uid for u in users["all"]):
        users["all"].append({"id": uid, "name": name})
        save_users()

def is_banned(uid):
    return any(b["id"] == uid for b in users["banned"])

def ban_user(uid):
    if not is_banned(uid):
        name = next((u["name"] for u in users["all"] if u["id"] == uid), str(uid))
        users["banned"].append({"id": uid, "name": name})
        save_users()
        return True
    return False

def unban_user(uid):
    users["banned"] = [b for b in users["banned"] if b["id"] != uid]
    save_users()

OWNER_ID = "1401560538936508509"

# ---------------- ตัวแปรข้อความ ----------------

BOT_TOKEN = "

gy_ck # พ่อมึงตายสัสจังไรดูดม้าลูกทรพีหีแม่มึงเล็กหำพ่อมึงเล็กเกิดมาได้ไงวะก็ละงงทำตัวไม่มีประโยชชาติหมาชิบหาบไอชิบหายดิสก็กระจอกหัวดิสไม่ทำไรเลยโดนยิงนี้โง่จัดควายก็ควายสมองหมาชิบหายน่าขำวะสภาพดิสกระจอกดิสโง่ๆควายไก่วะคนเขมรรึไงวะไปเป็นเขมรเถอะสัสอีคางคกอิหมอยชนดกพ่อกับแมมีงน่าจะเย็ดกันถึงมีงมาได้แค่เย็ดแบบยัดหม่เข้าเพราะหีแม่มึงเท่ารูเข็มหำพ่อมึงสั้นควายๆโง่สมองหมาปัญญาควาย
"""

CHINESE_TEXT = """ # 更騎辺葬表庫属洗州返彬北材療。始到焦像検用選分坊吸高理益高優緊意物 先。継族読断利割共民等曜省様。発駆処持写約同周常定急同録誰量刊無国報地。下入症重秋超写知県去局能。聞状雨式国差小容最脚住自東信帯万権一。記将響和海演気気専味微国手私脅行門安子。在無境乗存能山間海式値朝氏料視密携見表録。議競索掲落遊典織知事告他草帯比選。都読急界害降年磐元解述切。芸気数法歌択表会先反状完東本経省死人北。分見供放転方貫将付横平歩辺本必。中芸購特点禁以経済記労止強開強載欲件。毛逮際企多向心更承芸町役疑。時禁請祐兵子木家策正康併求出平悩。父民歴新善乗准打員吐真方。病春終停書前出要際長心仙害害宿。野載法達係定側企未到全田携平認見爆変。終勝棺平天経済同州必目選。校済話朝九矢新公世投金方投日真受閣醸野。名応遇内事将和閣発政塾悪隣茶火多南注。間岩室趣方欲係難全障選階写衆題対末市。私欄埼最整杯隊増導中浜独。日治村歌映案行情産数院寺東協万雑。正車再部探爪価両覧変認近議犯本員。竹思西記雄機太済十入開印定愛。渡強殺丹全高火込田基江待意。転決葉囲著能笠味父速学斉。洋時合更数性芸弁今顧傷竹。定九事愛加当独時図考分術社能顧写人。聞映図合声毎選生円素巡暮議授可権阪表不基。考掲遂待閉来面本日目関毛題建刊歩写指。綬情淑基諒言最数可火月町舞門外文八高活。測経支健木司倍公際身平育宝論。井放煮読加約民得看乗芸一河線触注。客投掲素間松詐幕女供過援楽彩。記車合問伝続運表口井常画田。作球域回報来金禁素読義提体側理苦。本百億車社転社王総戻英理少高起江分主記能。宙件座運闘国共申済作紘引期景挑政問票黙。居氏言見健常画続業献終団線将伊。難塚刊知万犯挙山訴罪宮宣遠謝審流野。図挙内探状栗裏認衛車録校索。歴動室禁材木近産掲面徹宿用境。国者政恋実革社信海店週古転立護。屈図前者気支界確残円将有誕村断掲基特長季。券館体記規棋連図画地記拶庫中区勝図。問連崎理堂待本降顔件企拶年岐豊実部好町関。重購影著先区築模係水討流層表一必幻。生厚隠期祉教習短昨離導供世。社米門協半季以部稿大減回善著局撃響書。文大写幹方置付彩広市目無営辻日要。養査統事原属夜策公力然隆接渡写。感服選者駆横文存歩認新春昨料新分持授備行。暖返暮進治崎条文芸委町向士味実述武。黒年克際政画驚建陸家検者待山。会更申語投辞傷内得野権応取振必求丘突欄。産稿再政面藤彩武質完雑端実暮企見。急取米刑数界検議題高化入町烈人。売作日応貢施加情長文後江。多部医静素容盟原再光早化。出石努録一点航則講整遊長改提主足親。年用記働見乱信個安去制将発男。目田作公題紙安座化者仲集行。創伸線身役治三位博保政戦大桶。訴祉惑子期徒注来涯望済無。上載図況著著村広頭演形元雑囻半。訴主談燃球観甲界過翼投売多検利長。建特禁頂加人真初婚科結二義。年投導購催細要述類虚続入演。江情変現芸意束局利者原球社図。院週大打誕方模戦投第申知事。航書合現室稿合断術史記局陽社誠芸早装。載戦結就銀投知載核第手離持開己知。月行文山読能場生国上就国炎動明。職嗅掲午困称浅供村掲暮県有非藤多情。籍府児専ใน間腕責治風技表社応。日済長次孫書芸読入物出祐培新困局界葉月。本千群広温辞物戸強子囲事状互情込察棋画。鈴能予予碁案浜右無要見騒提犬敬保相。別駒己前仕持使布意生鯖始液。辱出情芸体他告時富概直牛市告照創芸定惑分。球製渡補要馬離都目受予最。欠烈命小速訴訪報野無堀提加索。正広謙部報時全警得月変警検最能性出整。栗主沖意似本総売都少参側。待業口真刊表提裁員週東本前仕紋度化。天康止囲影校金勝人帯本川尽体間様終各説。能団代同訴国議第提麺野補投縦話返福相学。止際構覧見写高打案故小国育者話埋言刊定土。柿符告任黒需術環情国負嘆要観民不。号京政回編究全文慮降役住。就歓校矢化稿提選況米造展供取村請。女戦語小校柔場億好供昇須属。働見乱信個安去制将発男。目田作公題紙安座化者仲集行。創伸線身役治三位博保政戦大桶。訴祉惑子期徒注来涯望済無。上載図況著著村広頭演形元雑囻半。訴主談燃球観甲界過翼投売多検利長。建特禁頂加人真初婚科結二義。年投導購催細要述類虚続入演。江情変現芸意束局利者原球社図。院週大打誕方模戦投第申知事。航書合現室稿合断術史記局陽社誠芸早装。載戦結就銀投知載核第手離持開己知。月行文山読能場生国上就国炎動明。職嗅掲午困称浅供村掲暮県有非藤多情。籍府児専ใน間腕責治風技表社応。日済長次孫書芸読入物出祐培新困局界葉月。本千群広温辞物戸強子囲事状互情込察棋画。鈴能予予碁案浜右無要見騒提犬敬保相。別駒己前仕持使布意生鯖始液
"""

KHMER_TEXT = # អូ! អី..........អ៉! អីសាច់ឆ្កែ អីដុសដី អីអណ្តាតបែកពីរ អីដុសស្មៅ អីឆ្កួតមួយរយប្រភេទ អីលលីកក្រោមដំបូល អីមុខត្រី អីឆ្អឹងក្រវ៉ាត់ទទេ អីគុណកញ់ អីត្រីមិនញ៉ាំអម្រាម អីផ្សិតបីពណ៌ អីឈីសបីរស អីសម្លេងសំឡេង អីដុសដែក អីក្មេងចង្វាក់ អីកំរិតចាស់ អីកំប៉ុងសុក អីខ្ចីលុយមិនសង អីថ្លើមឆា អំបិល អីវីរុសអេដស៍ អីសេះដុសលាមក អីស្នែងសុក អីធ្មេញបែក អីសាច់ឆ្កែ អីកណ្តុរដុស អីចុះទឹកក្រូចស្ងួត អីសម្លផ្លែកកក់ អីស្រែប្រហែលជំហ៊ាន អីចុះសម្លប្រហែល អីក្រូចក្រម៉ាត់ពេញរាង អីចង្វាក់មិនដឹងចប់ អីសព្វឡើងអឹម អីហឺតឡើងកំពង់ អីត្រីគ្រូចបែកធ្មេញ អីឆក់ផ្សែងឆ្វក អីមាន់សម្រាប់ក្រោយ អីគោដុសសព្វ អីកង្កែបឆា ឆ្ងាញ់ អីសត្វក្ងោកឆា ក្រម៉ក អីហ៊ីយ៉ាមធ្លាក់សេះ អីឆ្កែចាស់រ៉េវ អីរ៉េវឡើងក្រោយ អីធុងមក់លាមក អីល្អមិនដាច់អូន អីដើរមិនមើលផ្លូវ អីកាំងជាប់កំពង់ អីសេះគូងពុះ អីក្រពើកូងរហូត អីក្បាលអូនកាត់ អីក្រពើត្រីស្ងួត អីដាក់មិនចូលរន្ធ អីត្រីទូម៉ាក្លុង អីពីរអង្គត អីខ្ទឹមក្បាលក្នុងកំប៉ុង អីខួរក្បាលស្មើគ្រាប់សណ្តែក អីរាងកញ្ចក់មាន់ អីចិត្តត្រីស៊ីវ អីឃ្លានពេញមួយឆ្នាំ អីស្កក់មក់ក្លាយជាជាតិស៊ីន អីថ្មក្រោមដី អីសាញ់កុប្បកម្ម អីមុសិកភ្លេចគីយ៉ុង អីពណ៌ដាក់ផ្ទះ អីចាន់មុខក្រម៉ាត់ អីសត្វល្អិតសព្វសមីករណ៍ អីខ្ជះពុះអាហារឆ្ងាញ់ អីក្របក់ធុងឆ្កុះ អីឃុំត្រី អីមនុស្សបក់ក្រៀល អីធុងស្រូវបន្លែ អីស្វែងរកអ្វីៗ
អារ៉ាបល់ ប្រពន្ធខ្ញុំ ឆាកា ឆាដ អារ៉ាបល់ ប្រពន្ធខ្ញុំ ឆាកា ឆាដ
"""

GIFT_TEXT = """
# ผมมีของขวัญสำหรับตัวหน้าหีไห้พวกมึง จาก Sleepmode15 & Sky หวังว่ามึงจะทำควาย
https://media.discordapp.net/attachments/1104642491052994661/1112241841564295198/file.gif?ex=6781f8ef&is=6780a76f&hm=7a8f7faf9325d6b9e19d61c6c7ceadf841dfaf441e4bb9aa8ea3c230c2cea1a6&
"""

PROMOTE_TEXT = """
# ⚠《☣𝔇𝖆𝖗𝖐𝖓𝖊𝖘𝖘☣》⚠ | บริการบอทดิสคอร์ดยศราคาถูกมียิงเบอร์ฟรีและต่างๆอีกมากมาย
**- แอดมินบริการตลอด✅️
- บอทใช้งานง่าย รันตลอด24ชั่วโมงแต่หัวดิสรันตลอด12ชั่วโมง
- หากใช้ไม่เป็น หรืออยากสอบถามไรไห้ติดต่ิเรามาได้พร้อมตอบตลอดเวลา
- มีของฟรีและอย่างอื่นอีกเยอะแยะ**

https://discord.gg/NYH7QP7EZX

"""



WARNING_EPHEMERAL = "# กูไม่รับผิดชอบที่มึงทำนะมึงทำเอง ไอ่ควาย\n**อยากหาความรู้ฉลาดเข้าสมองและอยากรู้ว่าใครสร้าง คลิกที่ลิ้งเลยสัสืคลิกดิควาย**\n\nhttps://discord.gg/NYH7QP7EZX"



LAG = "🤔😇😳🙁🥵😗🤨😒😄😿😸😟😷🥵🙄😇🤢🤧😭🤑😶😊😏🤢😳🧐🙄🤧😑😷😅😇😐😹🤭😒🙁🤬😲🤒☹️😭😋😋😠🤩🤤😔😭💀☠️🥥🤣💢🥚✔️😩👤🤨🥶😅😮‍💨🍏🐠🦐🍐🍈🥝🤨🤖✔️🤑🌰🦐🫐😅🥶😔😭🥥😂💢🥚🦐🫐 🥭🤨😔🤣💢🥚🍏✖️🥥🤓😅🥭😔👤🥝🥶✔️🥲💢🐠🐠🥝🐠🦐🍏🫐🍐🍍🥭🍈🥝🌰🥚🍟🥖😮‍💨😅😰🥶🤨💢🥲🤑✖️✔️🥰😩🤖👤👍🤣😂🥥☠️🤓💀😭"



K_J = """ควายสัสจังไรอิขนหมอยดกกุจะไม่หยุดกุจะสร้างความรำคาญแปสมแท็กพวกมึงควายควยสัสจังไรขนหมอยดกแม่มึงตายพ่อมึงตายไอ้ชิงหมาเกิดมึงเกิดมาทำไมวะควายชิบหายสัสไอ้เหี้ยโง่ไอ้ชาติหมามาเกิดไอ้เหี้ย2ขาไอ้ควายไอ้หำไซส์34หี34@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone@everyone
"""



NSFW_IMAGES = [
    "https://api-cdn.rule34.xxx/images/2090/faca750621a0fa383d85dcf9a24b8b214209c302.gif",
    "https://api-cdn.rule34.xxx/images/1673/00758e80ccd868c658e41b03b94c29d0.jpeg",
    "https://api-cdn.rule34.xxx/images/2602/d535d9da2b0b23fce2429d17f7b6337d.png",
    "https://api-cdn.rule34.xxx/images/4611/07a18dffc3d59537e86ab55b214a54d7.jpeg",
    "https://api-cdn.rule34.xxx/images/1403/0551eec4b0a42e240fe7896728bb9807.jpeg",
    "https://api-cdn.rule34.xxx/images/1175/d7c5cccaca0b139875f9d9dd7da63f78.png",
    "https://api-cdn.rule34.xxx/images/2369/b580c0100ad26817e3f17472a81764a5.jpeg",
    "https://api-cdn.rule34.xxx/images/1974/531348a6d9d88a96ed8564cd1647d8bf.jpeg",
    "https://api-cdn.rule34.xxx/images/2038/8730aa96f0e3820a902206d41e488249.png",
    "https://api-cdn.rule34.xxx/images/1747/efe0ae93d490ccb373d2d77e6a18c7b6.png",
    "https://api-cdn.rule34.xxx/images/1350/8efd1a280d5dc98b5591de852cae9879.png",
    "https://api-cdn.rule34.xxx/images/7244/3c80f6afb64e72ea1b2092765495da48.png",
    "https://api-cdn.rule34.xxx/images/1735/5a63309f4d3ce95862e7cf159f160e7c.jpeg",
    "https://api-cdn.rule34.xxx/images/2861/617d8e5508fd033484e3d0514d9192c8.png",
    "https://api-cdn.rule34.xxx/images/4097/d365ad60eebfb031b02ec4d02f1901e999d08cab.png",
    "https://api-cdn.rule34.xxx/images/3968/304bdfceb5483fafedd0938b1d37451e.jpeg",
    "https://api-cdn.rule34.xxx/images/1835/7c6d2661d7d71ece31af506efc69ae18.png",
    "https://api-cdn.rule34.xxx/images/4118/99941186e137f7b375d9c3562f0fd4be.jpeg",
    "https://api-cdn.rule34.xxx/images/1375/ae31780729432267b778ed1fbc29badc.png",
    "https://api-cdn.rule34.xxx/images/5181/09c454e6985e85d21195bbb43d41ae8e.jpeg",
    "https://api-cdn.rule34.xxx/images/2104/42681bf7fbf3f1e4f0e68b18a100925e.png",
    "https://api-cdn.rule34.xxx/images/2484/908dd4cb318fc3b2eced8b3d9e12b24e.jpeg",
    "https://api-cdn.rule34.xxx/images/1657/d6babedf13803477afd6408e45f98f48.jpeg",
    "https://api-cdn.rule34.xxx/images/617/5d77b717109645a987dc9d4ad2181885.gif",
    "https://api-cdn.rule34.xxx/images/2538/22ac05e168f7c72df4e4c035719a9d51.png",
    "https://api-cdn.rule34.xxx/images/1680/a2711caeccf4bb55a50771732f28385b.png",
    "https://api-cdn.rule34.xxx/images/1441/551275328f598eabc89e5d90f3f0105d.jpeg",
    "https://api-cdn.rule34.xxx/images/559/da3eda46d5f8f744918b7e3d18227488.png",
    "https://api-cdn.rule34.xxx/images/2319/2d90d4722beea42832a2eeac61567a4d.jpeg",
    "https://api-cdn.rule34.xxx/images/3188/08dad60f315d4d67ccf4693e20498f23.jpeg",
    "https://api-cdn.rule34.xxx/images/2727/4e444c16bc89afd389988230b09fe0b8.jpeg",
    "https://api-cdn.rule34.xxx/images/4693/1d1c27261b09f406f6f088e019941fdf.jpeg",
    "https://api-cdn.rule34.xxx/images/603/98dc8499f1f50a0b58709721c8c66825.jpeg",
    "https://api-cdn.rule34.xxx/images/5548/e128ed8c7c7c9469e92ced35655db03d.jpeg",
]



THAI_MONTHS = [
    "มกราคม","กุมภาพันธ์","มีนาคม","เมษายน","พฤษภาคม","มิถุนายน",
    "กรกฎาคม","สิงหาคม","กันยายน","ตุลาคม","พฤศจิกายน","ธันวาคม"
]



MAX_SPAM_PER_COMMAND = 30
DEFAULT_SPAM_COUNT = 10


class DiscordApiManager:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def fetch_nsfw_image(self) -> str:
        url = "https://api.waifu.pics/nsfw/waifu"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("url", "❌ ไม่สามารถดึงรูปภาพได้")
                return f"❌ API ตอบสถานะ {resp.status}"
        except Exception as e:
            return f"❌ เกิดข้อผิดพลาด: {str(e)}"


class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)
        self.session: aiohttp.ClientSession | None = None
        self.api_manager: DiscordApiManager | None = None

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        self.api_manager = DiscordApiManager(self.session)

        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} slash command(s).")
        except Exception as e:
            print(f"Failed to sync slash commands: {e}")

    async def on_ready(self):
        print(f"Logged in as {self.user} ({self.user.id})")
        print("Bot is ready and listening for commands.")
        print("==============================")

    async def close(self):
        await super().close()
        if self.session:
            await self.session.close()

    async def send_warning(self, interaction: discord.Interaction):
        await interaction.response.send_message(WARNING_EPHEMERAL, ephemeral=True)

    async def fast_spam(self, interaction: discord.Interaction, message_func, count: int):
        for i in range(count):
            try:
                await message_func()
                await asyncio.sleep(0)
            except Exception as e:
                print(f"Error during spam (#{i+1}): {e}")

bot = MyBot()

async def check_user(interaction: discord.Interaction):
    uid = str(interaction.user.id)
    name = str(interaction.user)
    add_user(uid, name)
    if is_banned(uid):
        await interaction.response.send_message("❌ คุณถูกแบน ใช้คำสั่งไม่ได้ไอ่ควาย", ephemeral=True)
        return False
    return True

# ---------------- คำสั่งแบน/ปลดแบน ----------------
@bot.tree.command(name="userban", description="แบนและปลดแบนพวกมึงอย่าหาไช้")
@app_commands.describe(action="ban หรือ unban", user_id="ไอดีผู้ใช้")
async def userban(interaction: discord.Interaction, action: str, user_id: str):

    if str(interaction.user.id) != OWNER_ID:
        await interaction.response.send_message("สันหาไช้ระมึงก็บอกอยู่ไอ้ควาย", ephemeral=True)
        return

    if action.lower() == "ban":
        ban_user(user_id)
        await interaction.response.send_message(f"✅ แบนแล้ว {user_id}", ephemeral=True)

    elif action.lower() == "unban":
        unban_user(user_id)
        await interaction.response.send_message(f"✅ ปลดแบนแล้ว {user_id}", ephemeral=True)

    else:
        await interaction.response.send_message("❌ ใช้ ban หรือ unban เท่านั้น", ephemeral=True)



@bot.tree.command(name="พิมพ์", description="พิมพ์ข้อความส่งเองmessage")
@app_commands.describe(message="ข้อความ", count="จำนวนครั้ง (1-30, default 10)")
async def custom(interaction: discord.Interaction, message: str, count: Optional[int] = None):

    if not await check_user(interaction):
        return

    await bot.send_warning(interaction)
    spam_count = 10 if count is None else count

    if spam_count > MAX_SPAM_PER_COMMAND:
        await interaction.followup.send(f"# มันจำกัดเเค่{MAX_SPAM_PER_COMMAND}ข้อความต่อการเเสปมในเเต่ละครั้งไอ่ควาย ไอ่โง่ หัดดูบ้างดิ่ อ่านไอ่สัส ตามึงมีไว้ทำไมวะ ไว้ดูเเต่หีหรอมึง", ephemeral=True)
        return

    async def spam_content():
        await interaction.followup.send(message)

    await bot.fast_spam(interaction, spam_content, spam_count)



@bot.tree.command(name="ด่าดิสกระจอก", description="ด่ายาวๆ แบบควยๆ")
@app_commands.describe(count="จำนวนครั้งที่สแปม (1-30, ค่าเริ่มต้น 10)")
async def funk(interaction: discord.Interaction, count: Optional[int] = None):

    if not await check_user(interaction):
        return

    await bot.send_warning(interaction)
    spam_count = 10 if count is None else count

    if spam_count > MAX_SPAM_PER_COMMAND:
        await interaction.followup.send(f"# มันจำกัดเเค่{MAX_SPAM_PER_COMMAND}ข้อความต่อการเเสปมในเเต่ละครั้งไอ่ควาย ไอ่โง่ หัดดูบ้างดิ่ อ่านไอ่สัส ตามึงมีไว้ทำไมวะ ไว้ดูเเต่หีหรอมึง", ephemeral=True)
        return

    async def spam_content():
        await interaction.followup.send(FUNK_TEXT)

    await bot.fast_spam(interaction, spam_content, spam_count)



@bot.tree.command(name="แสปมบรรทัด", description="กูไม่รู้ว่าจะบอกไง")
@app_commands.describe(message="ข้อความ", repeat="จำนวนครั้งที่ขึ้นบรรทัดใหม่ (1-20)", count="จำนวนครั้งที่สแปม (1-30, default 10)")
async def fast_cmd(interaction: discord.Interaction, message: str, repeat: int, count: Optional[int] =  None):

    if not await check_user(interaction):
        return

    await bot.send_warning(interaction)

    repeat_count = max(1, min(repeat, 20))
    spam_count = 10 if count is None else count

    if spam_count > MAX_SPAM_PER_COMMAND:
        await interaction.followup.send(f"# มันจำกัดเเค่{MAX_SPAM_PER_COMMAND}ข้อความต่อการเเสปมในเเต่ละครั้งไอ่ควาย ไอ่โง่ หัดดูบ้างดิ่ อ่านไอ่สัส ตามึงมีไว้ทำไมวะ ไว้ดูเเต่หีหรอมึง", ephemeral=True)
        return

    full_message = "\n".join([message for _ in range(repeat_count)])

    async def spam_content():
        await interaction.followup.send(full_message)

    await bot.fast_spam(interaction, spam_content, spam_count)



@bot.tree.command(name="ภาษาอาหวัง", description="เเสปมจีน")
@app_commands.describe(count="จำนวนครั้งที่สแปม (1-30, ค่าเริ่มต้น 10)")
async def chinese_cmd(interaction: discord.Interaction, count: Optional[int] = None):

    if not await check_user(interaction):
        return

    await bot.send_warning(interaction)
    spam_count = 10 if count is None else count

    if spam_count > MAX_SPAM_PER_COMMAND:
        await interaction.followup.send(f"# มันจำกัดเเค่{MAX_SPAM_PER_COMMAND}ข้อความต่อการเเสปมในเเต่ละครั้งไอ่ควาย ไอ่โง่ หัดดูบ้างดิ่ อ่านไอ่สัส ตามึงมีไว้ทำไมวะ ไว้ดูเเต่หีหรอมึง", ephemeral=True)
        return

    async def spam_content():
        await interaction.followup.send(CHINESE_TEXT)

    await bot.fast_spam(interaction, spam_content, spam_count)



@bot.tree.command(name="เส้นหมอย", description="เเสปมด่าแบพวกแขมภาษาเส้นหมอย")
@app_commands.describe(count="จำนวนครั้งที่สแปม (1-30, ค่าเริ่มต้น 10)")
async def khmer_cmd(interaction: discord.Interaction, count: Optional[int] = None):

    if not await check_user(interaction):
        return

    await bot.send_warning(interaction)

    spam_count_total = 6
    user_count = count if count is not None else 10

    if user_count > MAX_SPAM_PER_COMMAND:
        await interaction.followup.send(f"# มันจำกัดเเค่{MAX_SPAM_PER_COMMAND}ข้อความต่อการเเสปมในเเต่ละครั้งไอ่ควาย ไอ่โง่ หัดดูบ้างดิ่ อ่านไอ่สัส ตามึงมีไว้ทำไมวะ ไว้ดูเเต่หีหรอมึง", ephemeral=True)
        return

    spam_times = user_count if user_count is not None else 10

    async def spam_content():
        await interaction.followup.send(KHMER_TEXT)

    await bot.fast_spam(interaction, spam_content, spam_times)


def format_thai_date(dt):
    dt = dt.astimezone(timezone.utc)
    day = dt.day
    month = THAI_MONTHS[dt.month - 1]
    year = dt.year + 543
    hour = dt.hour
    minute = dt.minute
    return f"{day} {month} {year} {hour:02d}:{minute:02d}"

@bot.tree.command(name="หาข้อมูลด้วยไอดีมั้ง", description="ดูเวลาสร้างรูปและอีกนิดนึง")
@app_commands.describe(user_id="ไอดีผู้ใช้ Discord")
async def userinfo(interaction: discord.Interaction, user_id: str):

    if not await check_user(interaction):
        return

    await interaction.response.defer(ephemeral=True)

    try:
        user = await bot.fetch_user(int(user_id))
    except:
        await interaction.followup.send("❌ หาไอดีนี้ไม่เจอไอ้ควาย", ephemeral=True)
        return

    is_bot = "🤖 บอท" if user.bot else "👤 คน"
    created_en = user.created_at.strftime("%d %B %Y • %H:%M UTC")
    created_th = format_thai_date(user.created_at)
    avatar_url = user.display_avatar.url

    embed = discord.Embed(
        title="📌 ข้อมูลผู้ใช้ Discord นี้",
        color=0xff0055
    )
    embed.add_field(name="ชื่อผู้ใช้", value=f"`{user}`", inline=False)
    embed.add_field(name="ชื่อที่แสดง", value=f"`{user.display_name}`", inline=False)
    embed.add_field(name="ไอดี", value=f"`{user.id}`", inline=False)
    embed.add_field(name="เป็นคนหรือบอท", value=is_bot, inline=False)
    embed.add_field(
        name="สร้างบัญชี",
        value=f"🇬🇧 {created_en}\n🇹🇭 {created_th}",
        inline=False
    )

    embed.set_thumbnail(url=avatar_url)
    embed.set_image(url=avatar_url)
    embed.set_footer(text="กดที่รูปเพื่อดูเต็มหากอยากได้รูปไห้กดรูปแล้วกดสามจุดกดบันทึกไม่ก็ดาวโหลด")

    await interaction.followup.send(embed=embed, ephemeral=True)



@bot.tree.command(name="gift", description="มีของขวัญมาเเจกไอ่หน้าหี")
@app_commands.describe(count="จำนวนครั้งที่สแปม (1-30, ค่าเริ่มต้น 10)")
async def gift_cmd(interaction: discord.Interaction, count: Optional[int] = None):

    if not await check_user(interaction):
        return

    await bot.send_warning(interaction)

    spam_times = count if count is not None else 10

    if spam_times > MAX_SPAM_PER_COMMAND:
        await interaction.followup.send(f"# มันจำกัดเเค่{MAX_SPAM_PER_COMMAND}ข้อความต่อการเเสปมในแต่ละครั้งไอ่ควาย ไอ่โง่ หัดดูบ้างดิ่ อ่านไอ่สัส ตามึงมีไว้ทำไมวะ ไว้ดูเเต่หีหรอมึง", ephemeral=True)
        return

    async def send_gift_msg():
        await interaction.followup.send(GIFT_TEXT)

    await bot.fast_spam(interaction, send_gift_msg, spam_times)



@bot.tree.command(name="spam18", description="สุ่มส่งภาพ18อาจมีน้อยหน่อยกุไม่ค่อยมีรูป")
@app_commands.describe(count="จำนวนครั้งที่สแปม (1-30, ค่าเริ่มต้น 10)")
async def spam18(interaction: discord.Interaction, count: Optional[int] = None):

    if not await check_user(interaction):
        return

    await bot.send_warning(interaction)

    spam_count = 10 if count is None else count

    if spam_count < 1 or spam_count > MAX_SPAM_PER_COMMAND:
        await interaction.followup.send(f"มันจำกัดเเค่{MAX_SPAM_PER_COMMAND}ข้อความต่อการเเสปมในเเต่ละครั้งไอ่ควาย ไอ่โง่ หัดดูบ้างดิ่ อ่านไอ่สัส ตามึงมีไว้ทำไมวะ ไว้ดูเเต่หีหรอมึง", ephemeral=True)
        return

    async def send_random_image():
        img_url = random.choice(NSFW_IMAGES)
        await interaction.followup.send(img_url)

    await bot.fast_spam(interaction, send_random_image, spam_count)



@bot.tree.command(name="promote-ดิสกุ", description="โปรโมทดิสกุและสิ่งที่กุทำ")
@app_commands.describe(count="จำนวนครั้งที่สแปม (1-30, ค่าเริ่มต้น 10)")
async def promote(interaction: discord.Interaction, count: Optional[int] = None):

    if not await check_user(interaction):
        return

    await bot.send_warning(interaction)
    spam_count = 10 if count is None else count

    if spam_count > MAX_SPAM_PER_COMMAND:
        await interaction.followup.send(f"# มันจำกัดเเค่{MAX_SPAM_PER_COMMAND}ข้อความต่อการเเสปมในเเต่ละครั้งไอ่ควาย ไอ่โง่ หัดดูบ้างดิ่ อ่านไอ่สัส ตามึงมีไว้ทำไมวะ ไว้ดูเเต่หีหรอมึง", ephemeral=True)
        return

    async def send_promote():
        await interaction.followup.send(PROMOTE_TEXT)

    await bot.fast_spam(interaction, send_promote, spam_count)



@bot.tree.command(name="lag", description="สแปมอิโมจิยาวๆ เพื่อเหี้ยอะไรก็ไม่รู้")
@app_commands.describe(count="จำนวนครั้งที่สแปม (1-30, ค่าเริ่มต้น 10)")
async def lag_cmd(interaction: discord.Interaction, count: Optional[int] = None):

    if not await check_user(interaction):
        return

    await bot.send_warning(interaction)

    spam_count = 10 if count is None else count

    if spam_count > MAX_SPAM_PER_COMMAND:
        await interaction.followup.send(f"# มันจำกัดเเค่{MAX_SPAM_PER_COMMAND}ข้อความต่อการเเสปมในเเต่ละครั้งไอ่ควาย ไอ่โง่ หัดดูบ้างดิ่ อ่านไอ่สัส ตามึงมีไว้ทำไมวะ ไว้ดูเเต่หีหรอมึง", ephemeral=True)
        return

    async def send_lag():
        await interaction.followup.send(LAG)

    await bot.fast_spam(interaction, send_lag, spam_count)



@bot.tree.command(name="แสปมแท็ก", description="สแปมแท็กรัวๆไห้ดิสนั้นแม่งรำคาญจนออก")
@app_commands.describe(count="จำนวนครั้งที่สแปม (1-30, ค่าเริ่มต้น 10)")
async def lag_cmd(interaction: discord.Interaction, count: Optional[int] = None):

    if not await check_user(interaction):
        return

    await bot.send_warning(interaction)

    spam_count = 10 if count is None else count

    if spam_count > MAX_SPAM_PER_COMMAND:
        await interaction.followup.send(f"# มันจำกัดเเค่{MAX_SPAM_PER_COMMAND}ข้อความต่อการเเสปมในเเต่ละครั้งไอ่ควาย ไอ่โง่ หัดดูบ้างดิ่ อ่านไอ่สัส ตามึงมีไว้ทำไมวะ ไว้ดูเเต่หีหรอมึง", ephemeral=True)
        return

    async def send_lag():
        await interaction.followup.send(K_J)

    await bot.fast_spam(interaction, send_lag, spam_count)



@bot.tree.command(name="spam-webhook", description="Spam Webhook กากๆ")
@app_commands.describe(
    webhook_url="ลิงก์ Webhook ที่ต้องการสแปม",
    message="ข้อความที่ต้องการสแปม",
    count="จำนวนครั้งที่สแปม (1-25, ค่าเริ่มต้น 5)",
    name="เปลี่ยนชื่อ Webhook (ไม่บังคับ)",
    avatar_url="เปลี่ยนรูปโปรไฟล์ Webhook (ไม่บังคับ)",
    delete_webhook="ลบ Webhook หลังสแปมเสร็จ (ไม่บังคับ)"
)
async def spam_webhook(
    interaction: discord.Interaction,
    webhook_url: str,
    message: str,
    count: Optional[int] = None,
    name: Optional[str] = None,
    avatar_url: Optional[str] = None,
    delete_webhook: Optional[bool] = False
):
    await bot.send_warning(interaction)

    spam_count = 5 if count is None else count

    if spam_count > MAX_SPAM_PER_COMMAND:
        await interaction.followup.send(f"# มันจำกัดเเค่{MAX_SPAM_PER_COMMAND}ข้อความต่อการเเสปมในเเต่ละครั้งไอ่ควาย ไอ่โง่ หัดดูบ้างดิ่ อ่านไอ่สัส ตามึงมีไว้ทำไมวะ ไว้ดูเเต่หีหรอมึง", ephemeral=True)
        return

    if not webhook_url.startswith("https://discord.com/api/webhooks/"):
        await interaction.followup.send("❌ ลิงก์ Webhook ไม่ถูกต้อง", ephemeral=True)
        return

    try:
        parts = webhook_url.split("/")
        webhook_id = parts[-2]
        webhook_token = parts[-1]
    except IndexError:
        await interaction.followup.send("❌ รูปแบบ Webhook URL ผิดพลาด", ephemeral=True)
        return

    async def send_to_webhook():
        payload = {
            "content": message,
            "username": name,
            "avatar_url": avatar_url
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        url = f"https://discord.com/api/webhooks/{webhook_id}/{webhook_token}"
        headers = {"Content-Type": "application/json"}

        try:
            async with bot.session.post(url, json=payload, headers=headers) as resp:
                if resp.status == 204:
                    pass
                else:
                    print(f"⚠️ Webhook ส่งไม่สำเร็จ: {resp.status}")
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการส่ง Webhook: {e}")

    await bot.fast_spam(interaction, send_to_webhook, spam_count)

    if delete_webhook:
        try:
            delete_url = f"https://discord.com/api/webhooks/{webhook_id}/{webhook_token}"
            async with bot.session.delete(delete_url) as resp:
                if resp.status == 204:
                    await interaction.followup.send("✅ Webhook ถูกลบเรียบร้อยแล้ว", ephemeral=True)
                else:
                    await interaction.followup.send(f"❌ ไม่สามารถลบ Webhook ได้ (สถานะ: {resp.status})", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ เกิดข้อผิดพลาดในการลบ Webhook: {e}", ephemeral=True)

if __name__ == "__main__":
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ กรุณาใส่ Token บอทของคุณในตัวแปร BOT_TOKEN!")
    else:
        try:
            bot.run(BOT_TOKEN)
        except discord.LoginFailure:
            print("❌ Token บอทไม่ถูกต้อง!")
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการรันบอท: {e}")
