import os
import threading

class Manage_Mysql:
    def get_path(self):
        lines = [line.rstrip('\n') for line in open('data/mysql_path.txt')]
        return lines[0]

    def start_mysql(self):
        path = self.get_path();
        print(path + 'mysqld')
        os.system(path + 'mysqld')

    def start(self):
        threading.Thread(target=self.start_mysql).start()

    def stop(self):
        path = self.get_path();
        os.system(path + 'mysqladmin -u root shutdown')