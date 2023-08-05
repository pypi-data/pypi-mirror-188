import configparser
from datetime import timedelta, datetime
import os
import logging

import fabric
from ftplib import FTP

import config
from domain.equipment_management import Equipments

class EquipmentShell(Equipments):

    @staticmethod
    def ssh_open_connection(equipment_name):
        # Test done
        try:
            connection = fabric.Connection(equipment_name, user=config.ssh_username,
                                           connect_kwargs={'password': config.ssh_password})
            connection.open()
            return connection
        except Exception as e:
            logging.error(e)

    @staticmethod
    def load_all(file_path: str = f"{config.inventory_local_directory}/{config.inventory_file_name}"):
        # Test done
        try:
            config_ = configparser.ConfigParser(allow_no_value=True)
            config_.read(file_path)

            equipments_dict: dict = {}

            for section in config_.sections():
                for variable in config_[section]:
                    if variable.__contains__(config.separateur):
                        equipment = EquipmentShell()
                        equipment.name, equipment.ip = variable.split(config.separateur)
                        equipment.ip = equipment.ip.removesuffix("\n")
                        # EquipmentShell.equipment_list.append(equipment)
                        equipments_dict[section] = equipments_dict.get(section, []) + [equipment]
            EquipmentShell.equipment_dict = equipments_dict
            return equipments_dict
        except Exception as e:
            logging.error(e)

    @staticmethod
    def ftp_get_config_files(dir_ftp_switchs: str = config.directory_ftp_switchs):
        # Tests done
        try:
            ftp_host = config.ftp_host
            ftp_user = config.ftp_username
            ftp_directory = config.directory_ftp_switchs

            logging.info(f"FTP connection : host = {ftp_host}, user = {ftp_user}, directory = {ftp_directory}")
            ftp = FTP(host=ftp_host, user=ftp_user, passwd=config.ftp_password)
            ftp.cwd(dir_ftp_switchs)

            files_in_ftp_dir = ftp.nlst()

            date_limit = EquipmentShell.recent_date_detection(ftp)
            logging.info(f"Most recent date : {date_limit} in directory {ftp_directory}")

            for file in files_in_ftp_dir:
                date_file = EquipmentShell.get_date_from_ftp_file(file)
                if date_file == date_limit:
                    ftp.retrbinary(f"RETR {file}", open(
                        f"{config.switch_configs_local_directory}/{EquipmentShell.new_name_file_from_ftp_dir(file)}",
                        'wb').write)
                    # logging.info(f"File {file}_{date_file} downloaded from FTP")
            logging.info("Configs versioning done!")
        except Exception as e:
            logging.error(e)

    @staticmethod
    def create(name_group: str, list_values: list,
               file_path: str = f"{config.inventory_local_directory}/{config.inventory_file_name}"):
        try:
            config_ = configparser.ConfigParser(allow_no_value=True)
            config_.read(file_path)

            config_.add_section(name_group)

            for ligne in list_values:
                name = ligne.split(' ')[0]
                ip = ligne.split(' ')[1]
                config_.set(name_group, f"{name}{config.separateur}{ip}", None)

            with open(file_path, 'w') as configfile:
                config_.write(configfile)
                logging.info(f"Equipment {name_group} created")
        except Exception as e:
            logging.error(e)

    @staticmethod
    def edit(name_group: str, list_values: list,
             file_path: str = f"{config.inventory_local_directory}/{config.inventory_file_name}"):
        try:
            config_ = configparser.ConfigParser(allow_no_value=True)
            config_.read(file_path)

            for section in config_.sections():
                if section == name_group:
                    config_.remove_section(name_group)
                    config_.add_section(name_group)

            for ligne in list_values:
                name = ligne.split(' ')[0]
                ip = ligne.split(' ')[1]
                config_.set(name_group, f"{name}{config.separateur}{ip}", None)

            with open(file_path, 'w') as configfile_edit:
                config_.write(configfile_edit)
            logging.info(f"Equipment {name_group} edited")
        except Exception as e:
            logging.error(e)

    @staticmethod
    def remove(name_group: str,
               file_path: str = f"{config.inventory_local_directory}/{config.inventory_file_name}"):
        try:
            config_ = configparser.ConfigParser(allow_no_value=True)
            config_.read(file_path)

            for section in config_.sections():
                if section == name_group:
                    config_.remove_section(name_group)

            with open(file_path, 'w') as configfile_remove:
                config_.write(configfile_remove)
            logging.info(f"Equipment {name_group} remove")
        except Exception as e:
            logging.error(e)

    @staticmethod
    def new_name_file_from_ftp_dir(file_name: str):
        # Tests done
        try:
            return f"{file_name.split('_')[0]}.txt"
        except Exception as e:
            logging.error(e)

    @staticmethod
    def get_date_from_ftp_file(file_name: str):
        # Tests done
        try:
            return f"{file_name.split('_')[1].split('.')[0]}"
        except Exception as e:
            logging.error(e)

    @staticmethod
    def recent_date_detection(ftp: FTP):
        # Tests done
        try:
            files_in_ftp_dir = ftp.nlst()

            older_date = datetime.min.strftime('%Y%m%d')

            for file in files_in_ftp_dir:
                date_file = EquipmentShell.get_date_from_ftp_file(file)
                if date_file > older_date:
                    older_date = date_file
            return older_date
        except Exception as e:
            logging.error(e)
