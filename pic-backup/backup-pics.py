
import subprocess 


def backup_pics(pic_links):
    with open(pic_links) as f:
        for line in f.read().splitlines():
            if len(line) < 3:
                continue
            link = line[2:]
            cmd = f'''curl -O {link}'''
            subprocess.run(cmd)


backup_pics("../pic-links.txt")
