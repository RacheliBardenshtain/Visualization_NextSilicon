import pandas as pd
import datetime
from typing import Dict

# פונקציה לפירוק cluster_id למילון
def parse_cluster_id(cluster_id: str) -> Dict[str, str]:
    parts = cluster_id.split(',')
    return {
        'chip': parts[0].strip(),
        'die': parts[1].strip(),
        'quad': parts[2].strip(),
        'row': parts[3].strip(),
        'col': parts[4].strip()
    }

# פונקציה ליצירת DataFrame מהקובץ
def create_dataframe_from_log(log_file: str) -> pd.DataFrame:
    data_list = []
    with open(log_file, 'r') as file:
        for line in file:
            # פירוק השורה לפי ;
            parts = line.strip().split(';')

            # המרה של כל חלק לפי הדרישות
            timestamp = float(parts[0].strip())
            datetime_obj = datetime.datetime.fromtimestamp(timestamp)  # המרת timestamp לזמן אמיתי
            cluster_id = parse_cluster_id(parts[1].strip())
            area = parts[2].strip()
            unit = parts[3].strip()
            io = parts[4].strip()
            tid = parts[5].strip()
            packet = parts[6].strip()

            # הוספת השורה ל-DataFrame
            data_list.append({
                'timestamp': datetime_obj,
                'cluster_id': cluster_id,
                'area': area,
                'unit': unit,
                'io': io,
                'tid': tid,
                'packet': packet
            })

    return pd.DataFrame(data_list)