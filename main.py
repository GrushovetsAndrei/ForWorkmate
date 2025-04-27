import os
import argparse
from functools import reduce
from collections import Counter

class Report_handler():
    def __init__(self, data : dict) -> None:
        self.data = data
        if self.data:
            self.headers = ['HANDLER', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        else:
            self.headers = []

    def __str__(self) -> str:
        if self.data:
            result = f'Total requests: {sum(self.data[' '].values())}\n\n'
            result += f'{self.headers[0].ljust(25,' ')}{self.headers[1].ljust(12,' ')}'
            result += f'{self.headers[2].ljust(12,' ')}{self.headers[3].ljust(12,' ')}'
            result += f'{self.headers[4].ljust(12,' ')}{self.headers[5].ljust(12,' ')}\n'

            for key in self.data.keys():
                result += f'{key.ljust(25,' ')}'
                result += f'{str(self.data[key].get('DEBUG',0)).ljust(12,' ')}'
                result += f'{str(self.data[key].get('INFO',0)).ljust(12,' ')}'
                result += f'{str(self.data[key].get('WARNING',0)).ljust(12,' ')}'
                result += f'{str(self.data[key].get('ERROR',0)).ljust(12,' ')}'
                result += f'{str(self.data[key].get('CRITICAL',0)).ljust(12,' ')}\n'
        else:
            result = ''
        return result

class TzLogger():
    def __init__(self)-> None: 
        if self.read_args():
            self.data = self.read_log()
        else:
            self.data = {}
            
    def show_report(self) -> bool:
        '''При необхожимости добавить еще несколько вариантов отчетов дополним  
        проверку значения параметра --report'''
        if self.args.report.lower() == 'handlers':
            report = Report_handler(self.data)
            print(report)
            return True
        else:
            print('Error! The report name is incorrect.')
            return False
        return True

    def read_args(self) -> bool :
        try:
            parser = argparse.ArgumentParser(exit_on_error=False)
            parser.add_argument('log', nargs='+', help='Имя файла с логами') #Проверить пустые аргументы
            parser.add_argument('--report', '-r', choices=['handlers'], default='handlers', help="Вывод отчета")
            self.args = parser.parse_args()
            return True
        except BaseException as e:
            self.args = argparse.Namespace(log = [], report = '')
            print('Error! Arguments parse error')
            return False

    def read_log(self) -> dict:
        try:
            self.data =[]
            for filename in self.args.log:
                if os.path.exists(filename) and not(os.path.isdir(filename)):
                    with open(filename, 'r') as file:
                        for line in file.readlines():
                            items = line.split(' ')
                            #Фильтруем по типу ручки "django.request"
                            if len(items) >= 6 and items[3][:-1]=='django.request':
                                tmp = dict()
                                tmp['Value'] = items[2]
                                tmp['Handler'] = ' '.join(items[5:])[' '.join(items[5:]).find(' /')+1:' '.join(items[5:]).find('/ ')+1]
                                if tmp['Handler'].replace(' ','') != '':
                                    self.data.append(tmp)
            
            logs_by_handler = reduce(self.group_by_log, self.data, {})
            logs_by_handler = dict(sorted(logs_by_handler.items()))
            logs_by_handler[' '] = {}
            for key in logs_by_handler.keys():
                if key != ' ':
                    items = logs_by_handler[key]
                    items_count = {x: items.count(x) for x in set(items)}
                    logs_by_handler[key] = items_count
                    logs_by_handler[' '] = dict(Counter(logs_by_handler[key])+\
                                                    Counter(logs_by_handler[' ']))
            if len(logs_by_handler.keys()) == 1:
                return {}
            else:
                return logs_by_handler
        except:
            return {}

    def group_by_log(self, acc: dict, log: dict) -> dict:
        if log["Handler"] not in acc:
            acc[log["Handler"]] = []
        acc[log["Handler"]].append(log["Value"])
        return acc

if __name__ == "__main__":
    app = TzLogger()
    app.show_report()
