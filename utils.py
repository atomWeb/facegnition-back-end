import decimal
import json
from datetime import datetime
import dateutil.tz


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 == 0:
                return int(o)
            else:
                return round(float(o), 12)
        return super(DecimalEncoder, self).default(o)

def get_time_by_zone(zone):
    es_time = dateutil.tz.gettz(zone)
    return datetime.now(tz=es_time)

def get_month_year():
    now = datetime.now()
    return f'{now.year:04d}/{now.month:02d}'

def get_str_timestamp_by_zone(zone):
    now_es_time = get_time_by_zone(zone)
    return now_es_time.strftime("%Y-%m-%d %H:%M:%S.%f")

def jsonify(obj, statusCode=200):
    return {
        'headers': {
            'Content-Type': 'application/json'
        },
        'statusCode': statusCode,
        'body': json.dumps(obj, cls=DecimalEncoder)
    }

