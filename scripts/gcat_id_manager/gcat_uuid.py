#!/usr/bin/env python
import os
import sys
import pymysql
import getpass
import logging
import argparse

SAMPLES_TABLE = "dev_samples"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main():
    args = parse_option()
    all_flag=args.all_uuid

    if args.mysql_cnf is None:
      args.mysql_cnf = "~/.my.cnf"
      
    if args.mysql_cnf is None:
      args.mysql_cnf = "~/.my.cnf"

    if args.table is None:
      args.table = SAMPLES_TABLE

    if args.uuid is None:
      result = get_uuid(args.name, 0, args.table, args.mysql_cnf, args.password,  all_flag)
    elif args.name is None:
      result = get_uuid(args.uuid, 1, args.table, args.mysql_cnf, args.password, mysql_info)

# check_id: UUID or SAMPLE_NAME    
# check_flag: 0=SAMPLE_NAME to UUID, 1=UUID to SAMPLE_NAME
# all_flag: If true, show all UUIDs 
# password_flag: If true, input password interactive
def get_uuid(check_id, check_flag, table_name, mysql_cnf, password_flag, *all_flag):
    # Connect MySQL
    conn = connect_mysql(password_flag, mysql_cnf)
 
    if len(all_flag) > 0:
      all_flag = all_flag[0]

    # SAMPLE_NAME to UUID
    if check_flag == 0:
      # Show all uuids if add_read > 0
      if all_flag :
        sql = "SELECT BIN_TO_UUID(sample_uuid) AS result FROM %s WHERE sample_name = '%s'" % (table_name, check_id)
      # Show one uuid where max(add_read) 
      else:
        sql = "SELECT BIN_TO_UUID(sample_uuid) AS result FROM %s WHERE sample_name='%s' AND add_read = (SELECT MAX(add_read) from %s where sample_name='%s')" % (table_name, check_id, table_name, check_id)
      out = execute_mysql(sql, conn)
    # UUID to SAMPLE_NAME
    elif check_flag == 1:
      sql = "SELECT sample_name AS result FROM %s WHERE sample_uuid=UUID_TO_BIN('%s') ORDER BY add_read " % (table_name, check_id)
      out = execute_mysql(sql, conn)
    if len(out) == 0:
      logger.error("[ERROR] No such ID.")
      exit(1)
    elif len(out) > 1:
      for a in out:
        return a['result']
    else:
      return out[0]['result']

def parse_option():
    parser = argparse.ArgumentParser(description='Print UUID to SAMPLE NAME or SAMPLE NAME to UUID.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-u', '--uuid', help="Show SAMPLE_NAME from UUID")
    group.add_argument('-n', '--name', help="Show UUID from SAMPLE_NAME")
    parser.add_argument('-a', '--all_uuid', help="Show all UUIDs if there are some IDs (Default: show only MAX add_read)", action='store_true')
    parser.add_argument('-t', '--table', help="Specify MySQL table name (Default: \"samples\")")
    parser.add_argument('-c', '--mysql_cnf', help="Specify MySQL config path (Default: ~/.my.cnf)")
    parser.add_argument('-p', '--password', help="Input MySQL password interactive (Default: read from my.cnf)", action='store_true')
    args = parser.parse_args()

    if (args.uuid is None) and (args.name is None):
      logger.error("[ERROR] Specify UUID or SAMPLE NAME.")
      exit(1)

    return args

def connect_mysql(password_flag, mysql_cnf):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    try:
        if password_flag:
          password = getpass.getpass("Input MySQL user password: ")
          conn = pymysql.connect(password=password, connect_timeout=5, cursorclass=pymysql.cursors.DictCursor, read_default_file=mysql_cnf)
        else:
          conn = pymysql.connect(connect_timeout=5, cursorclass=pymysql.cursors.DictCursor, read_default_file=mysql_cnf)
    except pymysql.MySQLError as e:
        logger.error("[ERROR] Could not connect to MySQL server.")
        logger.error(e)
        sys.exit()
    return conn

def execute_mysql(sql, conn):
    logger = logging.getLogger()
    with conn.cursor() as cur:
        cur.execute(sql)
        result = cur.fetchall()
    conn.commit()
    return result

if __name__ == '__main__':
  main() 
