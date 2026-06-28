import psutil, subprocess, io, csv

SYSTEM_PROCESSES = {
    'system', 'svchost.exe', 'explorer.exe', 'winlogon.exe', 'csrss.exe', 'smss.exe',
    'lsass.exe', 'services.exe', 'wininit.exe', 'taskmgr.exe', 'cmd.exe', 'powershell.exe',
    'conhost.exe', 'sihost.exe', 'runtimebroker.exe', 'dwm.exe', 'fontdrvhost.exe',
    'audiodg.exe', 'spoolsv.exe', 'searchindexer.exe', 'wudfhost.exe', 'das.exe',
    'asuscertservice.exe', 'esif_uf.exe', 'midisrv.exe', 'wmiregistrationservice.exe', 'dtsapo4service.exe', 
    'rogliveservice.exe', 'lsaiso.exe', 'registry', 'aggregatorhost.exe', 'armourycrate.service.exe', 'startmenuexperiencehost.exe', 
    'dashost.exe', 'gpupowersavingtrayicon.exe', 'asussoftwaremanageragent.exe', 
    'asussystemanalysis.exe', 'searchhost.exe', 'dllhost.exe', 'secure system', 'officeclicktorun.exe', 
    'nissrv.exe', 'memory compression', 'asussoftwaremanager.exe', 'securityhealthservice.exe', 'jhi_service.exe', 
    'asusoptimization.exe', 'gamesdk.exe', 'igfxcuiservice.exe', 'igfxem.exe', 'asusswitch.exe', 
    'armourysocketserver.exe', 'system idle process', 'asusappservice.exe', 'intelcphecisvc.exe', 'msmpeng.exe', 
    'mpdefendercoreservice.exe', 'intelcphdcpsvc.exe', 'nvdisplay.container.exe', 'memuservice.exe', 'wlanext.exe', 
    'aacambientlighting.exe', 'wmiprvse.exe', 'armourycrate.usersessionhelper.exe', 'nvsphelper64.exe', 'nvcontainer.exe', 
    'asusptpservice.exe', 'msedgewebview2.exe', 'shellhost.exe', 'textinputhost.exe', 'asus_framework.exe', 'unsecapp.exe', 
    'ctfmon.exe', 'rtkauduservice64.exe', 'presentationfontcache.exe', 'pet.exe', 'asussystemdiagnosis.exe', 
    'rvcontrolsvc.exe', 'armouryswagent.exe', 'shellexperiencehost.exe', 'tasklist.exe', 'armourycratecontrolinterface.exe',
    'armouryhtmldebugserver.exe', 'lightingservice.exe', 'oneapp.igcc.winservice.exe', 'widgetservice.exe',
    'smartscreen.exe', 'bash.exe', 'code.exe', 'python.exe', 'widgets.exe', 'sppsvc.exe', 'gamebarftserver.exe'
}

def get_open_programs():
    try:
        result = subprocess.run(['tasklist', '/FI', 'WINDOWTITLE ne N/A', '/FO', 'CSV', '/NH'],
                                capture_output=True, text=True, encoding='cp866')
        if result.returncode != 0:
            return []
        
        programs = set()
        reader = csv.reader(io.StringIO(result.stdout))
        for row in reader:
            if len(row) > 0:
                name = row[0].strip('"').lower()
                if name and name not in SYSTEM_PROCESSES:
                    programs.add(name)
        return list(programs)
    except Exception:
        programs = set()
        for proc in psutil.process_iter(['name']):
            try:
                name = proc.info['name'].lower()
                if name and name not in SYSTEM_PROCESSES:
                    programs.add(name)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return list(programs)

def close_unwanted_programs(allowed_list, open_progs):
    allowed = [name.lower() for name in allowed_list]

    for prog in open_progs:
        if prog not in allowed and prog not in SYSTEM_PROCESSES:
            try:
                subprocess.run(['taskkill', '/F', '/IM', prog], capture_output=True, check=False)
            except Exception:
                pass


