import BaseConfig
import json


def parse_json(file_path):
    data_list = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = file.read()
        data = json.loads(json_data)
        # 解析设备信息
        devices = data.get('devices', {})
        for device_name, device_info in devices.items():
            geo = device_info.get('geo')
            info = {
                "name": device_name,
                "height": geo[0],
                "type": "station",
                "LatLng": {
                    "lat": geo[1],
                    "lng": geo[2]
                },
            }
            data_list.append(info)

        # 解析目标信息
        target = data.get('target', {})
        info = {
            "name": "A drone",
            "height": target.get('H'),
            "type": "drone",
            "LatLng": {
                "lng": target.get('L'),
                "lat": target.get('B'),
            },
        }
        data_list.append(info)
        return data_list
    except FileNotFoundError:
        print(f"未找到文件: {file_path}")
    except json.JSONDecodeError:
        print("JSON 数据格式有误，请检查。")


if __name__ == "__main__":
    file_path = BaseConfig.DB_PATH + '/current_result.txt'
    print(parse_json(file_path))
