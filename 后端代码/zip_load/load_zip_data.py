import os
import zipfile
from os import path
import zip_load.data_setting as data_setting

class LoadZip():
    def __init__(self, class_id, class_year, class_teacher, zip_name):
        self.class_id = str(class_id)
        self.class_year =str(class_year)
        self.class_teacher = str(class_teacher)
        self.zip_name = zip_name
        self.zip_path = ""
        self.zip_data_path = ""

    def get_zip_path(self):

        if self.zip_path == "":
            file_dir_name = self.class_id + "_" + self.class_year + "_" + self.class_teacher
            zip_path = path.join(data_setting.zips_path, file_dir_name)
            if not path.exists(zip_path):
                os.mkdir(zip_path)
            self.zip_path = zip_path
        return self.zip_path

    def get_data_path(self):

        if self.zip_path == "":
            self.get_zip_path()
        data_path = path.join(self.zip_path, data_setting.zip_data_path)
        if not path.exists(data_path):
            os.mkdir(data_path)
        self.zip_data_path = data_path
        return data_path

    def get_zipfile(self):
        zip_path = self.get_zip_path()
        load_data_path = self.get_data_path()
        zip_file_path = path.join(zip_path, self.zip_name)
        if path.exists(zip_file_path):
            with zipfile.ZipFile(zip_file_path, 'r') as zf:
                for file_name in zf.namelist():
                    try:
                        new_name = file_name.encode('cp437').decode('gbk')
                    except:
                        new_name = file_name.encode('utf-8').decode('utf-8')
                    new_path = path.join(load_data_path, new_name)
                    if zf.getinfo(file_name).file_size > 0:
                        with open(file=new_path, mode='wb') as f:
                            f.write(zf.read(file_name))
                    else:
                        os.mkdir(new_path)
        else:
            return 1
        return 0


def load_zip_data(course_id,course_year,teacher_id,zip_name):
    load_zip = LoadZip(course_id, course_year, teacher_id, zip_name)
    load_zip.get_zipfile()


if __name__ == "__main__":
    load_zip = LoadZip('1', '2018', "258369", 'C_demo.zip')
    load_zip.get_zipfile()
