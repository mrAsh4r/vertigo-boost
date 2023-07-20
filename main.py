import os
import json
import requests
import time
import shutil
import re
import pyautogui as pg

from csgoFriendCode import FriendCode

from steam_totp import generate_twofactor_code_for_time



class account:
    def get2FA(self):
        a = int(time.time())
        beforeUpd = 30 - a % 30 #time in seconds when update come
        
        if beforeUpd < 2:
            time.sleep(beforeUpd+0.5)
            a = a + beforeUpd + 1

        code = generate_twofactor_code_for_time(self.secret, a)
        
        return code
    
    def __init__(self, login, password):
        self.login = login
        self.password = password
        
        try:
            steamid = maFileInfo[login][0]
            secret = maFileInfo[login][1]
        except KeyError:
            print(f"Нету файла с shared_secret для аккаунта {login} :(")
            return
        
        self.secret = secret
        self.steamID = steamid

def getSharedSecretsAndSteamID():
    profiles = {}
    
    for i in os.scandir('maFiles'):
        if (i.name[-7:] == ".maFile"):
            a = open(f"maFiles/{i.name}", "r").read()
            a = json.loads(a)
            profiles[a["account_name"]] = [a["Session"]["SteamID"], a["shared_secret"]]
    return profiles
    
maFileInfo = getSharedSecretsAndSteamID()

def getAccounts():
    accs = {}
    s = open("steam.txt", "r").read().split("\n")
    
    for i in s:
        a = i.split(" ")
        accs[a[0]] = account(a[0], a[1])
    
    return accs

accounts = getAccounts()


class folderHelper:
    
    path = "F:/steam/userdata/"
    __folder_constant = 76561197960265728
    
    #get folder id by steamid
    def __getFolderID(steamID) -> int:
        return steamID - folderHelper.__folder_constant
    
    def __checkFolderExist(folderID) -> bool:
        return os.path.isdir(f"{folderHelper.path}{folderID}")
    
    def __deleteUserdataFolder(folderID) -> None:
        os.system(f'rmdir "{folderHelper.path}{folderID}" /s /q')
        
    def __copyUserdataFolder(folderID) -> None:
        src = 'USERDATA'
        dest = f"{folderHelper.path}{folderID}"
        shutil.copytree(src, dest) 
    
    def __createLocalConfig(folderID, options) -> None:
        config = '''
"UserLocalConfigStore"
{
	"Software"
	{
		"Valve"
		{
			"Steam"
			{
				"apps"
				{
					"7"
					{
						"cloud"
						{
							"last_sync_state"		"synchronized"
						}
					}
					"760"
					{
						"cloud"
						{
							"quota_bytes"		"20000000000"
							"quota_files"		"50000"
							"used_bytes"		"0"
							"used_files"		"0"
						}
					}
					"2371090"
					{
						"cloud"
						{
							"last_sync_state"		"synchronized"
						}
					}
					"730"
					{
						"cloud"
						{
							"last_sync_state"		"synchronized"
						}
						"LaunchOptions"		"OPTIONS"
					}
				}
				"LastPlayedTimesSyncTime"		"10"
			}
		}
	}
    "LibraryLowPerfMode"		"1"
	"StartupState.Friends"		"0"
	"LibraryDisplaySize"		"1"
	"LibraryDisableCommunityContent"		"1"
}        
'''
        
        config = config.replace("OPTIONS", options)
        file = open(f"{folderHelper.path}{folderID}/config/localconfig.vdf", "w")
        file.write(config)
        file.close()
    
    def setLaunchOptions(steamID: int, options: str):
        
        folderID = folderHelper.__getFolderID(steamID)
        
        if (folderHelper.__checkFolderExist(folderID)):
            folderHelper.__deleteUserdataFolder(folderID)
        folderHelper.__copyUserdataFolder(folderID)
        folderHelper.__createLocalConfig(folderID, options)


# Писалось 2 часа выкинулось за 30 секунд
# class steamHelper:
    # def _getRefreshToken(a: account) -> str:
        # a = open(f"maFiles/{a.steamID}.maFile", "r").read()
        # return json.loads(a)["Session"]["RefreshToken"]
    
    
    # def _getLoginSecure(steamID, refreshToken: str):
        # try:
            # return str(steamID) + "%7C%7C" + requests.post(f"https://api.steampowered.com/IAuthenticationService/GenerateAccessTokenForApp/v1/", data={"steamid": steamID, "refresh_token": refreshToken}).json()["response"]["access_token"]
        # except:
            # raise Exception("Не верный RefreshToken :(")
        
    # def _getSessionID(steamID, LoginSecure: str):
        # c = {
            # "steamLoginSecure": LoginSecure
        # }
        
        # try:
            # return re.search(r'g_sessionID = "(.*)";', requests.get(f"https://steamcommunity.com/profiles/{steamID}/home", cookies=c).text).group(1)
        # except:
            # raise Exception("Ошибка при получении sessionID, очень странно... Возможно сменили js переменную :/")
    
    
    # that can send and accept friend requests
    # def addFriend(a: account, friendSteamID):
        # RefreshToken = steamHelper._getRefreshToken(a)
        # LoginSecure = steamHelper._getLoginSecure(a.steamID, RefreshToken)
        # SessionID = steamHelper._getSessionID(a.steamID, LoginSecure)
        
        # data = {
            # "sessionID": SessionID,
            # "steamid": friendSteamID,
            # "accept_invite": 0
        # }
        
        # c = {
            # "steamLoginSecure": LoginSecure,
            # "sessionid": SessionID
        # }
        
        # print(requests.post("https://steamcommunity.com/actions/AddFriendAjax", data=data, cookies=c).text)
        
        
        


class guiWorker:    
    
    def __auth(a: account):
        
        #click on login
        pg.click(666, 460)
        time.sleep(0.3)
        pg.write(a.login)
        
        
        #click on password
        pg.click(666, 535)
        time.sleep(0.3)
        pg.write(a.password)
        
        
        #click on submit button
        pg.click(830, 630)
        
        
        #write 2FA
        time.sleep(3)
        pg.write(a.get2FA())
        
        
        #close steam
        # time.sleep(13)
        # pg.click(414, 1058, button='right')
        # time.sleep(1)
        # pg.click(414, 1017)
        
        #roll up all wins to clear for next
        time.sleep(10)
        # pg.hotkey('win', 'd')
        
        
        
        
    
    def launchCSGO(self, options = ""):
        folderHelper.setLaunchOptions(self.acc.steamID, options)
        coords = re.search(r"-x (\d*) -y (\d*)", options)
        if (len(coords.groups()) == 2):
            self.x = int(coords.group(1))
            self.y = int(coords.group(2))
        # os.system("cmd /c start steam://rungameid/730")
        os.system("cmd /c start F:/steam/steam.exe -applaunch 730 -noverifyfiles -nofriendsui -no-browser")
        time.sleep(3)
        
        while (pg.screenshot(region=(624,651,1,1)).getcolors()[0][1] != (25, 26, 30)):
            print("waiting...")
            time.sleep(2)
            
        time.sleep(2)
        guiWorker.__auth(self.acc)
        
    
    def __init__(self, a: account):
        self.acc = a
        self.x = 0
        self.y = 0



class csgoParty:

    def __init__(self):
        self.members = {}
        self.leader = ""
    
    def __len__(self):
        return len(self.members)
    
    
    def _getRole(self, m: str):
        if (m == self.leader):
            return "leader"
        return "member"
    
    def __repr__(self):
        p = "Ur's party:\n"
        
        for i in self.members:
            p += f"{i} - {self._getRole(i)}\n"
        
        for i in range(5 - len(self)):
            p += "<Empty slot>\n"
        
        p += f"\nКоличество участников: {len(self)}/5\n"
        return p
    
    def _partyIsReady(self) -> bool:
        return (len(self) == 5) and (self.leader != "")
    
    
    def addMember(self, gui: guiWorker):
        if len(self.members) >= 5:
            raise Exception("Брат в лоби может быть только 5 челов...")
            
        self.members[gui.acc.login] = gui
    
    def _inviteMember(self, member: str):
        pg.moveTo(self.members[self.leader].x + 391, self.members[self.leader].y + 96)
        time.sleep(2)
        pg.click()
        time.sleep(2)
        pg.click(self.members[self.leader].x + 310, self.members[self.leader].y + 117)
        time.sleep(2)
        pg.write(FriendCode.encode(self.members[member].acc.steamID))
        time.sleep(2)
        pg.rightClick(self.members[self.leader].x + 164, self.members[self.leader].y + 176)
        time.sleep(2)
        pg.click(self.members[self.leader].x + 302, self.members[self.leader].y + 167)
        print("закрываем окно")
        time.sleep(3)
        pg.click(self.members[self.leader].x + 247, self.members[self.leader].y + 204)
    
    def _inviteAllMembers(self):
        for i in self.members:
            if (self._getRole(i) == "member"):
                self._inviteMember(i)
    
    def _acceptAllInvites():
        for i in self.members:
            
            if (self._getRole(i) != "member"):
                continue
            
            # self.members[i]
            
    
    #member - login steam
    def setLeader(self, member: str):
        self.leader = member
        
    def completeParty(self):
        # if (not self._partyIsReady()):
            # raise Exception("Пати не готово к запуску!")
        
        print("Ну ща буду приглашать хуле")
        self._inviteAllMembers()
        # self._acceptAllInvites()
        

        
def main():
    os.system("mode con:cols=80 lines=22")
    
    party = csgoParty()
    r = 0
    c = 0
    
    for i in accounts:
        a = accounts[i]
        gui = guiWorker(a)
        x = 400 * c
        y = 3 + 300 * r
        c+=1
        if (c == 4):
            c=0
            r+=1
        # gui.launchCSGO(f"-nojoy -nohltv -no-browser -nosound -low -novid -window -w 400 -h 300 -x {x} -y {y} -heapsize 1048576")
        gui.launchCSGO(f"-nojoy -nohltv -no-browser -nosound -low -novid -window -w 400 -h 300 -x {x} -y {y}")
        party.addMember(gui)
    
    print(party)
    # party.setLeader(input("Who will be leader? Input name: "))
    party.setLeader(list(party.members.keys())[0])
    print("-"*80)
    print(f"Leader is: {list(party.members.keys())[0]}")
    print("-"*80)
    print(party)
    
    input("Собираем пати?")
    party.completeParty()
    print("Press any key to kill all processes...")
    input()
    os.system("taskkill /f /im csgo.exe")
    time.sleep(2)
    os.system("taskkill /f /im steam.exe")
    

main()