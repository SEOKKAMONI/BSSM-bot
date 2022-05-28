from ast import Subscript
from pydoc import describe
from this import d
import discord
import requests
from bs4 import BeautifulSoup
import datetime

days =['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

day_number = datetime.datetime.today().weekday()

client = discord.Client()

token = '토큰'

header = {'User-agent' : 'Mozila/2.0'}
response = requests.get("https://bssm.kro.kr/meal" , header)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
meal_times = soup.select('.meal_time')
meal_menus = soup.select('.meal_menu')
check_menu = soup.select_one('.meal_menu') # 메뉴가 있는지 없는지 체크하기위해 공휴일 일수도 있으니깐

response1 = requests.get("https://school.busanedu.net/bssm-h/na/ntt/selectNttList.do?mi=1040046&bbsId=5156419",verify=False); # 크롤링하고싶은 사이트 링크 작성
html1 = response1.text
soup1 = BeautifulSoup(html1, 'html.parser')
competitions = soup1.select('.ta_l > a')

y_m_d = datetime.datetime.today().strftime('%Y년 %m월 %d일 {}'.format(days[day_number]))

@client.event
async def on_ready():
    print('시스템 가동 준비완료')

@client.event
async def on_message(message):
    if message.content.startswith('!급식표'):
        if(days[day_number] != '토요일' and days[day_number] != '일요일' and check_menu != "급식이 없습니다."): # 그게 아니라면 정상적으로 급식 출력
            embed = discord.Embed(title=y_m_d, description="🍱 부산소마고 급식 정보 🍱", color=0x008000)
            for meal_time,meal_menu in zip(meal_times,meal_menus):
                menu = meal_menu.text
                time = meal_time.text
                embed.add_field(name=time, value=menu, inline=True)
        else: # 휴일 혹은 주말일때는 급식이 없습니다 출력
            embed = discord.Embed(title=y_m_d, description="해당하는 날짜에는 급식이 없습니다", color=0x008000)
        embed.set_footer(text="Bot Made by. 김석진 #9335", icon_url="https://search.pstatic.net/common/?src=http%3A%2F%2Fcafefiles.naver.net%2FMjAyMDAzMzBfMTM1%2FMDAxNTg1NDk1NDg0MzQ0.3gAtZonNGC6GDOgJ2HWFVE5haE2zZ1A9mCmCmUA8UUgg.IaR5OGJcNDv4hYK_UR4EKzbj_zmN_mpCK20atEmgUDUg.JPEG%2F97409BAF-76F7-48C9-97F8-8F70804E6FD6.jpeg&type=sc960_832")
        await message.channel.send(embed=embed)

    elif message.content.startswith('!대회정보'):
        count = 0
        embed = discord.Embed(title="🔎 각종 대회 정보 🔎", color=0x008000)
        for competition in competitions:
            if(count != 5):
                title = competition.text.strip()
                url = competition.attrs['href']
                embed.add_field(name=f"{title}", value=f"링크 바로가기: https://school.busanedu.net/{url}", inline=False)
                count += 1
        embed.set_footer(text="Bot Made by. 김석진 #9335", icon_url="https://search.pstatic.net/common/?src=http%3A%2F%2Fcafefiles.naver.net%2FMjAyMDAzMzBfMTM1%2FMDAxNTg1NDk1NDg0MzQ0.3gAtZonNGC6GDOgJ2HWFVE5haE2zZ1A9mCmCmUA8UUgg.IaR5OGJcNDv4hYK_UR4EKzbj_zmN_mpCK20atEmgUDUg.JPEG%2F97409BAF-76F7-48C9-97F8-8F70804E6FD6.jpeg&type=sc960_832")
        await message.channel.send(embed=embed)

client.run(token)