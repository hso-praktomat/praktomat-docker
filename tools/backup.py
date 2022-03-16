from shell import *
from datetime import date

thisDir = dirname(__file__)
topDir = abspath(pjoin(thisDir, ".."))
pgBackupDir = f'{HOME}/pgbackup'

def doBackup():
    run(f'{topDir}/tivoli-client/run-tivoli-client dsmc incr /data')

def freeFilename(name, ext):
    cand = name + ext
    if not exists(cand):
        return cand
    for i in range(1000):
        cand = f'{name}_{i}{ext}'
        if not exists(cand):
            return cand
    raise ValueError(f"No free file name found: {cand}")

def dumpPostgres(container, dbName):
    mkdir(pgBackupDir, createParents=True)
    today = date.today().isoformat()
    basename = pjoin(pgBackupDir, f'pg_dump_{container}_{dbName}_{today}')
    backupName = freeFilename(basename, '.gz')
    cmd = f"docker exec -ti {container} pg_dump -U postgres {dbName} | gzip > {backupName}"
    print(cmd)
    run(cmd)

def backup(containerWithDbs):
    for (container, db) in containerWithDbs:
        dumpPostgres(container, db)
    doBackup()

if __name__ == '__main__':
    backup([
        ('aud-win_db', 'praktomat_default'),
        ('aud-win_db', 'praktomat_aud-win'),
        ('aud-ai_db', 'praktomat_default'),
        ('aud-ai_db', 'praktomat_aud-ai')
    ])
