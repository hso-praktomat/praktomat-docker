from shell import *
from datetime import date
from utils import *

thisDir = dirname(__file__)
topDir = abspath(pjoin(thisDir, ".."))
pgBackupDir = f'{HOME}/pgbackup'

def doBackup():
    info('Performing backup with tivoli')
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
    info(f'Dumping postgres DB {dbName} in container {container}')
    mkdir(pgBackupDir, createParents=True)
    today = date.today().isoformat()
    basename = pjoin(pgBackupDir, f'pg_dump_{container}_{dbName}_{today}')
    backupName = freeFilename(basename, '.gz')
    cmd = f"docker exec -ti {container} pg_dump -U postgres {dbName} | gzip > {backupName}"
    info(cmd)
    run(cmd)

def backup(containerWithDbs):
    print()
    info('New backup run ...')
    for (container, db) in containerWithDbs:
        dumpPostgres(container, db)
    doBackup()
    info('Backup run finished')

if __name__ == '__main__':
    backup([
        ('aud-win_db', 'praktomat_default'),
        ('aud-win_db', 'praktomat_aud-win'),
        ('aud-ai_db', 'praktomat_default'),
        ('aud-ai_db', 'praktomat_aud-ai')
    ])
