from configparser import ConfigParser
from os import path as osp
from textwrap import dedent
from twindb_backup.verify import edit_backup_my_cnf


def test_edit_backup_my_cnf(tmpdir):
    datadir = tmpdir.mkdir("mysql")
    with open(osp.join(str(datadir), "backup-my.cnf"), "w") as fp:
        fp.write(
            dedent(
                """
                # This MySQL options file was generated by innobackupex.

                # The MySQL server
                [mysqld]
                innodb_checksum_algorithm=crc32
                innodb_log_checksums=1
                innodb_data_file_path=ibdata1:12M:autoextend
                innodb_log_files_in_group=2
                innodb_log_file_size=50331648
                innodb_page_size=16384
                innodb_undo_directory=./
                innodb_undo_tablespaces=2
                server_id=0
                innodb_log_checksums=ON
                innodb_redo_log_encrypt=OFF
                innodb_undo_log_encrypt=OFF
                server_uuid=00eb2d82-dc60-11ec-86a2-0242ac100301
                master_key_id=0
                """
            )
        )
    edit_backup_my_cnf(str(datadir))
    cfg = ConfigParser()
    cfg.read(osp.join(str(datadir), "backup-my.cnf"))
    assert cfg.getboolean("mysqld", "innodb_log_checksums") is True