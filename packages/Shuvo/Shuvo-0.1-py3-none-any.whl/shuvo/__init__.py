import os,sys
def shuvo():
    os.system("clear")
    os.system("cls")
    print("""\033[1;32m  
╔═════════════════════════════════════════════════╗\033[1;31m
║           WELCOME TO MAHDI SHORTCUT             ║\033[1;33m
║═════════════════════════════════════════════════║\033[1;33m                     
║\033[0;37m##     ##    ###    ##     ## ########  ####     ║
║\033[1;92m###   ###   ## ##   ##     ## ##     ##  ##      ║
║\033[1;93m#### ####  ##   ##  ##     ## ##     ##  ##      ║
║\033[1;91m## ### ## ##     ## ######### ##     ##  ##      ║
║\033[1;92m##     ## ######### ##     ## ##     ##  ##      ║
║\033[1;93m##     ## ##     ## ##     ## ##     ##  ##      ║
║\033[1;33m##     ## ##     ## ##     ## ########  ####     ║ 
║                                    \033[1;33mVERSION 4.2  ║
║╭──────────────\033[1;91m[POWERED BY MAHDI HASAN ]\033[1;33m─────────║
│ ╭──────────────────────────────────────────────╮│
│ │ [A] AUTHOR   :\033[0;37mMAHDI HASAN SHUVO              ││
│ │ \033[1;32m[F] FACEBOOK :m.me/bk4human                  ││
│ │ \033[1;32m[G]GITHUB    : SHUVO-BBHH                    ││ 
│ │ \033[1;37m[W] WHATSAPP : 01616406924                   ││
│ ╰─\033[1;33m─────────────────────────────────────────────╯│
╰\033[1;33m─────────────────────────────────────────────────╯\033[1;32m""")
    print('\033[1;97m====================================================') 
    print('        \x1b[97m\033[37;41m[ WELL COME TO MAHDI SHOTCUT  ]\033[0;m')
    print('\033[1;97m====================================================') 
    print("\033[1;97m[01] \033[1;92mRANDOM TOOLS [paid]         \033[1;96m")
    print("\033[1;97m[02] \033[1;92mRANDOM CLOINIG TOOL [FREE]")
    print("\033[1;97m[03] \033[1;92mFACEBOOK  ")
    print("\033[1;97m[04] \033[1;92mUPDATE")
    print("\033[1;97m====================================================")                    
    m=input('\033[1;97mCOUSE :')
    if m in['1','01']:
        os.system("rm -rf mahdi-mex")
        os.system("git clone https://github.com/Shuvo-BBHH/mahdi-mex")
        os.system("cd mahdi-mex && python mahdi.py")

    if m in['02','2']:
        os.system("rm -rf cloneBD")
        os.system("git clone https://github.com/Shuvo-BBHH/cloneBD")
        os.system("cd cloneBD && python mahdi.py")
    if m in['6','06']:
        os.system('pip uninstall Shuvo')
        os.system('pip install Shuvo')

    if m in['3','03']:
        os.system("xdg-open https://www.facebook.com/bk4human")
        os.system("xdg-open https://www.facebook.com/m4d1")    



    elif m :
        mahdi()

    elif m in ['']:
        mahdi()    

shuvo()