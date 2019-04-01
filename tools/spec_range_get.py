from credentials import REDSHIFT_SETTINGS
import datetime
import psycopg2
from psycopg2 import sql
from tqdm import tqdm

def redshift_connector():
    """connect to redshift using credentials.py"""

    try:
      conn = psycopg2.connect(host=REDSHIFT_SETTINGS['HOST'],
                  port=REDSHIFT_SETTINGS['PORT'],
                  database=REDSHIFT_SETTINGS['DATABASE_NAME'],
                  user=REDSHIFT_SETTINGS['USERNAME'],
                  password=REDSHIFT_SETTINGS['PASSWORD'],
                  connect_timeout=5)
      return conn
    except:
      print("Redshift busted af. You on the VPN?")

def get(wildcard, query):
    """get our query from redshift/metabase"""

    conn = redshift_connector()
    rs_cur = conn.cursor()
    rs_cur.execute(sql.SQL(query), (wildcard,))
    row = rs_cur.fetchall()
    result = ([i for i in row])
    rs_cur.close
    result = tuple(result)
    print(result)
    return result

def get_wildcard():
    """get our wildcard variable for query"""
    
    today = datetime.date(2019, 3, 3) #adjust desired starting date here
    counter = 0
    date_range = []
    while counter <= 20: #adjust how many days you want in range
        date_range.append(today)
        today += datetime.timedelta (days = 1)
        counter += 1
    return date_range

def report(vip_dict,port_count):
  """report findings in a quickly readable translatable way"""
  
  print(f'Total: {port_count}')
  vips = ['Vow(26193)', 'Weave(20193)', 'Expectel(59775)', 'Zang(58)', 'Zen(14449)', 'Signalwire(52284)', 'Intulse(47037)']
  vips_indexer = 0 #index out vip name list for reporting
  for each in vip_dict.values():
    print(f'{vips[vips_indexer]}: {each}\n--')
    vips_indexer += 1

def main():

  query = """
SELECT "public"."trunking_portorder"."id" AS "id", "public"."trunking_portorder"."customer_id" AS "customer_id"
FROM "public"."trunking_portorder"
WHERE CAST("public"."trunking_portorder"."date_created" AS date) = %s
GROUP BY "public"."trunking_portorder"."id", "public"."trunking_portorder"."customer_id"
ORDER BY "public"."trunking_portorder"."id" ASC, "public"."trunking_portorder"."customer_id" """
  port_count = 0
  vip_dict = {26193:0,20193:0,59775:0,58:0,38640:0,52284:0,47037:0}
  date_range = get_wildcard()
  for date in tqdm(date_range): #for each day in week, set SQL wildcard to date and run query for that date
      wildcard = date
      print(f'Date: {wildcard}')
      for pon,uid in get(wildcard, query):
        port_count += 1 #total ports
        if uid in vip_dict:
          vip_dict[uid] += 1 #ports per UID
  report(vip_dict,port_count)

if __name__ == "__main__":
    main()