import json


class JSONPipeline(object):
    def open_spider(self, spider):
        self.file = open('../data/protests.json', 'w')
        self.file.write('[')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False) + ",\n"
        self.file.write(line)

        return item

    def close_spider(self, spider):
        self.file.write("]")
        self.file.close()
