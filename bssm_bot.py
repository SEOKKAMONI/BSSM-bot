from ast import Subscript
from pydoc import describe
from this import d
import discord
import requests
from bs4 import BeautifulSoup
import datetime
import json

days =['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

day_number = datetime.datetime.today().weekday()

client = discord.Client()

token = '토큰'

header = {'User-agent' : 'Mozila/2.0'}

# 부산소프트웨어마이스터고 bssm.kro.kr
response = requests.get("https://bssm.kro.kr/meal" , header)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

meal_times = soup.select('.meal_time')
meal_menus = soup.select('.meal_menu')
check_menu = soup.select_one('.meal_menu') # 메뉴가 있는지 없는지 체크하기위해 공휴일 일수도 있으니깐

# 부산소프트웨어마이스터고 각종대회정보 
response1 = requests.get("https://school.busanedu.net/bssm-h/na/ntt/selectNttList.do?mi=1040046&bbsId=5156419",verify=False)
html1 = response1.text
soup1 = BeautifulSoup(html1, 'html.parser')

competitions = soup1.select('.ta_l > a')

# 네이버 부산소프트웨어마이스터고 급식 식단표 
response2 = requests.get("https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EB%B6%80%EC%82%B0%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4%EB%A7%88%EC%9D%B4%EC%8A%A4%ED%84%B0%EA%B3%A0%EB%93%B1%ED%95%99%EA%B5%90" , header)
html2 = response2.text
soup2 = BeautifulSoup(html2, 'html.parser')

day_checks = soup2.select(".dday_txt")
items = soup2.select(".item_list")
dates = soup2.select(".cm_date")

# 날짜
y_m_d = datetime.datetime.today().strftime('%Y년 %m월 %d일 {}'.format(days[day_number]))

@client.event
async def on_ready():
    print('시스템 가동 준비완료')

@client.event
async def on_message(message):
    if message.content.startswith('!도움말'):
        embed = discord.Embed(title="🟢 도움말 🟢", description="봇 사용법을 알려줍니다 !!", color=0x008000)
        embed.add_field(name="!급식표", value="아침, 점심, 저녁으로 급식정보를 알려줍니다.", inline=False)
        embed.add_field(name="!시간표 X학년X반", value="ex) !시간표 1학년 2반\n 해당 시간표가 보여집니다.", inline=False) # https://github.com/SEOKKAMONI       
        embed.set_footer(text="Bot Made by. 김석진 #9335", icon_url="https://search.pstatic.net/common/?src=http%3A%2F%2Fcafefiles.naver.net%2FMjAyMDAzMzBfMTM1%2FMDAxNTg1NDk1NDg0MzQ0.3gAtZonNGC6GDOgJ2HWFVE5haE2zZ1A9mCmCmUA8UUgg.IaR5OGJcNDv4hYK_UR4EKzbj_zmN_mpCK20atEmgUDUg.JPEG%2F97409BAF-76F7-48C9-97F8-8F70804E6FD6.jpeg&type=sc960_832")
        embed.add_field(name="!대회정보", value="부산소프트웨어마이스터고 사이트 각종 대회 정보에서 가져온\n 데이터로 대회정보를 알려줍니다.", inline=False)
        await message.channel.send(embed=embed)
    elif message.content.startswith('!급식표'):
        if(days[day_number] != '토요일' and days[day_number] != '일요일' and check_menu != "급식이 없습니다."): # 토요일이나 일요일 혹은 급식이 없으면 공휴일로 판별함
            embed = discord.Embed(title=y_m_d, description="🍱 부산소마고 급식 정보 🍱", color=0x008000)
            for day_check,item,date in zip(day_checks,items,dates):
                bssm_date = date.text.replace("TODAY", " ") # TODAY 를 공백으로 변경
                bssm_item = item.text.replace(" ", "\n") # 공백을 한줄 바꿈으로 변경하므로 일렬로 정렬
                embed.add_field(name=bssm_date, value=bssm_item, inline=True)
        else: # 휴일 혹은 주말일때는 급식이 없습니다 출력
            embed = discord.Embed(title=y_m_d, description="해당하는 날짜에는 급식이 없습니다", color=0x008000)
        embed.set_footer(text="Bot Made by. 김석진 #9335", icon_url="https://search.pstatic.net/common/?src=http%3A%2F%2Fcafefiles.naver.net%2FMjAyMDAzMzBfMTM1%2FMDAxNTg1NDk1NDg0MzQ0.3gAtZonNGC6GDOgJ2HWFVE5haE2zZ1A9mCmCmUA8UUgg.IaR5OGJcNDv4hYK_UR4EKzbj_zmN_mpCK20atEmgUDUg.JPEG%2F97409BAF-76F7-48C9-97F8-8F70804E6FD6.jpeg&type=sc960_832")
        await message.channel.send(embed=embed)

    elif message.content.startswith('!대회정보'):
        count = 0
        embed = discord.Embed(title="🔎 각종 대회 정보 🔎", color=0x008000) # 부소마 사이트에서 크롤링함
        for competition in competitions:
            if(count != 5):
                title = competition.text.strip()
                url = competition.attrs['href']
                embed.add_field(name=f"{title}", value=f"링크 바로가기: https://school.busanedu.net/{url}", inline=False)
                count += 1
        embed.set_footer(text="Bot Made by. 김석진 #9335", icon_url="https://search.pstatic.net/common/?src=http%3A%2F%2Fcafefiles.naver.net%2FMjAyMDAzMzBfMTM1%2FMDAxNTg1NDk1NDg0MzQ0.3gAtZonNGC6GDOgJ2HWFVE5haE2zZ1A9mCmCmUA8UUgg.IaR5OGJcNDv4hYK_UR4EKzbj_zmN_mpCK20atEmgUDUg.JPEG%2F97409BAF-76F7-48C9-97F8-8F70804E6FD6.jpeg&type=sc960_832")
        await message.channel.send(embed=embed)
    elif message.content.startswith("!시간표"):
        class_name = message.content.replace("!시간표 ", "")
        search = message.content.replace(" ", "")
        if(class_name == "1학년1반"):
            embed = discord.Embed(title="1학년 1반 시간표", color=0x008000)
            embed.set_image(url = "https://postfiles.pstatic.net/MjAyMjA1MjlfMjQx/MDAxNjUzODI2MjcwMTQz.Dr577gfcujaJllsR61zwGsONzJU4bNyCLSlTy6B-Ux4g.yQAvUW9ID49XdsaA0ntlefDBp91Z-7IzVM275MEXn4sg.JPEG.sj060706/1%ED%95%99%EB%85%841%EB%B0%98.jpg?type=w773")
            embed.set_footer(text="Bot Made by. 김석진 #9335", icon_url="https://search.pstatic.net/common/?src=http%3A%2F%2Fcafefiles.naver.net%2FMjAyMDAzMzBfMTM1%2FMDAxNTg1NDk1NDg0MzQ0.3gAtZonNGC6GDOgJ2HWFVE5haE2zZ1A9mCmCmUA8UUgg.IaR5OGJcNDv4hYK_UR4EKzbj_zmN_mpCK20atEmgUDUg.JPEG%2F97409BAF-76F7-48C9-97F8-8F70804E6FD6.jpeg&type=sc960_832")
            await message.channel.send(embed=embed)
        elif(class_name == "1학년2반"):
            embed = discord.Embed(title="1학년 2반 시간표", color=0x008000) 
            embed.set_image(url = "https://postfiles.pstatic.net/MjAyMjA1MjlfMjAy/MDAxNjUzODI2MjczMTg5.u8hCRvshj72nLOUx1zhDxsMxJJPHHpX18VkgtrYNU4gg.tWsH66Bovn5zxo61B4DWBxqHqSelUzXBJV8jryFgrtwg.JPEG.sj060706/1%ED%95%99%EB%85%842%EB%B0%98.jpg?type=w773")
            embed.set_footer(text="Bot Made by. 김석진 #9335", icon_url="https://search.pstatic.net/common/?src=http%3A%2F%2Fcafefiles.naver.net%2FMjAyMDAzMzBfMTM1%2FMDAxNTg1NDk1NDg0MzQ0.3gAtZonNGC6GDOgJ2HWFVE5haE2zZ1A9mCmCmUA8UUgg.IaR5OGJcNDv4hYK_UR4EKzbj_zmN_mpCK20atEmgUDUg.JPEG%2F97409BAF-76F7-48C9-97F8-8F70804E6FD6.jpeg&type=sc960_832")
            await message.channel.send(embed=embed)
        elif(class_name == "1학년3반"):
            embed = discord.Embed(title="1학년 3반 시간표", color=0x008000)
            embed.set_image(url = "https://postfiles.pstatic.net/MjAyMjA1MjlfNCAg/MDAxNjUzODI2Mjc1MjA0.jGUAIbQ7E7IwsGVMt-G7R7uhrPTVLUm_dy6ZVqHu7ggg.bpqQTB3gGJvJlxgU6To-OOr5uQCycNJXmvw57J5PN5wg.JPEG.sj060706/1%ED%95%99%EB%85%843%EB%B0%98.jpg?type=w773")
            embed.set_footer(text="Bot Made by. 김석진 #9335", icon_url="https://search.pstatic.net/common/?src=http%3A%2F%2Fcafefiles.naver.net%2FMjAyMDAzMzBfMTM1%2FMDAxNTg1NDk1NDg0MzQ0.3gAtZonNGC6GDOgJ2HWFVE5haE2zZ1A9mCmCmUA8UUgg.IaR5OGJcNDv4hYK_UR4EKzbj_zmN_mpCK20atEmgUDUg.JPEG%2F97409BAF-76F7-48C9-97F8-8F70804E6FD6.jpeg&type=sc960_832")
            await message.channel.send(embed=embed)
        elif(class_name == "1학년4반"):
            embed = discord.Embed(title="1학년 4반 시간표", color=0x008000)
            embed.set_image(url = "https://postfiles.pstatic.net/MjAyMjA1MjlfMjM5/MDAxNjUzODI2Mjc2OTg5.fxZdsZmhlUNv0cRqFtrgZ9ewFXhuG4BcYNWiGD4CuaQg.piVcyu1hkxQF_gVjiYW9ZiaN1h5ah-Kr4OUXkhP8Ij8g.JPEG.sj060706/1%ED%95%99%EB%85%844%EB%B0%98.jpg?type=w773")
            embed.set_footer(text="Bot Made by. 김석진 #9335", icon_url="https://search.pstatic.net/common/?src=http%3A%2F%2Fcafefiles.naver.net%2FMjAyMDAzMzBfMTM1%2FMDAxNTg1NDk1NDg0MzQ0.3gAtZonNGC6GDOgJ2HWFVE5haE2zZ1A9mCmCmUA8UUgg.IaR5OGJcNDv4hYK_UR4EKzbj_zmN_mpCK20atEmgUDUg.JPEG%2F97409BAF-76F7-48C9-97F8-8F70804E6FD6.jpeg&type=sc960_832")
            await message.channel.send(embed=embed)
client.run(token)