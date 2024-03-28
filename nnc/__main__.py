from .func import crawl
import json
import sys
from datetime import datetime

if __name__ == '__main__':
    result = crawl(sys.argv[1])

    f = open(f'''result-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json''''', 'w', encoding='utf-8')
    json.dump(result, f, ensure_ascii=False)
